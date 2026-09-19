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


class TestStockGasBrake(unittest.TestCase):
  def setUp(self):
    self.controller = make_controller()
    self.state = make_state()

  def hold(self, accel, frames=10, stopping=False):
    for _ in range(frames):
      result = self.controller.stock_gas_brake(accel, self.state, stopping)
    return result

  def test_signed_request_between_entry_and_release(self):
    # A small positive request does not enter braking from torque mode.
    self.hold(0.1)
    self.assertFalse(self.controller.brake_mode)
    # Once braking, the request follows the corrected acceleration through zero.
    for accel, expected in ((-0.3, 30), (-0.1, 10), (0., 0), (0.02, -2), (0.15, -15), (-0.05, 5)):
      self.assertEqual(self.hold(accel), (-650., expected))
      self.assertTrue(self.controller.brake_mode)

  def test_release_and_reentry_hysteresis(self):
    for speed in (0.4, 1.0, 4., 15.):
      with self.subTest(speed=speed):
        self.controller = make_controller()
        self.state = make_state(speed=speed, minimum=100. if speed < 2. else -650.)
        floor = self.controller.params.regen_accel_available(self.state.axle_torque_min, speed)
        self.hold(floor - 0.5)
        self.assertTrue(self.controller.brake_mode)
        self.hold(floor + 0.05)
        self.assertTrue(self.controller.brake_mode)
        gas, brake = self.hold(floor + 0.3, frames=1)
        self.assertFalse(self.controller.brake_mode)
        self.assertEqual(brake, 0)
        self.assertGreater(gas, -650.)  # existing torque slew out of the brake-mode request
        # No chatter: falling back inside the band does not re-enter braking.
        for accel in (floor + 0.1, floor, floor - 0.05):
          self.hold(accel, frames=1)
          self.assertFalse(self.controller.brake_mode)

  def test_stopping_and_standstill_stay_unsigned(self):
    for state, stopping in ((self.state, True), (make_state(standstill=True), False), (make_state(cruise_standstill=True), False)):
      self.controller = make_controller()
      self.state = make_state()
      self.hold(-0.3)
      self.assertEqual(self.hold(0.15)[1], -15)
      # One slew step covers the positive band, so the first such request is already non-positive.
      _, brake = self.controller.stock_gas_brake(0.1, state, stopping)
      self.assertGreaterEqual(brake, 0)

  def test_slew_and_maximum_authority(self):
    previous = 0.
    for accel, expected in ((-4., 150), (0.1, -10)):  # cal 0x5f6 low-speed deceleration floor
      for _ in range(20):
        _, brake = self.controller.stock_gas_brake(accel, self.state, False)
        self.assertLessEqual(abs(self.controller.brake_accel_cmd - previous), 0.2 + 1e-9)
        previous = self.controller.brake_accel_cmd
      self.assertEqual(brake, expected)

  def test_stopping_keeps_existing_hold_demand(self):
    self.assertEqual(self.hold(-2., frames=20, stopping=True), (-650., 150))
    self.assertTrue(self.controller.brake_mode)


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

  def test_signed_demand_holds_0xa_until_release(self):
    for accel, expected in ((-0.3, -30.), (0., 0.), (0.02, 2.), (0.15, 15.), (-0.05, -5.)):
      for _ in range(10):
        mode, demand = self.update(accel)
        self.assertEqual(mode, 0xa)
      self.assertEqual(demand, expected)
    self.assertEqual(self.controller.apply_gas, -650.)
    self.assertEqual(self.update(0.3), (0x1, 0.))
    for accel in (0.1, 0., -0.05, 0.1):
      self.assertEqual(self.update(accel), (0x1, 0.))

  def test_stop_intent_drops_positive_request_and_can_clear(self):
    self.update(-0.3)
    for _ in range(5):
      self.assertEqual(self.update(0.15)[0], 0xa)
    self.control.actuators.longControlState = "stopping"
    self.assertEqual(self.update(-0.3), (0xb, -5.))  # one slew step from +0.15
    self.control.actuators.longControlState = "pid"
    # Resume ordinary braking without requiring speed to rise above 1.5 m/s.
    self.assertEqual(self.update(-0.3)[0], 0xa)

  def test_other_platforms_keep_speed_based_near_stop(self):
    self.controller = make_controller(CAR.CHEVROLET_MALIBU)
    self.assertEqual(self.update(-0.3)[0], 0xb)

  def test_disengagement_clears_retained_path(self):
    self.update(-0.3)
    for _ in range(3):
      mode, demand = self.update(0.1)
    self.assertEqual((mode, demand), (0xa, 10.))
    # CC.enabled can remain true for lateral control while longitudinal is inactive.
    self.control.longActive = False
    self.assertEqual(self.update(0.), (0x1, 0.))
    self.assertFalse(self.controller.brake_mode)

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
