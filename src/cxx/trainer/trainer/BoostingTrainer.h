#ifndef _TORCH5SPRO_BOOSTING_TRAINER_H_
#define _TORCH5SPRO_BOOSTING_TRAINER_H_

#include "core/DataSet.h"
#include "trainer/WeakLearner.h"
#include "measurer/measurer.h"
#include "trainer/FTrainer.h"

namespace Torch
{

	class BoostingTrainer : public FTrainer
	{
	public:
		///
		BoostingTrainer();

		///
		virtual bool setWeakLearners(int n_classifiers_, WeakLearner **weak_learners_);

		///
		virtual bool train();
		virtual double forward(const Tensor *example_);
		///
		virtual void initWeights();
		virtual void updateWeights();

		//
		virtual bool noSampling();
		virtual bool randomSampling();

		///
		virtual ~BoostingTrainer();

		//   virtual void cleanup();

	protected: //was private before.. changed by Venkatesh
		//
		void cleanup();

		// Sample weights
		double *m_weights_samples;

		// Label
		short *m_label_samples;

		LabelledMeasure *m_labelledmeasure;

		// shuffle index
		long *m_shuffledindex_dataset;

		// sample repartition (for boosting by sampling)
		double *m_repartition;

		// Number of classifiers
		int m_n_classifiers;

		// Number of examples
		int m_n_examples;

		// Number of weak classifiers
		int m_n_classifiers_trained;

		// Weak classifier weights
		double *m_weights;

		// Weak learners (to train weak classifiers)
		WeakLearner **m_weak_learners;

		bool verbose;
	};
}

#endif