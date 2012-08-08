/**
 * @file visioner/src/lut_problem.cc
 * @date Fri 27 Jul 13:58:57 2012 CEST
 * @author Andre Anjos <andre.anjos@idiap.ch>
 *
 * @brief This file was part of Visioner and originally authored by "Cosmin
 * Atanasoaei <cosmin.atanasoaei@idiap.ch>". It was only modified to conform to
 * Bob coding standards and structure.
 *
 * Copyright (C) 2011-2012 Idiap Research Institute, Martigny, Switzerland
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 3 of the License.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <numeric>

#include "core/logging.h"
#include "lbfgs/lbfgs.h"

#include "visioner/model/trainers/lutproblems/lut_problem.h"
#include "visioner/model/mdecoder.h"

namespace bob { namespace visioner {

  namespace lbfgs_wrapper
  {
    ////////////////////////////////////////////////////////////////////////////////
    // libLBFGS wrapper.
    ////////////////////////////////////////////////////////////////////////////////

    static lbfgsfloatval_t linesearch(
        void* instance, const lbfgsfloatval_t* x, lbfgsfloatval_t* g,
        const int, const lbfgsfloatval_t)
    {
      LUTProblem* lp = (LUTProblem*)instance;
      return lp->linesearch(x, g);
    }
  }

  // Constructor
  LUTProblem::LUTProblem(
      const DataSet& data, const param_t& param)
    :       m_data(data), 
    m_param(param),

    m_rloss(make_loss(param)),
    m_loss(*m_rloss),

    m_sharing(make_sharing(param)),

    m_mluts(n_outputs()),
    m_luts(n_outputs(), LUT(0, n_entries())),

    m_sscores(n_samples(), n_outputs(), 0.0),
    m_wscores(n_samples(), n_outputs()),
    m_cscores(n_samples(), n_outputs()),

    m_umasks(n_features(), n_entries(), 0.0)
    {
      std::vector<double> counts(n_entries());
      std::vector<std::pair<double, uint64_t> > stats(n_entries());

      const double cutoff = 0.90;

      // Mask the entries that are not frequent enough                
      //      - the associated response is fixed to zero!
      for (uint64_t f = 0; f < n_features(); f ++)
      {
        std::fill(counts.begin(), counts.end(), 0.0);
        for (uint64_t s = 0; s < n_samples(); s ++)
        {
          const uint16_t u = fvalue(f, s);
          counts[u] += cost(s);
        }
        const double thres = cutoff * std::accumulate(counts.begin(), counts.end(), 0.0);

        for (uint64_t u = 0; u < n_entries(); u ++)
        {
          stats[u].first = counts[u];
          stats[u].second = u;
        }                        
        std::sort(stats.begin(), stats.end(), std::greater<std::pair<double, uint64_t> >());                        

        double sum = 0.0;
        for (uint64_t uu = 0; uu < n_entries() && sum < thres; uu ++)
        {
          const double cnt = stats[uu].first;
          const uint64_t u = stats[uu].second;

          m_umasks(f, u) = 1.0;                                
          sum += cnt;
        }
      }
    }

  // Update predictions
  void LUTProblem::update_scores(const std::vector<LUT>& luts)
  {
# pragma omp parallel for
    for (uint64_t s = 0; s < n_samples(); s ++)
    {
      for (uint64_t o = 0; o < n_outputs(); o ++)
      {
        const LUT& lut = luts[o];                        
        const uint16_t u = fvalue(lut.feature(), s);
        m_sscores(s, o) += lut[u];
      }
    }
  }

  // Update current scores
  void LUTProblem::update_cscores(const double* x)
  {
# pragma omp parallel for
    for (uint64_t s = 0; s < n_samples(); s ++)
    {
      for (uint64_t o = 0; o < n_outputs(); o ++)
      {
        m_cscores(s, o) = m_sscores(s, o) + x[o] * m_wscores(s, o);
      }
    }
  }

  // Optimize the LUT entries for the selected feature
  bool LUTProblem::line_search()
  {
    // Buffer the weak learner scores
# pragma omp parallel for
    for (uint64_t s = 0; s < n_samples(); s ++)
    {
      for (uint64_t o = 0; o < n_outputs(); o ++)
      {
        const LUT& lut = m_luts[o];
        const uint64_t u = fvalue(lut.feature(), s);
        m_wscores(s, o) = lut[u];
      }
    }

    // Line-search to scale the LUT entries (using libLBFGS)
    static const uint64_t iters = 20;
    lbfgs_parameter_t param;
    lbfgs_parameter_init(&param);
    param.max_iterations = iters;
    param.epsilon = 1e-40;
    param.min_step = 1e-40;
    param.linesearch = LBFGS_LINESEARCH_BACKTRACKING;

    lbfgsfloatval_t* x = lbfgs_malloc(n_outputs());
    lbfgsfloatval_t* fx = lbfgs_malloc(1);

    std::fill(x, x + n_outputs(), 0.0);
    *fx = 0.0;

    const int ret = lbfgs(n_outputs(), x, fx, lbfgs_wrapper::linesearch,
        NULL, (void*)this, &param);

    const double min_x = *std::min_element(x, x + n_outputs());
    const double max_x = *std::max_element(x, x + n_outputs());

    const bool ok = (max_x > std::numeric_limits<double>::epsilon()) &&
      (ret == LBFGS_SUCCESS ||
       ret == LBFGS_ALREADY_MINIMIZED ||
       ret == LBFGSERR_MAXIMUMLINESEARCH ||
       ret == LBFGSERR_MAXIMUMITERATION ||
       ret == LBFGSERR_ROUNDING_ERROR ||
       ret == LBFGSERR_MINIMUMSTEP ||
       ret == LBFGSERR_MAXIMUMSTEP);

    // OK, setup std::vector<LUT>
    if (ok == true)
    {
      for (uint64_t o = 0; o < n_outputs(); o ++)
      {
        LUT& lut = m_luts[o];
        lut.scale(x[o]);
        m_mluts[o].push_back(lut);
      }                 
    }

    bob::core::info << "line-search step = [" << min_x << " - " << max_x << "]"
      << std::endl;

    lbfgs_free(x);
    lbfgs_free(fx);
    return ok;
  }

}}