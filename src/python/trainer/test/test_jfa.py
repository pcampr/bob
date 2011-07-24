#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Thu 14 Jul 2011

"""Test JFA trainer package
"""

import os, sys
import unittest
import torch
import random

def equals(x, y, epsilon):
  return (abs(x - y) < epsilon).all()

class JFATrainerTest(unittest.TestCase):
  """Performs various JFA trainer tests."""
  
  def test01_updateEigen(self):
    # Tests our updateEigen function
    A = torch.core.array.float64_3(
      [0.9293, 0.2511, 0.3517, 0.3500, 0.6160, 0.8308, 0.1966, 0.4733, 0.5853,
      0.5497, 0.7572, 0.5678, 0.9172, 0.7537, 0.0759, 0.2858, 0.3804, 0.0540], (2,3,3))

    C = torch.core.array.float64_2([
      0.1361, 0.5499, 0.6221, 0.4018, 0.1233, 0.4173, 0.9448, 0.3377,
      0.8693, 0.1450, 0.3510, 0.0760, 0.1839, 0.0497, 0.4909, 0.9001,
      0.5797, 0.8530, 0.5132, 0.2399, 0.2400, 0.9027, 0.4893, 0.3692], (3,8))

    uv = torch.core.array.float64_2((3,8))

    # call the update_u function
    torch.trainer.jfa_updateEigen(A,C,uv)
    # Expected results (JFA cookbook, matlab)
    uv_ref = torch.core.array.float64_2([
      -0.3120, 0.8754, 0.7009, 0.5404, -0.9020, -5.2395, -1.3741, 0.4054,
      -1.2266, 20.2066, 7.6548, 5.4262, 1.4229, 6.7651, 2.3354, 0.7859,
      2.0873, -15.1771, -5.5488, -4.1597, -0.8070, -3.2141, -0.1202, -0.8457], (3,8))

    # Makes sure results are good
    self.assertTrue(equals(uv, uv_ref, 5e-3))

  def test02_estimateXandU(self):
    # test the estimateXandU function
    F=torch.core.array.float64_2(
      [0.3833, 0.6173, 0.5755, 0.5301, 0.2751, 0.2486,
      0.4516, 0.2277, 0.8044, 0.9861, 0.0300, 0.5357,
      0.0871, 0.8021, 0.9891, 0.0669, 0.9394, 0.0182,
      0.6838, 0.7837, 0.5341, 0.8854, 0.8990, 0.6259], (4,6))
    N=torch.core.array.float64_2(
      [0.1379, 0.2178, 
      0.1821, 0.0418, 
      0.1069, 0.6164, 
      0.9397, 0.3545], (4,2))
    m=torch.core.array.float64_1([0.1806, 0.0451, 0.7232, 0.3474, 0.6606, 0.3839], (6,))
    E=torch.core.array.float64_1([0.6273, 0.0216, 0.9106, 0.8006, 0.7458, 0.8131], (6,))
    d=torch.core.array.float64_1([0.4106, 0.9843, 0.9456, 0.6766, 0.9883, 0.7668], (6,))
    v=torch.core.array.float64_2(
      [0.3367, 0.6624, 0.2442, 0.2955, 0.6802, 0.5278,
      0.4116, 0.6026, 0.7505, 0.5835, 0.5518, 0.5836], (2,6))
    u=torch.core.array.float64_2(
      [0.5118, 0.0826, 0.7196, 0.9962, 0.3545, 0.9713,
      0.3464, 0.8865, 0.4547, 0.4134, 0.2177, 0.1257], (2,6))
    z=torch.core.array.float64_2(
      [0.3089, 0.7261, 0.7829, 0.6938, 0.0098, 0.8432,
      0.9223, 0.7710, 0.0427, 0.3782, 0.7043, 0.7295], (2,6))
    y=torch.core.array.float64_2([0.2243, 0.2691, 0.6730, 0.4775], (2,2))
    x=torch.core.array.float64_2((4,2))
    spk_ids=torch.core.array.uint32_1([0,0,1,1], (4,))

    # call the estimateXandU function
    torch.trainer.jfa_estimateXandU(F,N,m,E,d,v,u,z,y,x,spk_ids)
    # Expected results(JFA cookbook, matlab)
    x_ref=torch.core.array.float64_2(
      [0.2143, 3.1979,
      1.8275, 0.1227,
      -1.3861, 5.3326,
      0.2359,  -0.7914], (4,2))

    # Makes sure results are good
    self.assertTrue(equals(x, x_ref, 2e-4))

  def test03_estimateYandV(self):
    # test the estimateYandV function
    F=torch.core.array.float64_2(
      [0.3833, 0.6173, 0.5755, 0.5301, 0.2751, 0.2486,
      0.4516, 0.2277, 0.8044, 0.9861, 0.0300, 0.5357,
      0.0871, 0.8021, 0.9891, 0.0669, 0.9394, 0.0182,
      0.6838, 0.7837, 0.5341, 0.8854, 0.8990, 0.6259], (4,6))
    N=torch.core.array.float64_2(
      [0.1379, 0.2178, 
      0.1821, 0.0418, 
      0.1069, 0.6164, 
      0.9397, 0.3545], (4,2))
    m=torch.core.array.float64_1([0.1806, 0.0451, 0.7232, 0.3474, 0.6606, 0.3839], (6,))
    E=torch.core.array.float64_1([0.6273, 0.0216, 0.9106, 0.8006, 0.7458, 0.8131], (6,))
    d=torch.core.array.float64_1([0.4106, 0.9843, 0.9456, 0.6766, 0.9883, 0.7668], (6,))
    v=torch.core.array.float64_2(
      [0.3367, 0.6624, 0.2442, 0.2955, 0.6802, 0.5278,
      0.4116, 0.6026, 0.7505, 0.5835, 0.5518, 0.5836], (2,6))
    u=torch.core.array.float64_2(
      [0.5118, 0.0826, 0.7196, 0.9962, 0.3545, 0.9713,
      0.3464, 0.8865, 0.4547, 0.4134, 0.2177, 0.1257], (2,6))
    z=torch.core.array.float64_2(
      [0.3089, 0.7261, 0.7829, 0.6938, 0.0098, 0.8432,
      0.9223, 0.7710, 0.0427, 0.3782, 0.7043, 0.7295], (2,6))
    y=torch.core.array.float64_2((2,2))
    x=torch.core.array.float64_2(
      [0.9976, 0.1375,
      0.8116, 0.3900,
      0.4857, 0.9274,
      0.8944, 0.9175], (4,2))
    spk_ids=torch.core.array.uint32_1([0,0,1,1], (4,))

    # call the estimateXandU function
    torch.trainer.jfa_estimateYandV(F,N,m,E,d,v,u,z,y,x,spk_ids)

    # Expected results(JFA cookbook, matlab)
    y_ref=torch.core.array.float64_2(
      [0.9630, 1.3868,
      0.04255, -0.3721], (2,2))

    # Makes sure results are good
    self.assertTrue(equals(y, y_ref, 2e-4))

  def test04_estimateZandD(self):
    # test the estimateYandV function
    F=torch.core.array.float64_2(
      [0.3833, 0.6173, 0.5755, 0.5301, 0.2751, 0.2486,
      0.4516, 0.2277, 0.8044, 0.9861, 0.0300, 0.5357,
      0.0871, 0.8021, 0.9891, 0.0669, 0.9394, 0.0182,
      0.6838, 0.7837, 0.5341, 0.8854, 0.8990, 0.6259], (4,6))
    N=torch.core.array.float64_2(
      [0.1379, 0.2178, 
      0.1821, 0.0418, 
      0.1069, 0.6164, 
      0.9397, 0.3545], (4,2))
    m=torch.core.array.float64_1([0.1806, 0.0451, 0.7232, 0.3474, 0.6606, 0.3839], (6,))
    E=torch.core.array.float64_1([0.6273, 0.0216, 0.9106, 0.8006, 0.7458, 0.8131], (6,))
    d=torch.core.array.float64_1([0.4106, 0.9843, 0.9456, 0.6766, 0.9883, 0.7668], (6,))
    v=torch.core.array.float64_2(
      [0.3367, 0.6624, 0.2442, 0.2955, 0.6802, 0.5278,
      0.4116, 0.6026, 0.7505, 0.5835, 0.5518, 0.5836], (2,6))
    u=torch.core.array.float64_2(
      [0.5118, 0.0826, 0.7196, 0.9962, 0.3545, 0.9713,
      0.3464, 0.8865, 0.4547, 0.4134, 0.2177, 0.1257], (2,6))
    z=torch.core.array.float64_2((2,6))
    y=torch.core.array.float64_2([0.2243, 0.2691, 0.6730, 0.4775], (2,2))
    x=torch.core.array.float64_2(
      [0.9976, 0.1375,
      0.8116, 0.3900,
      0.4857, 0.9274,
      0.8944, 0.9175], (4,2))
    spk_ids=torch.core.array.uint32_1([0,0,1,1], (4,))

    # call the estimateXandU function
    torch.trainer.jfa_estimateZandD(F,N,m,E,d,v,u,z,y,x,spk_ids)

    # Expected results(JFA cookbook, matlab)
    z_ref=torch.core.array.float64_2(
      [0.3256, 1.8633, 0.6480, 0.8085, -0.0432, 0.2885,
      -0.3324, -0.1474, -0.4404, -0.4529, 0.0484, -0.5848], (2,6))

    # Makes sure results are good
    self.assertTrue(equals(z, z_ref, 2e-4))


if __name__ == '__main__':
  sys.argv.append('-v')
  if os.environ.has_key('TORCH_PROFILE') and \
      os.environ['TORCH_PROFILE'] and \
      hasattr(torch.core, 'ProfilerStart'):
    torch.core.ProfilerStart(os.environ['TORCH_PROFILE'])
  os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))
  unittest.main()
  if os.environ.has_key('TORCH_PROFILE') and \
      os.environ['TORCH_PROFILE'] and \
      hasattr(torch.core, 'ProfilerStop'):
    torch.core.ProfilerStop()