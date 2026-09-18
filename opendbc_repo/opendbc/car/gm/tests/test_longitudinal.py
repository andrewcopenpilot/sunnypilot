import unittest
from types import SimpleNamespace

from opendbc.can import CANParser
from opendbc.car import Bus, structs
from opendbc.car.gm import gmcan
from opendbc.car.gm.carcontroller import CarController
from opendbc.car.gm.values import CAR, DBC, CanBus


def make_controller(car=CAR.CHEVROLET_VOLT, network="gateway"):
  cp = structs.CarParams.new_message(carFingerprint=car, networkLocation=network,
                                    openpilotLongitudinalControl=True, autoResumeSng=True)
  return CarController(DBC[car], cp, structs.CarParamsSP())


def make_state(speed=0.5, minimum=100., valid=True, standstill=False, cruise_standstill=False):
  out = structs.CarState.new_message(vEgo=speed, standstill=standstill)
  out.cruiseState.standstill = cruise_standstill
  return SimpleNamespace(out=out, axle_torque_min=minimum, axle_torque_min_valid=valid,
                         lka_steering_cmd_counter=0, pt_lka_steering_cmd_counter=0, loopback_lka_steering_cmd_updated=False,
                         loopback_lka_steering_cmd_ts_nanos=0)


class TestVoltCreepTransitions(unittest.TestCase):
  def setUp(self):
    self.controller = make_controller()
    self.state = make_state()

  def enter_braking(self):
    self.controller.stock_gas_brake(-0.3, self.state, False)
    self.assertTrue(self.controller.brake_mode)

  def test_entry_and_retention_are_distinct(self):
    # A small positive request must not enter braking from torque mode.
    self.controller.stock_gas_brake(0.1, self.state, False)
    self.assertFalse(self.controller.brake_mode)
    self.enter_braking()
    # Reducing brake demand must not relinquish the path, even when it reaches zero.
    for accel in (-0.1, 0., 0.02):
      for _ in range(10):
        gas, brake = self.controller.stock_gas_brake(accel, self.state, False)
      self.assertTrue(self.controller.brake_mode)
      self.assertEqual(gas, -650.)
      self.assertEqual(brake, 8 if accel < 0. else 0)

  def test_small_positive_release_preserves_hysteresis(self):
    # Earlier release is limited to moving creep and does not immediately re-enter
    # braking when corrected demand fluctuates around the new release boundary.
    for speed in (0.4, 0.8, 1.0):
      with self.subTest(speed=speed):
        self.controller = make_controller()
        self.state = make_state(speed=speed)
        self.enter_braking()
        self.controller.stock_gas_brake(0.02, self.state, False)
        self.assertTrue(self.controller.brake_mode)
        self.controller.stock_gas_brake(0.06, self.state, False)
        self.assertFalse(self.controller.brake_mode)
        for accel in (0.04, 0.02, 0., -0.05, 0.04):
          self.controller.stock_gas_brake(accel, self.state, False)
          self.assertFalse(self.controller.brake_mode)
        self.enter_braking()

  def test_torque_handoff_initializes_once(self):
    self.enter_braking()
    gas, brake = self.controller.stock_gas_brake(0.4, self.state, False)
    self.assertFalse(self.controller.brake_mode)
    self.assertEqual((gas, brake), (100., 0))
    gas_next, _ = self.controller.stock_gas_brake(0.4, self.state, False)
    self.assertGreater(gas_next, gas)
    self.assertLessEqual(gas_next - gas, 40.)

  def test_invalid_minimum_uses_existing_slew(self):
    for minimum in (65536., float("nan")):
      with self.subTest(minimum=minimum):
        self.controller = make_controller()
        self.state = make_state()
        self.enter_braking()
        self.state.axle_torque_min = minimum
        self.state.axle_torque_min_valid = False
        gas, brake = self.controller.stock_gas_brake(0.4, self.state, False)
        self.assertFalse(self.controller.brake_mode)
        self.assertGreater(gas, -650.)
        self.assertLess(gas, 0.)
        self.assertEqual(brake, 0)

  def test_handoff_preserves_torque_limits(self):
    for minimum, expected in ((-10000., -650.), (10000., 1018.)):
      with self.subTest(minimum=minimum):
        self.controller = make_controller()
        self.state = make_state(minimum=minimum)
        self.controller.brake_mode = True
        self.controller.gas_cmd = -650.
        gas, _ = self.controller.stock_gas_brake(1., self.state, False)
        self.assertEqual(gas, expected)

  def test_excluded_states_keep_legacy_release(self):
    cases = [
      (make_controller(), make_state(speed=1.5)),
      (make_controller(), make_state(speed=4.)),
      (make_controller(), make_state(speed=-0.5)),
      (make_controller(), make_state(speed=0.)),
      (make_controller(), make_state(standstill=True)),
      (make_controller(), make_state(cruise_standstill=True)),
      (make_controller(network="fwdCamera"), make_state()),
      (make_controller(CAR.CHEVROLET_MALIBU), make_state()),
    ]
    for controller, state in cases:
      with self.subTest(car=controller.CP.carFingerprint, state=state, network=controller.CP.networkLocation):
        controller.brake_mode = True
        controller.gas_cmd = -650.
        gas, brake = controller.stock_gas_brake(0.1, state, False)
        self.assertFalse(controller.stock_creep_active)
        self.assertFalse(controller.brake_mode)
        self.assertLess(gas, 0.)  # legacy slew, not a positive minimum-torque seed
        self.assertEqual(brake, 0)

  def test_creep_brake_scale_blends_out_with_speed(self):
    for speed, expected in ((0.4, 24), (0.8, 24), (1.0, 24), (1.25, 27), (1.5, 30), (4., 30)):
      with self.subTest(speed=speed):
        controller = make_controller()
        state = make_state(speed=speed)
        for _ in range(10):
          gas, brake = controller.stock_gas_brake(-0.3, state, False)
        self.assertEqual((gas, brake), (-650., expected))
        self.assertTrue(controller.brake_mode)

  def test_excluded_states_keep_unscaled_brake_demand(self):
    disabled = make_controller()
    disabled.params.STOCK_CREEP_TRANSITIONS = False
    unscaled = make_controller()
    unscaled.params.CREEP_BRAKE_SCALE = 1.
    cases = [
      (make_controller(), make_state(speed=0.)),
      (make_controller(), make_state(speed=-0.5)),
      (make_controller(), make_state(standstill=True)),
      (make_controller(), make_state(cruise_standstill=True)),
      (make_controller(network="fwdCamera"), make_state()),
      (make_controller(CAR.CHEVROLET_MALIBU), make_state()),
      (disabled, make_state()),
      (unscaled, make_state()),
    ]
    for controller, state in cases:
      with self.subTest(car=controller.CP.carFingerprint, state=state):
        for _ in range(10):
          _, brake = controller.stock_gas_brake(-0.3, state, False)
        self.assertEqual(brake, 30)

  def test_scaled_braking_preserves_slew_and_maximum_authority(self):
    previous = 0.
    for _ in range(20):
      _, brake = self.controller.stock_gas_brake(-4., self.state, False)
      self.assertLessEqual(abs(self.controller.brake_accel_cmd - previous), 0.2 + 1e-9)
      previous = self.controller.brake_accel_cmd
    self.assertEqual(brake, 150)  # Existing creep deceleration cap remains reachable.
    for _ in range(20):
      self.controller.stock_gas_brake(0.02, self.state, False)
      self.assertLessEqual(abs(self.controller.brake_accel_cmd - previous), 0.2 + 1e-9)
      previous = self.controller.brake_accel_cmd
    self.assertEqual(self.controller.brake_accel_cmd, 0.)
    self.assertTrue(self.controller.brake_mode)

  def test_stopping_keeps_existing_hold_demand(self):
    for _ in range(20):
      gas, brake = self.controller.stock_gas_brake(-2., self.state, True)
    self.assertFalse(self.controller.stock_creep_active)
    self.assertTrue(self.controller.brake_mode)
    self.assertEqual((gas, brake), (-650., 150))

  def test_baseline_switch(self):
    self.controller.params.STOCK_CREEP_TRANSITIONS = False
    self.enter_braking()
    self.controller.stock_gas_brake(-0.09, self.state, False)
    self.assertFalse(self.controller.brake_mode)
    self.assertFalse(self.controller.stock_creep_active)


class TestVoltCreepCAN(unittest.TestCase):
  def setUp(self):
    self.controller = make_controller()
    self.state = make_state()
    self.control = structs.CarControl.new_message(enabled=True, longActive=True)
    self.control.actuators.longControlState = "pid"
    self.parser = CANParser(DBC[CAR.CHEVROLET_VOLT][Bus.chassis], [("EBCMFrictionBrakeCmd", 25)], CanBus.OBSTACLE)
    self.tick = 0

  def update(self, accel):
    self.control.actuators.accel = accel
    self.controller.frame = self.tick * 4
    nanos = 1_000_000_000 + self.tick * 40_000_000
    _, messages = self.controller.update(self.control.as_reader(), None, self.state, nanos)
    self.assertIn(0x315, self.parser.update([[nanos, messages]]))
    self.tick += 1
    brake_message = next(message for message in messages if message[0] == 0x315)
    mode = int(self.parser.vl["EBCMFrictionBrakeCmd"]["FrictionBrakeMode"])
    demand = self.parser.vl["EBCMFrictionBrakeCmd"]["FrictionBrakeCmd"]
    # Check the actual packet's checksum, including the independently selected active bit.
    data = brake_message[1]
    raw_brake = ((data[0] & 0xf) << 8) | data[1]
    idx = data[4] & 3
    self.assertEqual(int.from_bytes(data[2:4], "big"), (0x10000 - (mode << 12) - raw_brake - idx) & 0xffff)
    return mode, demand

  def test_scaled_demand_is_sent_on_can(self):
    for _ in range(10):
      mode, demand = self.update(-0.3)
    self.assertEqual((mode, demand), (0xa, -24.))
    self.assertEqual(self.controller.apply_gas, -650.)

  def test_zero_demand_retains_active_path_until_torque_handoff(self):
    self.assertEqual(self.update(-0.3)[0], 0xa)
    for _ in range(10):
      mode, demand = self.update(0.02)
    self.assertEqual((mode, demand), (0xa, 0.))
    self.assertEqual(self.update(0.06), (0x1, 0.))
    self.assertEqual(self.controller.apply_gas, 100.)

  def test_stop_intent_can_clear_below_near_stop_speed(self):
    self.control.actuators.longControlState = "stopping"
    self.assertEqual(self.update(-0.3)[0], 0xb)
    self.control.actuators.longControlState = "pid"
    # Resume ordinary braking without requiring speed to rise above 1.5 m/s.
    self.assertEqual(self.update(-0.3)[0], 0xa)
    self.assertEqual(self.update(0.06), (0x1, 0.))
    self.assertEqual(self.controller.apply_gas, 100.)

  def test_repeated_creep_release_and_reentry_has_no_mode_chatter(self):
    for speed in (0.2, 0.5, 1.):
      self.state.out.vEgo = speed
      for _ in range(3):
        for _ in range(20):
          self.assertEqual(self.update(-0.3)[0], 0xa)
        for _ in range(20):
          self.assertEqual(self.update(0.02)[0], 0xa)
        self.assertEqual(self.update(0.06), (0x1, 0.))
        for accel in (0.04, 0.02, 0., -0.05, 0.04):
          self.assertEqual(self.update(accel), (0x1, 0.))

  def test_other_platforms_and_baseline_keep_speed_based_near_stop(self):
    for controller in (make_controller(CAR.CHEVROLET_MALIBU), make_controller()):
      if controller.CP.carFingerprint == CAR.CHEVROLET_VOLT and controller.CP.networkLocation == structs.CarParams.NetworkLocation.gateway:
        controller.params.STOCK_CREEP_TRANSITIONS = False
      self.controller = controller
      self.assertEqual(self.update(-0.3)[0], 0xb)

  def test_disengagement_clears_retained_path(self):
    self.update(-0.3)
    self.update(0.02)
    # CC.enabled can remain true for lateral control while longitudinal is inactive.
    self.control.longActive = False
    self.assertEqual(self.update(0.), (0x1, 0.))
    self.assertFalse(self.controller.brake_mode)
    self.assertFalse(self.controller.stock_creep_active)

  def test_stopping_still_sends_full_stop_mode(self):
    self.control.actuators.longControlState = "stopping"
    self.state.out.standstill = True
    self.state.out.cruiseState.standstill = True
    for _ in range(20):
      mode, demand = self.update(-2.)
    self.assertEqual((mode, demand), (0xd, -150.))

  def test_disabled_helper_cannot_force_active_zero_demand(self):
    message = gmcan.create_friction_brake_command(self.controller.packer_ch, CanBus.OBSTACLE, 0, 0,
                                                 False, True, False, self.controller.CP, brake_active=True)
    self.assertEqual(message[1][0] >> 4, 0x1)


if __name__ == "__main__":
  unittest.main()
