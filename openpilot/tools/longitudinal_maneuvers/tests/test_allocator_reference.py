import math
import unittest
from dataclasses import replace

import numpy as np

from opendbc.car.gm.tests.test_longitudinal import make_controller, make_state
from openpilot.tools.longitudinal_maneuvers.ascm_loop_reference import (
  Owner, RawAllocation, allocate_acceleration, publish_brake_acceleration,
)

ORDINARY_MOVING = dict(request_state=1, request_flags=0, correction=0, minimum_accel=-79,
                       standstill_status=False, special_timer=1, hold=False, previous_submode=2)


class TestAllocatorAgainstReference(unittest.TestCase):
  """The runtime allocator against the recovered 13afc0 ordinary moving branch.

  The thresholds are the runtime's (no OEM request-state selector or disturbance correction).
  Ownership from the previous owner's threshold and the signed, slewed brake request must agree.
  """

  def sweep(self, speed, minimum, corrected_milli):
    controller = make_controller()
    p = controller.params
    state = make_state(speed=speed, minimum=minimum)
    entry = p.regen_accel_available(minimum, speed) + float(np.interp(speed, p.BRAKE_ENTRY_MARGIN_BP, p.BRAKE_ENTRY_MARGIN_V))
    reference = RawAllocation(Owner.TORQUE, 0, 0, False)
    positive = 0
    for corrected in corrected_milli:
      _, brake = controller.stock_gas_brake(corrected / 1000., state, False)
      threshold = entry + (p.BRAKE_ENTRY_HYST if reference.owner == Owner.BRAKE else 0.)
      reference = allocate_acceleration(reference, corrected=corrected, threshold=math.ceil(threshold * 1000), **ORDINARY_MOVING)
      self.assertEqual(controller.brake_mode, reference.owner == Owner.BRAKE, corrected)
      self.assertLessEqual(abs(-brake * 10 - reference.brake_accel), 5, corrected)
      # 131440 writes the enveloped request back as the next cycle's prior demand (cal 0x5f6 floor).
      reference = replace(reference, brake_accel=publish_brake_acceleration(reference.brake_accel, -1500))
      positive = max(positive, -brake)
    return positive

  def test_creep_sweeps_and_steps_match(self):
    # Two full cycles: torque -> brake entry, signed retention through zero, release, re-entry.
    up = list(range(-400, 300, 10))
    for speed in (0.3, 0.67, 1.0):
      with self.subTest(speed=speed):
        self.assertGreaterEqual(self.sweep(speed, 100., (up[::-1] + up) * 2), 14)
    steps = [-180] * 5 + [100] * 10 + [-1000] * 10 + [150] * 15 + [-50] * 5
    self.assertGreaterEqual(self.sweep(0.67, 100., steps), 14)

  def test_entry_slew_is_a_known_difference(self):
    # With cal 0x806/0x808 = 0 the OEM takes the whole request on the brake-entry cycle. The
    # runtime allocator slews from zero instead; this predates signed requests and is unchanged.
    controller = make_controller()
    _, brake = controller.stock_gas_brake(-0.3, make_state(speed=0.67), False)
    reference = allocate_acceleration(RawAllocation(Owner.TORQUE, 0, 0, False), corrected=-300, threshold=-150, **ORDINARY_MOVING)
    self.assertEqual((brake, reference.brake_accel), (20, -300))


if __name__ == "__main__":
  unittest.main()
