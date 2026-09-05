import unittest

from opendbc.car import structs
from opendbc.car.gm.interface import CarInterface
from opendbc.car.gm.values import CAR
from openpilot.common.realtime import DT_CTRL
from openpilot.selfdrive.controls.lib.longcontrol import LongControl, LongCtrlState


class TestVoltLongitudinalTrial(unittest.TestCase):
  def params(self, candidate=CAR.CHEVROLET_VOLT):
    fp = {i: {} for i in range(7)}
    cp = CarInterface.get_params(candidate, fp, [], alpha_long=True, is_release=False, docs=False)
    sp = CarInterface.get_params_sp(cp, candidate, fp, [], alpha_long=True, is_release_sp=False, docs=False)
    return cp, sp

  def test_gain_schedule(self):
    cp, sp = self.params()
    self.assertEqual(list(cp.longitudinalTuning.kiBP), [5., 35.])
    control = LongControl(cp, sp)
    for speed, expected_i in [(0., 1.92), (5., 1.92), (20., 1.56), (35., 1.2), (40., 1.2)]:
      control.pid.speed = speed
      self.assertAlmostEqual(control.pid.k_p, 0.1)
      self.assertAlmostEqual(control.pid.k_i, expected_i, places=6)
      self.assertEqual(control.pid.k_d, 0.)

  def test_actual_pid_update_uses_p_and_keeps_feedforward(self):
    cp, sp = self.params()
    control = LongControl(cp, sp)
    cs = structs.CarState(vEgo=5., aEgo=-0.5)
    target = -1.
    output = control.update(True, cs, target, False, (-3.5, 2.))
    self.assertAlmostEqual(control.pid.p, -0.05)
    self.assertAlmostEqual(control.pid.i, -0.5 * 1.92 * DT_CTRL)
    self.assertEqual(control.pid.f, target)
    self.assertAlmostEqual(output, target - 0.05 - 0.5 * 1.92 * DT_CTRL)

  def test_stop_ramp_and_disengagement_are_unchanged(self):
    cp, sp = self.params()
    control = LongControl(cp, sp)
    cs = structs.CarState(vEgo=0.2, aEgo=0.)
    control.last_output_accel = 0.
    control.pid.i = -0.8
    output = control.update(True, cs, -0.5, True, (-3.5, 2.))
    self.assertEqual(control.long_control_state, LongCtrlState.stopping)
    self.assertAlmostEqual(output, -DT_CTRL)
    self.assertEqual(control.pid.i, 0.)
    self.assertEqual(control.pid.p, 0.)
    self.assertEqual(control.update(False, cs, -0.5, False, (-3.5, 2.)), 0.)
    self.assertEqual(control.long_control_state, LongCtrlState.off)

  def test_other_gm_platform_retains_original_gains(self):
    cp, sp = self.params(CAR.GMC_ACADIA)
    for actual, expected in zip(cp.longitudinalTuning.kiV, [2.4, 1.5], strict=True):
      self.assertAlmostEqual(actual, expected, places=6)
    control = LongControl(cp, sp)
    self.assertEqual(control.pid.k_p, 0.)
    self.assertAlmostEqual(control.pid.k_i, 2.4, places=6)

  def test_camera_volt_and_stock_long_do_not_enable_p(self):
    for camera, stock in [(True, False), (False, True)]:
      cp, sp = self.params()
      if camera:
        cp.networkLocation = structs.CarParams.NetworkLocation.fwdCamera
      if stock:
        cp.openpilotLongitudinalControl = False
      self.assertEqual(LongControl(cp, sp).pid.k_p, 0.)


if __name__ == '__main__':
  unittest.main()
