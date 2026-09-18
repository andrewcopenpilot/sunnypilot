"""Bounds and command forwarding for Volt brake characterization in maneuver mode."""
import math

from opendbc.car import structs
from opendbc.car.gm.values import CAR

BRAKE_TEST_MIN = -14.  # legacy brake-positive convention: up to +14 signed CAN counts
BRAKE_TEST_MAX = 20.  # EBCM counts; characterization ceiling, not the controller maximum
BRAKE_TEST_MIN_SPEED = 0.4  # m/s
BRAKE_TEST_MAX_SPEED = 2.0  # m/s
BRAKE_TEST_MAX_AGE_NS = 250_000_000


def brake_test_enabled(CP, CP_SP):
  return (CP_SP.longitudinalManeuverMode and CP.openpilotLongitudinalControl and
          CP.carFingerprint == CAR.CHEVROLET_VOLT and CP.networkLocation == structs.CarParams.NetworkLocation.gateway)


def brake_test_valid(command, timestamp, now_nanos, CS, release=False):
  return (math.isfinite(command) and BRAKE_TEST_MIN <= command <= BRAKE_TEST_MAX and
          (not release or command == 0.) and
          timestamp > 0 and 0 <= now_nanos - timestamp <= BRAKE_TEST_MAX_AGE_NS and
          CS.canValid and BRAKE_TEST_MIN_SPEED < CS.vEgo < BRAKE_TEST_MAX_SPEED and
          not (CS.standstill or CS.cruiseState.standstill or CS.gasPressed or CS.brakePressed))


def forward_brake_test(CC, CP, CP_SP, CS, plan, plan_time, now_nanos, plan_valid):
  """Return None for normal control, True for a valid test, False for a test needing a stop."""
  CC.brakeTestActive = bool(brake_test_enabled(CP, CP_SP) and CC.enabled and CC.longActive and plan.brakeTestActive)
  CC.brakeTestCommand = 0.
  CC.brakeTestRelease = False
  CC.brakeTestMonoTime = 0
  if not CC.brakeTestActive:
    return None
  CC.brakeTestCommand = plan.brakeTestCommand
  CC.brakeTestRelease = plan.brakeTestRelease
  CC.brakeTestMonoTime = plan_time if plan_valid else 0
  return brake_test_valid(CC.brakeTestCommand, CC.brakeTestMonoTime, now_nanos, CS, CC.brakeTestRelease) and not plan.shouldStop
