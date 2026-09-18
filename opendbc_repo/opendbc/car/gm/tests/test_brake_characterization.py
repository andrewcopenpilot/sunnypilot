import unittest
from types import SimpleNamespace

from opendbc.car import structs
from opendbc.car.gm.brake_characterization import brake_test_enabled, forward_brake_test
from opendbc.car.gm.tests import test_longitudinal as fixtures
from opendbc.car.gm.values import CAR


class TestBrakeCharacterizationCAN(unittest.TestCase):
  def setUp(self):
    fixtures.TestVoltCreepCAN.setUp(self)
    self.controller.CP_SP.longitudinalManeuverMode = True
    self.state.out.canValid = True
    self.control.brakeTestActive = True
    self.control.brakeTestMonoTime = 1_000_000_000

  def update(self, command, fresh=True):
    self.control.brakeTestCommand = command
    if fresh:
      self.control.brakeTestMonoTime = 1_000_000_000 + self.tick * 40_000_000
    return fixtures.TestVoltCreepCAN.update(self, -0.3)

  def test_every_integer_demand_bypasses_creep_scaling_and_keeps_mode(self):
    for command in range(13):
      self.assertEqual(self.update(command), (0xb, -float(command)))
      self.assertEqual(self.controller.apply_gas, -650.)
    self.assertEqual(self.update(0.), (0xb, 0.))

  def test_stale_invalid_and_out_of_bounds_commands_stop(self):
    for case in ('stale', 'future', 'nan', 'negative', 'large', 'slow', 'fast', 'standstill', 'cruise_stop', 'invalid_can', 'stopping'):
      with self.subTest(case=case):
        self.setUp()
        self.update(2.)
        command = 2.
        fresh = True
        if case == 'stale':
          self.control.brakeTestMonoTime = 1
          fresh = False
        elif case == 'future':
          self.control.brakeTestMonoTime = 9_000_000_000
          fresh = False
        elif case in ('nan', 'negative', 'large'):
          command = {'nan': float('nan'), 'negative': -1., 'large': 13.}[case]
        elif case in ('slow', 'fast'):
          self.state.out.vEgo = {'slow': 0.39, 'fast': 2.}[case]
        elif case == 'standstill':
          self.state.out.standstill = True
        elif case == 'invalid_can':
          self.state.out.canValid = False
        elif case == 'cruise_stop':
          self.state.out.cruiseState.standstill = True
        else:
          self.control.actuators.longControlState = 'stopping'
        for _ in range(10):
          _, demand = self.update(command, fresh=fresh)
        self.assertEqual(demand, -175. if case == 'fast' else -150.)
        self.assertFalse(self.controller.stock_creep_active)

  def test_fault_stays_latched_when_fresh_commands_return(self):
    self.update(2.)
    self.control.brakeTestMonoTime = 1
    self.update(2., fresh=False)
    for _ in range(10):
      _, demand = self.update(2.)
    self.assertEqual(demand, -150.)
    self.assertTrue(self.controller.brake_test_failed)
    self.controller.frame = self.tick * 4
    output, _ = self.controller.update(self.control.as_reader(), None, self.state, 1_000_000_000 + self.tick * 40_000_000)
    self.assertEqual(output.longControlState, structs.CarControl.Actuators.LongControlState.stopping)
    self.tick += 1
    self.control.brakeTestActive = False
    for _ in range(10):
      _, demand = self.update(2.)
    self.assertFalse(self.controller.brake_test_failed)
    self.assertEqual(demand, -24.)

  def test_pedals_and_disengagement_cancel_direct_output(self):
    for condition in ('gas', 'brake', 'inactive'):
      self.setUp()
      self.update(12.)
      if condition == 'inactive':
        self.control.longActive = False
      else:
        setattr(self.state.out, condition + 'Pressed', True)
      self.assertEqual(self.update(12.), (0x1, 0.))

  def test_requires_authorized_vehicle_and_mode(self):
    for controller, expected in ((fixtures.make_controller(), 24.),
                                 (fixtures.make_controller(CAR.CHEVROLET_MALIBU), 30.)):
      self.setUp()
      self.controller = controller
      # Unsupported vehicles remain unsupported even with maneuver mode selected.
      if controller.CP.carFingerprint != CAR.CHEVROLET_VOLT or controller.CP.networkLocation != structs.CarParams.NetworkLocation.gateway:
        controller.CP_SP.longitudinalManeuverMode = True
      for _ in range(10):
        _, demand = self.update(1.)
      self.assertEqual(demand, -expected)

  def test_camera_network_is_not_authorized(self):
    controller = fixtures.make_controller(network='fwdCamera')
    controller.CP_SP.longitudinalManeuverMode = True
    self.assertFalse(brake_test_enabled(controller.CP, controller.CP_SP))

  def test_inactive_request_returns_to_normal_mapping(self):
    self.update(3.)
    self.control.brakeTestActive = False
    for _ in range(10):
      _, demand = self.update(3.)
    self.assertEqual(demand, -24.)


class TestBrakeTestForwarding(unittest.TestCase):
  def test_authorization_freshness_and_serialization(self):
    controller = fixtures.make_controller()
    cs = fixtures.make_state().out
    cs.canValid = True
    cc = structs.CarControl.new_message(enabled=True, longActive=True)
    plan = SimpleNamespace(brakeTestActive=True, brakeTestCommand=3.5, shouldStop=False)
    args = (cc, controller.CP, controller.CP_SP, cs, plan)
    self.assertIsNone(forward_brake_test(*args, 1_000_000_000, 1_100_000_000, True))
    controller.CP_SP.longitudinalManeuverMode = True
    self.assertTrue(forward_brake_test(*args, 1_000_000_000, 1_100_000_000, True))
    with structs.CarControl.from_bytes(cc.to_bytes()) as decoded:
      self.assertTrue(decoded.brakeTestActive)
      self.assertEqual(decoded.brakeTestCommand, 3.5)
      self.assertEqual(decoded.brakeTestMonoTime, 1_000_000_000)
    self.assertFalse(forward_brake_test(*args, 1_000_000_000, 1_300_000_000, True))
    self.assertFalse(forward_brake_test(*args, 1_000_000_000, 1_100_000_000, False))
    self.assertEqual(cc.brakeTestMonoTime, 0)
    plan.shouldStop = True
    self.assertFalse(forward_brake_test(*args, 1_000_000_000, 1_100_000_000, True))
    cc.longActive = False
    self.assertIsNone(forward_brake_test(*args, 1_000_000_000, 1_100_000_000, True))
    self.assertFalse(cc.brakeTestActive)
