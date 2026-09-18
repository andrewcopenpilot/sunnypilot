import unittest

from opendbc.car.gm.values import GMSafetyFlags
from opendbc.car.structs import CarParams
from opendbc.safety.tests.common import CANPackerSafety
from opendbc.safety.tests.libsafety import libsafety_py


class TestGmSignedBrakeSafety(unittest.TestCase):
  def setUp(self):
    self.safety = libsafety_py.libsafety
    self.packer = CANPackerSafety('gm_global_a_chassis')
    self.configure(GMSafetyFlags.EV | GMSafetyFlags.SIGNED_BRAKE_TEST)

  def configure(self, param, sp_param=0):
    self.safety.set_current_safety_param_sp(sp_param)
    self.safety.set_safety_hooks(CarParams.SafetyModel.gm, param)
    self.safety.init_tests()

  def tx(self, request, mode=0xA, bus=1):
    msg = self.packer.make_can_msg_safety('EBCMFrictionBrakeCmd', bus,
                                       {'FrictionBrakeCmd': request, 'FrictionBrakeMode': mode})
    return bool(self.safety.safety_tx_hook(msg))

  def test_entire_signed_range_and_modes_with_controls_on_and_off(self):
    for enabled in (False, True):
      self.safety.set_controls_allowed(enabled)
      for mode in range(16):
        for request in range(-2048, 2048):
          expected = request == 0 or (enabled and -400 <= request < 0) or (enabled and mode == 0xA and 0 < request <= 14)
          self.assertEqual(self.tx(request, mode), expected, (enabled, mode, request))

  def test_flag_and_hardware_scope(self):
    flag = GMSafetyFlags.SIGNED_BRAKE_TEST
    for param, sp_param, bus in ((0, 0, 1), (GMSafetyFlags.EV, 0, 1), (flag, 0, 1),
                                (flag | GMSafetyFlags.EV | GMSafetyFlags.HW_CAM | GMSafetyFlags.HW_CAM_LONG, 0, 0),
                                (flag | GMSafetyFlags.EV, 1, 1)):
      self.configure(param, sp_param)
      self.safety.set_controls_allowed(True)
      for request in (1, 7, 14, 15, 2047):
        self.assertFalse(self.tx(request, bus=bus))

  def test_gas_override_blocks_positive_requests(self):
    self.safety.set_controls_allowed(True)
    self.safety.set_gas_pressed_prev(True)
    for request in (1, 7, 14):
      self.assertFalse(self.tx(request))

  def test_next_drive_without_flag_resets_allowance(self):
    self.safety.set_controls_allowed(True)
    self.assertTrue(self.tx(14))
    self.configure(GMSafetyFlags.EV)
    self.safety.set_controls_allowed(True)
    self.assertFalse(self.tx(14))
    self.assertTrue(self.tx(-14))
