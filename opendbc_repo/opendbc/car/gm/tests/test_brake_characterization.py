import unittest
from types import SimpleNamespace

from opendbc.car import structs
from opendbc.car.gm.brake_characterization import brake_test_enabled, forward_brake_test
from opendbc.car.gm.tests import test_longitudinal as fixtures
from opendbc.car.gm.values import LongOwner, CAR


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
    for speed in (0.41, 1.0, 1.75):
      with self.subTest(speed=speed):
        self.setUp()
        self.state.out.vEgo = speed
        for command in range(-200, 21):
          self.assertEqual(self.update(command), (0xa, -float(command)))
          self.assertEqual(self.controller.apply_gas, -650.)
        self.assertEqual(self.update(0.), (0xa, 0.))

  def test_direct_release_holds_keep_mode_and_fixed_torque(self):
    for release in (0., 5., 8.):
      with self.subTest(release=release):
        self.setUp()
        self.state.out.vEgo = 0.8
        for _ in range(100):  # Four seconds of application at 25 Hz.
          self.assertEqual(self.update(12.), (0xa, -12.))
        for _ in range(200):  # Eight-second release hold, including zero demand.
          self.assertEqual(self.update(release), (0xa, -release))
          self.assertEqual(self.controller.apply_gas, -650.)
          self.assertFalse(self.controller.brake_test_failed)

  def test_signed_steps_round_trip_through_controller_dbc_and_checksum(self):
    for signed in (-20., 0., 3., 0., 6., 0., 10., 0., 15., 0., 20., 0., 200., 0.):
      for _ in range(10):
        self.assertEqual(self.update(-signed), (0xa, signed))
        self.assertEqual(self.controller.apply_gas, -650.)
        self.assertFalse(self.controller.brake_test_failed)

  def test_positive_signed_request_cannot_use_inactive_release(self):
    self.update(14.)
    self.control.brakeTestRelease = True
    self.update(-14.)
    self.assertTrue(self.controller.brake_test_failed)

  def test_zero_only_release_uses_inactive_mode_and_retains_torque_request(self):
    self.assertEqual(self.update(12.), (0xa, -12.))
    for _ in range(50):
      self.assertEqual(self.update(0.), (0xa, 0.))
    self.control.brakeTestRelease = True
    for _ in range(200):
      self.assertEqual(self.update(0.), (0x1, 0.))
      self.assertEqual(self.controller.apply_gas, -650.)
      self.assertEqual(self.controller.owner, LongOwner.POWERTRAIN)
    self.control.brakeTestRelease = False
    self.assertEqual(self.update(0.), (0xa, 0.))

  def test_inactive_brake_hold_retains_all_validation_and_fault_latching(self):
    for case in ('nonzero', 'fractional', 'stale', 'slow', 'invalid_can', 'standstill'):
      with self.subTest(case=case):
        self.setUp()
        self.update(12.)
        self.control.brakeTestRelease = True
        self.assertEqual(self.update(0.), (0x1, 0.))
        command = 10. if case == 'nonzero' else 0.1 if case == 'fractional' else 0.
        if case == 'stale':
          self.control.brakeTestMonoTime = 1
        if case == 'slow':
          self.state.out.vEgo = 0.39
        if case == 'invalid_can':
          self.state.out.canValid = False
        if case == 'standstill':
          self.state.out.standstill = True
        self.update(command, fresh=case != 'stale')
        self.assertTrue(self.controller.brake_test_failed)
        self.state.out.vEgo = 1.
        self.state.out.canValid = True
        self.state.out.standstill = False
        for _ in range(10):
          mode, demand = self.update(0.)
        # a latched abort keeps requesting the -2.0 m/s^2 stop through the brake controller
        self.assertEqual((mode, demand), (0xa, -200.))

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
          command = {'nan': float('nan'), 'negative': -201., 'large': 21.}[case]
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
          mode, demand = self.update(command, fresh=fresh)
        # An abort requests a -2.0 m/s^2 stop through the brake controller: 0xA, or 0xD once cruise reports standstill.
        self.assertEqual(mode, 0xd if case == 'cruise_stop' else 0xa)
        self.assertEqual(demand, -200.)

  def test_fault_stays_latched_when_fresh_commands_return(self):
    self.update(2.)
    self.control.brakeTestMonoTime = 1
    self.update(2., fresh=False)
    for _ in range(10):
      _, demand = self.update(2.)
    self.assertEqual(demand, -200.)
    self.assertTrue(self.controller.brake_test_failed)
    self.controller.frame = self.tick * 4
    output, _ = self.controller.update(self.control.as_reader(), None, self.state, 1_000_000_000 + self.tick * 40_000_000)
    self.assertEqual(output.longControlState, structs.CarControl.Actuators.LongControlState.stopping)
    self.tick += 1
    self.control.brakeTestActive = False
    for _ in range(10):
      _, demand = self.update(2.)
    self.assertFalse(self.controller.brake_test_failed)
    self.assertEqual(demand, -30.)

  def test_pedals_and_disengagement_cancel_direct_output(self):
    for condition in ('gas', 'brake', 'inactive'):
      self.setUp()
      self.update(20.)
      if condition == 'inactive':
        self.control.longActive = False
      else:
        setattr(self.state.out, condition + 'Pressed', True)
      self.assertEqual(self.update(20.), (0x1, 0.))

  def test_requires_authorized_vehicle_and_mode(self):
    # Unsupported vehicles keep their normal allocation (the Malibu uses the lookup tables: 21 counts at -0.3 m/s^2).
    for controller, expected in ((fixtures.make_controller(), 30.),
                                 (fixtures.make_controller(CAR.CHEVROLET_MALIBU), 21.)):
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
      mode, demand = self.update(3.)
    self.assertEqual((mode, demand), (0xa, -30.))


class TestBrakeTestForwarding(unittest.TestCase):
  def test_authorization_freshness_and_serialization(self):
    controller = fixtures.make_controller()
    cs = fixtures.make_state().out
    cs.canValid = True
    cc = structs.CarControl.new_message(enabled=True, longActive=True)
    plan = SimpleNamespace(brakeTestActive=True, brakeTestCommand=3.5, brakeTestRelease=False, shouldStop=False)
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
    self.assertFalse(cc.brakeTestRelease)

  def test_signed_forwarding_round_trip_and_bounds(self):
    controller = fixtures.make_controller()
    controller.CP_SP.longitudinalManeuverMode = True
    cs = fixtures.make_state().out
    cs.canValid = True
    cc = structs.CarControl.new_message(enabled=True, longActive=True)
    plan = SimpleNamespace(brakeTestActive=True, brakeTestCommand=-14., brakeTestRelease=False, shouldStop=False)
    for command, valid in ((-200., True), (-200.01, False), (20., True), (20.01, False), (float('inf'), False)):
      plan.brakeTestCommand = command
      self.assertEqual(forward_brake_test(cc, controller.CP, controller.CP_SP, cs, plan,
                                          1_000_000_000, 1_100_000_000, True), valid)
      if valid:
        cc.clear_write_flag()
        with structs.CarControl.from_bytes(cc.to_bytes()) as decoded:
          self.assertEqual(decoded.brakeTestCommand, command)

  def test_release_forwarding_requires_zero_and_preserves_timestamp(self):
    controller = fixtures.make_controller()
    controller.CP_SP.longitudinalManeuverMode = True
    cs = fixtures.make_state().out
    cs.canValid = True
    cc = structs.CarControl.new_message(enabled=True, longActive=True)
    plan = SimpleNamespace(brakeTestActive=True, brakeTestCommand=0., brakeTestRelease=True, shouldStop=False)
    args = (cc, controller.CP, controller.CP_SP, cs, plan)
    self.assertTrue(forward_brake_test(*args, 1_000_000_000, 1_100_000_000, True))
    with structs.CarControl.from_bytes(cc.to_bytes()) as decoded:
      self.assertTrue(decoded.brakeTestActive)
      self.assertTrue(decoded.brakeTestRelease)
      self.assertEqual(decoded.brakeTestCommand, 0.)
      self.assertEqual(decoded.brakeTestMonoTime, 1_000_000_000)
    plan.brakeTestCommand = 0.1  # Must be exactly zero, even if CAN would round to zero.
    self.assertFalse(forward_brake_test(*args, 1_000_000_000, 1_100_000_000, True))
    plan.brakeTestCommand = 0.
    self.assertFalse(forward_brake_test(*args, 1_000_000_000, 1_300_000_000, True))
    plan.brakeTestActive = False
    self.assertIsNone(forward_brake_test(*args, 1_000_000_000, 1_100_000_000, True))
    self.assertFalse(cc.brakeTestRelease)
