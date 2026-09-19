"""Readable excerpts of the stock ASCM longitudinal controller.

Start with read_one_cycle() and ASCM_LOOP_REFERENCE.md.
CONFIRMED = traced arithmetic/order. INFERRED = interpretation of that evidence.
UNKNOWN = an unresolved meaning, policy or runtime input.
OMITTED = firmware exists, but this excerpt does not translate that branch.

This is a study document expressed as Python, not a replacement controller or
complete simulation. No CAN, CarState, vehicle control, or maneuver integration.
Firmware/calibrations: MPU1 84876565, ACC 23366550, VSC 84059606,
DYN 84059607, VCFG 23366555. See ASCM_DYNAMICS_AND_OUTPUTS.md for latest evidence.
SI explanatory excerpts and raw integer translations coexist; units are stated
at each boundary. Integer helpers preserve truncation but not machine overflow;
sensor excerpts do not reproduce float32 rounding. Names are ours, not OEM names.
"""

from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum
from typing import Protocol


class Owner(IntEnum):
  INACTIVE = 0
  TORQUE = 1
  BRAKE = 2


class NotTranscribed(NotImplementedError):
  """An excerpt reached a branch that requires the original firmware."""


class FirmwareStages(Protocol):
  """Interface for reading the call order, NOT an implemented firmware backend.

  Each stage reads/writes shared state. In particular, feedback sees the mode
  chosen on previous cycles; allocation then chooses this cycle's mode.
  """

  def prepare_vehicle_state_and_dynamics(self) -> None: ...
  def reload_vehicle_model_calibration(self) -> None: ...
  def prepare_torque_capability(self) -> None: ...
  def select_acceleration_request(self) -> None: ...
  def update_acceleration_feedback(self) -> None: ...
  def select_actuator_and_brake_submode(self) -> None: ...
  def convert_and_shape_powertrain_torque(self) -> None: ...
  def update_auxiliary_torque_and_hold_state(self) -> None: ...
  def update_adaptation(self) -> None: ...
  def record_response_history(self) -> None: ...
  def shape_and_publish_commands(self) -> None: ...


def read_one_cycle(stock: FirmwareStages) -> None:
  """CONFIRMED sequencing; roughly 40 ms per cycle in this firmware.

  The first call summarizes preparation outside 139d80, including 1344b0.
  The middle stages follow FUN_00139d80 exactly. Model reload and final command
  publication belong to its caller 131440. Detailed excerpts appear below.
  The Protocol makes omitted stages explicit; no guessed defaults implement them.
  """
  # Upstream boundary: sensor estimates, candidate requests, object flags and
  # supervisor state. UNKNOWN: several physical enums and exact fault-to-exit
  # timing. The recovered twelve-state supervisor is not translated here.
  # Sensor conditioning has its own faster schedule: read_one_dynamics_tick().
  stock.prepare_vehicle_state_and_dynamics()     # includes 1344b0 classification

  # 131440 -> 139e50 reloads the model EVERY cycle. Later mass adaptation does
  # not survive this reload, although its residual/counter states can survive.
  stock.reload_vehicle_model_calibration()
  stock.prepare_torque_capability()             # 139ce0: actual/min/max -> accel
  stock.select_acceleration_request()           # 13ade0: uses PREVIOUS I
  stock.update_acceleration_feedback()          # 13a5d0: old owner/hold, delayed PI
  stock.select_actuator_and_brake_submode()      # 13afc0: NEW owner, still OLD hold

  # 13a360 adds class +1 rolling resistance AFTER capability computation.
  # Ratio output is computed before primary transition seeding/filter/slew.
  stock.convert_and_shape_powertrain_torque()
  # 13a180 updates hold for NEXT allocation, plus flag23/timer hysteresis.
  # No auxiliary/ratio actuator publication was found; do not discard the
  # routine's hold/flag side effects on that account. A conditional raw memory
  # transfer includes these numbers (stored record 8 == 0x5a; default disabled).
  # UNKNOWN: transfer endpoint and a particular module's stored enable value.
  stock.update_auxiliary_torque_and_hold_state()
  stock.update_adaptation()                     # 13b6c0; OMITTED Python algorithm
  # 13b910 commits after >=100 ms: 120 ms on the 40 ms schedule, although its
  # lookup assumes 100 ms. UNKNOWN: full downstream role of its response score.
  stock.record_response_history()               # OMITTED Python history algorithm
  # 131440 reshapes brake demand and writes it back for the next cycle; enable
  # and submode are separate. UNKNOWN: how the receiving EBCM turns that request
  # into hydraulic pressure. This reference ends at ASCM command publication.
  stock.shape_and_publish_commands()


@dataclass(frozen=True)
class UnidentifiedDynamicsReading:
  value: float
  validity_bit: bool


def decode_dynamics_0x140(payload: bytes) -> UnidentifiedDynamicsReading:
  """CONFIRMED 81410 -> 79b00/772d0 -> 484c0 -> c32d0.

  This is the EIGHT-byte receive entry, not the three-byte turn-signal message.
  INFERRED from consumers: longitudinal acceleration domain. The conditioned
  branch also feeds the sensor/wheel residual c1250; see ASCM_DYNAMICS_AND_OUTPUTS.md.
  UNKNOWN: sending ECU, physical sign convention and complete fault policy.
  We preserve the validity bit without interpreting True as 'valid'.
  """
  if len(payload) != 8:
    raise ValueError("The dynamics receive entry has eight bytes")
  raw = int.from_bytes(payload[4:6], "big") & 0xFFF
  signed = raw - 0x1000 if raw & 0x800 else raw
  return UnidentifiedDynamicsReading(signed / 64.0, bool(payload[2] & 0x20))


class DynamicsTaskStages(Protocol):
  """The separate 10 ms task; its scheduling is part of the reference.

  OMITTED: a concrete backend for the full sensor/wheel processors and their
  fault state machines. Numeric excerpts below accept those boundary decisions.
  """

  def condition_sensor_using_previous_wheel_and_residual(self) -> None: ...
  def update_wheel_acceleration_channels(self) -> None: ...
  def update_sensor_wheel_residual(self) -> None: ...


def read_one_dynamics_tick(stock: DynamicsTaskStages) -> None:
  """bcfc0: calls bd074, bd09e, bd0f2, normally every 10 ms.

  The sensor processor sees PREVIOUS wheel/residual publications. The residual
  processor then sees NEW sensor/wheel publications. The 40 ms ACC loop samples
  these results; calling all three only once per ACC cycle changes transients.
  UNKNOWN: whole-system task phase/jitter relative to a real recorded drive.
  """
  stock.condition_sensor_using_previous_wheel_and_residual()
  stock.update_wheel_acceleration_channels()
  stock.update_sensor_wheel_residual()


@dataclass(frozen=True)
class SensorChannelMemory:
  value: float
  previously_accepted: bool


def condition_dynamics_sensor(
  sample: float, old: SensorChannelMemory, accepted: bool, initialize: bool,
) -> SensorChannelMemory:
  """cbc10 first channel: retain, seed, or filter with VSC +0x69c=0.21.

  CONFIRMED: accepted means the raw status equals 0x42 and four supplied fault
  gates are zero. It is NOT simply the single bit returned by the CAN decoder.
  UNKNOWN: physical meaning and upstream policy of every fault gate.
  OMITTED: deriving those gates and the separate published status. The caller
  must supply acceptance and initialization; an invalid sample retains value.
  """
  value = old.value
  if accepted:
    value = old.value + 0.21 * (sample - old.value) if old.previously_accepted and not initialize else sample
  return SensorChannelMemory(value, accepted)


def clamp_sensor(value: float) -> float:
  """cbd70 float bounds; Python does not reproduce SPE float32 rounding."""
  return min(max(value, -16.0), 15.99951171875)


def correct_sensor_geometry(filtered_sensor: float, other_channel_z: float) -> float:
  """cbdb0: clamp the product FIRST, then clamp the corrected sum.

  VCFG +0x30=0.00693000015. UNKNOWN: physical name/orientation of working +0xac
  ('z' here is a placeholder). Do not substitute the wheel residual for it.
  """
  correction = clamp_sensor(0.00693000015 * other_channel_z)
  return clamp_sensor(filtered_sensor + correction)


@dataclass(frozen=True)
class SensorBiasOutputs:
  residual_input: float  # uncompensated branch -> bf9b0 -> dfad0
  compensated_acceleration: float  # neighboring branch -> bfa10


def split_sensor_bias_paths(
  conditioned_sensor: float, initialized_bias: float, adaptive_bias: float,
  filtered_disturbance: float, blend: float,
) -> SensorBiasOutputs:
  """cbf30 first call's two numeric outputs, resolved using stack arguments.

  CONFIRMED: c8df0 latches initialized_bias ONCE from 4000d7f8. Stored record
  100 (36 bytes, fifth float) supplies it on successful startup read; otherwise
  the firmware default is zero. Later adaptive updates do not relatch it.
  UNKNOWN: the actual saved bias on any particular module. Supply it explicitly.
  OMITTED: adaptive-bias learning, disturbance filtering and blend scheduling;
  parameters here are their already calculated outputs, not guessed defaults.

  The residual receives the branch WITHOUT disturbance subtraction. Feeding
  compensated_acceleration to dfad0 would incorrectly close a feedback path.
  cc8e0/ca5c0 subsequently select/retain each output independently.
  """
  adaptive_bias = min(max(adaptive_bias, -0.981), 0.981)
  residual_input = conditioned_sensor - initialized_bias
  compensated = ((1.0 - blend) * (residual_input - filtered_disturbance)
                 + blend * (conditioned_sensor - adaptive_bias))
  return SensorBiasOutputs(clamp_sensor(residual_input), clamp_sensor(compensated))


def retain_sensor_output(new_value: float, retained_value: float, gates: tuple[int, int, int, int, int]) -> float:
  """ca5c0/ca610: publish and save new only when all five supplied gates are 0.

  Apply separately to the two bias outputs. UNKNOWN: full physical names and
  temporal behavior of the gates; retention alone does not mean ACC stays on.
  """
  return new_value if all(gate == 0 for gate in gates) else retained_value


def select_wheel_acceleration(c1680: float, c16b0: float, c16e0: float, c1710: float, selection: int) -> float:
  """dfad0 wheel derivative selection; DYN +1=0 in the examined calibration.

  These are acceleration derivatives, not the adjacent speed fields.
  UNKNOWN: exact wheel/axle labels; getter addresses preserve known identity.
  """
  if selection == 0:
    return (c16e0 + c1710) * 0.5
  if selection == 1:
    return (c1680 + c16b0) * 0.5
  return (c1680 + c16b0 + c16e0 + c1710) * 0.25


@dataclass(frozen=True)
class WheelResidualMemory:
  wheel_filtered: float
  residual_unclamped: float
  output: float


def update_sensor_wheel_residual(
  sensor: float, wheel_acceleration: float, old: WheelResidualMemory,
  slow_wheel_filter: bool, initialize_wheel: bool, initialize_residual: bool,
) -> WheelResidualMemory:
  """dfad0 numeric recurrence, normally once per 10 ms task; output -> c1250.

  sensor is the accepted/retained bf9b0 branch, NOT compensated bfa10.
  slow_wheel_filter means bVar4 OR the retention timer >0. OMITTED: computing
  that predicate/timer and dfad0's separate status outputs from upstream gates.
  The firmware shares initialize_residual between residual and output filters;
  initialize_wheel is a different flag. Coefficients are per tick, not per second.
  Python uses double precision; no claim of bit-exact SPE arithmetic is made.

  INFERRED: acceleration-domain disturbance. UNKNOWN: contributions of grade,
  pitch, bias and wheel-estimation errors; neither angle nor grade percentage.
  """
  bound = 2.37930012
  target = min(max(wheel_acceleration, sensor - bound), sensor + bound)
  alpha = 0.01999999955 if slow_wheel_filter else 0.118100002
  wheel = target if initialize_wheel else old.wheel_filtered + alpha * (target - old.wheel_filtered)
  residual = sensor - wheel
  if not initialize_residual:
    residual = old.residual_unclamped + 0.118100002 * (residual - old.residual_unclamped)
  limited = min(max(residual, -bound), bound)
  output = limited if initialize_residual else old.output + 0.00999999978 * (limited - old.output)
  # Save the UNCLAMPED middle state, plus a separate final output-filter state.
  return WheelResidualMemory(wheel, residual, output)



def c_div(numerator: int, denominator: int) -> int:
  """Integer division toward zero, including negative inputs."""
  if denominator <= 0:
    raise ValueError("This excerpt requires a positive denominator")
  return (abs(numerator) // denominator) * (-1 if numerator < 0 else 1)


def stock_integer_filter(target: int, previous: int, weight: int) -> int:
  """CONFIRMED 12e5e0; preserve its one-count anti-stall behavior.

  Weight is usually integer calibration_time_ms / dt_ms, but some callers
  provide a table weight directly. Machine-width overflow is not reproduced.
  """
  if weight < 0:
    raise ValueError("Filter weight must be nonnegative")
  result = c_div(previous * weight + target, weight + 1)
  if result == previous and target != previous:
    result += 1 if target > previous else -1
  return result


def update_acceleration_difference(
  dynamics_value: float, vehicle_accel: float, previous_milliunits: int, dt_ms: int = 40,
) -> int:
  """CONFIRMED core arithmetic in 1344b0; result is DAT_4001d8f4.

  INFERRED role: disturbance-related correction. Do NOT name it measured grade.
  Sensor c32d0 is compared with the vehicle acceleration estimate. The second
  input c1250 uses the SAME sensor source after conditioning/bias subtraction,
  compared with wheel-derived acceleration; it participates in classification.
  The residuals do not uniquely identify grade versus pitch/bias/wheel error.
  """
  if dt_ms <= 0:
    raise ValueError("dt_ms must be positive")
  difference = int(dynamics_value * 1000) - int(vehicle_accel * 1000)
  return stock_integer_filter(difference, previous_milliunits, 2000 // dt_ms) # cal 0x6a4


@dataclass(frozen=True)
class DynamicsClassCalibration:
  """Raw stock calibration values; no guessed physical names or defaults.

  Dynamics/acceleration thresholds use the firmware's integer milliunits.
  Reference threshold and DAT_4001d934 use signed speed in 0.01 km/h.
  """
  positive_input_threshold: int  # 0x69c
  negative_input_threshold: int  # 0x69e
  positive_difference_threshold: int  # 0x6a0
  negative_difference_threshold: int  # 0x6a2
  positive_activation_ms: int  # 0x6a6
  positive_counter_limit_ms: int  # 0x6a8
  negative_activation_ms: int  # 0x6aa
  negative_counter_limit_ms: int  # 0x6ac
  minimum_raw_reference: int  # 0x69a
  negative_class_enabled: bool  # byte 0x698 == 1


def classify_dynamics(
  second_input_milliunits: int, filtered_difference_milliunits: int,
  raw_reference_d934: int, counter: int, cal: DynamicsClassCalibration, dt_ms: int = 40,
) -> tuple[int, int]:
  """CONFIRMED counter/classification portion of 1344b0.

  Returns (new counter DAT_4001d91a, class DAT_4001d8f2).
  raw_reference_d934 is signed speed in 0.01 km/h; cal 0x69a=4000 means
  class -1 is prohibited below 40 km/h, including creep. Class +1 has no
  corresponding speed gate. Physical class names remain inferred, not OEM names.
  The separate d91c timer update at the start of 1344b0 is OMITTED: signed
  speed < -50 centi-km/h permits counting down; otherwise it reloads 5000/dt.
  It is NOT a stationary-stop timer.
  No local invalid-input => zero-class rule exists. Sensor status c3060==0x24
  instead contributes to fault aggregates in 1333f0/132c70. UNKNOWN: exact
  supervisor disengagement timing; do not infer it from this local classifier.
  """
  if dt_ms <= 0:
    raise ValueError("dt_ms must be positive")
  positive_evidence = (second_input_milliunits > cal.positive_input_threshold
                       and filtered_difference_milliunits > cal.positive_difference_threshold)
  negative_evidence = (second_input_milliunits < cal.negative_input_threshold
                       and filtered_difference_milliunits < cal.negative_difference_threshold)
  if positive_evidence:
    if counter < cal.positive_counter_limit_ms // dt_ms:
      counter += 1
  elif negative_evidence:
    if raw_reference_d934 < cal.minimum_raw_reference:
      counter = 0
    elif counter > -(cal.negative_counter_limit_ms // dt_ms):
      counter -= 1
  else:
    # Evidence faded: count back toward neutral rather than flipping immediately.
    counter += -1 if counter > 0 else 1 if counter < 0 else 0

  if counter >= cal.positive_activation_ms // dt_ms:
    dynamics_class = 1
  elif (counter <= -(cal.negative_activation_ms // dt_ms)
        and cal.negative_class_enabled and raw_reference_d934 >= cal.minimum_raw_reference):
    dynamics_class = -1
  else:
    dynamics_class = 0
  return counter, dynamics_class


def minimum_capability_from_converted_torque(
  converted_min_torque_nm: float, speed: float, torque_to_accel: Callable[[float, float], float],
) -> float:
  """CONFIRMED final part of 1399a0, calibration 0x68e=-5000 / 0x690=0.

  Input is AFTER the stock fallback selection and sign-dependent efficiency
  conversion, not raw AxleTorqueMin. Those operations are OMITTED here.
  torque_to_accel represents stock 13bb20 (vehicle model including resistance).
  Actual and maximum torque have separate capability conversions in 139ce0.
  """
  bounded_torque = min(max(converted_min_torque_nm, -5000.0), 0.0)
  return torque_to_accel(bounded_torque, speed)


@dataclass(frozen=True)
class FeedbackTerms:
  selected_request: float
  proportional: float
  integral: float
  reference_rate_term: float
  auxiliary_integral: float
  dynamics_correction: float # table 0x774(raw difference); NOT raw DAT_4001d8f4


def ordinary_feedback_sum(terms: FeedbackTerms, request_enabled: bool) -> float:
  """CONFIRMED ordinary summation near the end of 13a5d0.

  The computation of individual terms is described in ASCM_LOOP_REFERENCE.md.
  Supplying these terms does not implement gain scheduling or anti-windup.
  OMITTED: request flags +0xc bit25 select a capability-ramping override instead.
  """
  corrected = (terms.selected_request + terms.proportional + terms.integral
               + terms.reference_rate_term + terms.auxiliary_integral)
  if request_enabled:
    corrected += terms.dynamics_correction
  return corrected


@dataclass(frozen=True)
class AllocationSnapshot:
  """State AFTER feedback, BEFORE allocation. Acceleration quantities are m/s².

  Callers must provide actual branch conditions; no guessed 'normal' defaults.
  'raw' names deliberately preserve flags whose physical meanings are UNKNOWN.
  """
  previous_owner: Owner
  request_state: int # firmware 0..4; NOT the CAN brake-mode nibble
  speed: float
  corrected_accel: float # feedback block +0x10
  dynamics_correction: float # feedback block +0xc, after table 0x774
  min_powertrain_accel: float # capability block +4
  dynamics_class: int # DAT_4001d8f2: -1, 0, +1; UNKNOWN physical class names
  alternate_entry_flag: bool # DAT_4001d990 == 1
  raw_request_bit24: bool
  raw_request_bit23: bool
  raw_vehicle_bit25: bool # DAT_4001d9a0 bit25
  raw_timer_d91c_nonzero: bool
  raw_feedback_e8: int
  previous_brake_submode: int
  raw_latch_e184: bool


def allocation_threshold(s: AllocationSnapshot, lookup: Callable[[int, float], float]) -> float:
  """CONFIRMED 13afc0 threshold for states 1/2 with recovered calibration.

  lookup(offset, speed) must return a stock table result converted to m/s².
  No invented tables are included. cal 0x83c=1 includes minimum capability when
  retaining brake mode. cal 0x78c=600 / 0x78e=800 give weights 0.4 / 0.2.
  """
  if s.request_state not in (1, 2):
    raise NotTranscribed("This threshold excerpt covers request states 1 and 2")
  if s.previous_owner == Owner.BRAKE:
    margin = lookup(0x708, s.speed)
    correction_weight = 0.4
  else:
    table = 0x720 if s.dynamics_class == -1 and s.alternate_entry_flag else 0x714
    margin = lookup(table, s.speed)
    correction_weight = 0.2
  state_margin = 0.050 if s.request_state == 2 else 0.0 # cal 0x81c / 0x81e
  return s.min_powertrain_accel + margin + correction_weight * s.dynamics_correction + state_margin


@dataclass(frozen=True)
class AllocationResult:
  owner: Owner
  torque_path_accel: float
  brake_path_accel: float
  latch_e184: bool


def ordinary_moving_allocation(
  s: AllocationSnapshot, threshold: float, shape_brake_request: Callable[[float], float],
) -> AllocationResult:
  """CONFIRMED common state-1/2 branches of 13afc0, excluding brake submodes.

  shape_brake_request must handle prior demand, entry preset/counter and slew:
  cal 0x806/808/80a/80c/80e and speed table 0x810. It must NOT clamp to zero.
  Firmware branches outside this excerpt raise rather than silently guessing.
  """
  if s.request_state not in (1, 2):
    raise NotTranscribed("Request states 0, 3 and 4 have separate branches")

  evaluate_brake_boundary = not s.raw_request_bit24 or s.raw_request_bit23 or s.raw_vehicle_bit25
  if not evaluate_brake_boundary:
    return AllocationResult(Owner.TORQUE, s.corrected_accel, 0.0, s.raw_latch_e184)

  if s.corrected_accel < threshold:
    # Positive vehicle acceleration can remain in brake mode if below boundary.
    # This subtracts the SAME mapped correction added by ordinary_feedback_sum.
    brake_target = s.corrected_accel - s.dynamics_correction
    return AllocationResult(Owner.BRAKE, 0.0, shape_brake_request(brake_target), True)

  if not s.raw_vehicle_bit25 and s.raw_timer_d91c_nonzero:
    if s.raw_feedback_e8 == 0 and s.previous_brake_submode != 3:
      # After the brake-selection latch, seed torque-side acceleration at the
      # minimum capability. 13a360 separately seeds its actual output in Nm.
      torque_accel = s.min_powertrain_accel if s.raw_latch_e184 else s.corrected_accel
      return AllocationResult(Owner.TORQUE, torque_accel, 0.0, s.raw_latch_e184)
    raise NotTranscribed("Firmware retains previous outputs here; needs complete state")

  # Separate recovered branch: brake retained WITHOUT subtracting correction.
  # Physical meaning of the gating flags is UNKNOWN. Do not generalize the
  # ordinary subtraction formula across every firmware state.
  raise NotTranscribed("State-gated brake retention uses corrected_accel directly")


@dataclass(frozen=True)
class TorqueState:
  output_nm: float
  filter_nm: float


def primary_torque_output(
  previous_owner: Owner, owner: Owner, axle_torque_min_nm: float,
  converted_target_nm: float, previous: TorqueState,
  filter_target: Callable[[float, float], float],
  slew_target: Callable[[float, float], float],
) -> TorqueState:
  """CONFIRMED primary torque output in 13a360; calibrated -650 Nm brake path.

  converted_target_nm is AFTER 13bbc0 and efficiency conversion. A separate
  ratio-dependent output and 13a180 auxiliary output are separate numbers;
  see ratio_torque_output and auxiliary_torque_number. Their numeric outputs
  have a raw block-transfer consumer, but no actuator publisher was found.
  axle_torque_min_nm must be AFTER 139ce0 lowers minimum to actual if actual
  torque is below the reported minimum; it is not always the untouched CAN field.
  filter_target uses cal 0x72e=150 ms; slew_target uses 0x6dc and 0x6e4/0x6f0.
  The caller must implement those stock operations; this supplies no new tune.
  """
  if owner != Owner.TORQUE:
    # This is the ASCM powertrain command while another mode owns acceleration,
    # not a claim that delivered axle torque is always -650 Nm.
    return TorqueState(-650.0, previous.filter_nm)
  if previous_owner != Owner.TORQUE:
    return TorqueState(axle_torque_min_nm, axle_torque_min_nm)
  filtered = filter_target(converted_target_nm, previous.filter_nm)
  return TorqueState(slew_target(filtered, previous.output_nm), filtered)


def stock_lookup(points: tuple[tuple[int, int], ...], argument: int) -> int:
  """12e3e0: signed, interleaved (x, y) pairs with endpoint saturation.

  Preserve table order: firmware does NOT sort points, including table 0x7de.
  This matters because that calibration's x values descend.
  """
  index = 0
  while index < len(points) - 1 and points[index][0] < argument:
    index += 1
  x, y = points[index]
  if index:
    previous_x, previous_y = points[index - 1]
    if argument < x and previous_x < x:
      return previous_y + c_div((y - previous_y) * (argument - previous_x), x - previous_x)
  return y


def stock_integer_slew(target: int, previous: int, lower_rate: int, upper_rate: int, dt_ms: int = 40) -> int:
  """12e620/12e630: clamp rate, then integrate it, both divisions toward zero.

  Rates are raw output counts/second. Unlike the filter there is no anti-stall
  increment. Does not reproduce multiplication overflow or short narrowing.
  """
  rate = c_div((target - previous) * 1000, dt_ms)
  rate = min(max(rate, min(lower_rate, upper_rate)), max(lower_rate, upper_rate))
  return previous + c_div(rate * dt_ms, 1000)


@dataclass(frozen=True)
class RequestSelection:
  request_milli: int
  state: int
  source: int # vehicle +0x1d: 0=candidate A, 1=B, 2=boundary, 3=disabled
  timer_e1a4: int


def select_request(
  candidate_a: int, candidate_b: int, minimum_accel: int, previous_integral: int,
  previous_request: int, predicted_speed: int, speed: int, gear_nonzero: bool,
  request_flags: int, vehicle_flags_14: int, timer_e1a4: int,
  lookup: Callable[[int, int], int], dt_ms: int = 40,
) -> RequestSelection:
  """13ade0, complete branch selection for calibration 23366550.

  Raw units: acceleration 0.001 m/s², speed 0.01 m/s. Flag numbers use LSB=0.
  A/B are upstream candidates, not accelerator/brake pedal measurements.
  OMITTED: upstream planning/supervisor generation of candidates and flags.
  UNKNOWN: reachable combinations and full timing in a real drive. This helper
  translates selection for supplied inputs, not every policy producing them.
  Assembly 13aec6 resolves the decompiler's missing max() arguments.
  """
  timer = max(timer_e1a4 - 1, 0)
  if not request_flags & (1 << 26):
    return RequestSelection(0, 0, 3, timer)
  if candidate_a == candidate_b and gear_nonzero:
    selected, state, source = candidate_a, 2, 0
  elif candidate_b == 3000 and gear_nonzero: # cal 0x7a6
    selected, state, source = candidate_a, 4, 0
  elif candidate_a == -6000: # cal 0x7a8
    selected, state, source = candidate_b, 3, 1
  elif candidate_b + previous_integral < minimum_accel:
    selected, state, source = candidate_b, 1, 1
  elif minimum_accel < candidate_a + previous_integral:
    selected, state, source = candidate_a, 1, 0
  else:
    # It is max(A, minimum), NOT minimum minus the previous integral.
    selected, state = max(candidate_a, minimum_accel), 1
    source = 0 if selected == candidate_a else 2
  if request_flags & (1 << 28):
    factor = lookup(0x7DE, predicted_speed)
    if vehicle_flags_14 & (1 << 24) or timer:
      if vehicle_flags_14 & (1 << 24):
        timer = 2000 // dt_ms # 0x7f6
      state = 3
  elif request_flags & (1 << 27) and previous_request > 0: # cal 0x81e
    state, factor = 4, lookup(0x7EA, speed)
  else:
    factor = 1000
  return RequestSelection(c_div(selected * factor, 1000), state, source, timer)


@dataclass(frozen=True)
class RawAllocation:
  """13afc0 output, raw 0.001 m/s²; submode is selected separately below."""
  owner: Owner
  torque_accel: int
  brake_accel: int
  latch_e184: bool


def allocate_acceleration(
  previous: RawAllocation, request_state: int, request_flags: int,
  corrected: int, correction: int, minimum_accel: int, threshold: int,
  standstill_status: bool, special_timer: int, hold: bool, previous_submode: int,
  dt_ms: int = 40,
) -> RawAllocation:
  """All outer-mode branches of 13afc0 for the examined calibration.

  0x806=0 and initial 0x808=0 disable entry preset/counter; 0x80c=0 and
  table 0x810 (all 5000) give symmetric 5 m/s³ brake slew after entry.
  threshold is the state-1/2 boundary, including the state-specific margin.
  Feedback may clear e184 before this call; pass that updated latch in previous.
  """
  latch = previous.latch_e184
  if request_state == 0:
    owner = previous.owner if request_flags & (1 << 25) else Owner.INACTIVE
    return RawAllocation(owner, 0, 0, latch)
  if request_state in (1, 2):
    evaluate = not request_flags & (1 << 24) or request_flags & (1 << 23) or standstill_status
    if not evaluate:
      return RawAllocation(Owner.TORQUE, corrected, 0, latch)
    if corrected < threshold:
      target = corrected - correction
      brake = stock_integer_slew(target, previous.brake_accel, -5000, 5000, dt_ms) if previous.owner == Owner.BRAKE else target
      return RawAllocation(Owner.BRAKE, 0, brake, True)
    if not standstill_status and special_timer:
      if not hold and previous_submode != 3:
        return RawAllocation(Owner.TORQUE, minimum_accel if latch else corrected, 0, latch)
      return previous # Both numeric outputs and owner are retained.
    # No subtraction, no slew, and no write to the old torque-acceleration slot.
    return RawAllocation(Owner.BRAKE, previous.torque_accel, corrected, latch)
  if request_state == 3:
    if not request_flags & (1 << 24) or standstill_status:
      return RawAllocation(Owner.BRAKE, 0, corrected - correction, latch)
    return RawAllocation(Owner.TORQUE, corrected, 0, latch)
  if request_state == 4:
    return RawAllocation(Owner.TORQUE, corrected, 0, latch)
  return RawAllocation(Owner.INACTIVE, 0, 0, latch)


@dataclass(frozen=True)
class BrakeSubmode:
  submode: int
  active_timer: int
  history_e170: int


def select_brake_submode(
  owner: Owner, previous_owner: Owner, speed_centimetres: int,
  cruise_main: bool, suppression: bool, previous_hold: bool, hold_variant_d8e2: bool,
  stop_flag27: bool, stop_flag28: bool, standstill_status: bool, special_timer: int,
  previous: BrakeSubmode, dt_ms: int = 40,
) -> BrakeSubmode:
  """Final part of 13afc0, calibration 0x820/822=150 and 0x824=0.

  Consumes hold BEFORE 13a180 updates it. Active timer is decremented later in
  131440. A submode is not a CAN mode until combined with the independent bit.
  UNKNOWN: EBCM pressure/actuation semantics of submodes 1..5; retain numbers
  rather than assigning hydraulic operating-mode names from ASCM evidence.
  """
  timer, history = previous.active_timer, previous.history_e170
  if owner != Owner.BRAKE or not cruise_main or suppression:
    mode = 1
  elif previous_hold and speed_centimetres < 150:
    mode = 4 if hold_variant_d8e2 else 5
    if mode == 5:
      timer, history = 2500 // dt_ms, 2
  elif (speed_centimetres < 150 and (stop_flag27 or stop_flag28 or standstill_status)) or special_timer == 0:
    mode = 3 if previous_owner == Owner.BRAKE else 2
  else:
    mode = 2
    history = 1 if speed_centimetres < 0 and history in (1, 2) else 0
  return BrakeSubmode(mode, timer, history)


def encode_brake_mode(owner: Owner, state: BrakeSubmode) -> tuple[int, BrakeSubmode]:
  """131440 timer ordering + MPU2 48420 packing; before external suppression.

  A timer reloaded to 62 is decremented to 61 in that same output cycle.
  """
  state = BrakeSubmode(state.submode, max(state.active_timer - 1, 0), state.history_e170)
  active = owner == Owner.BRAKE or state.active_timer != 0
  return (int(active) << 3) | state.submode, state


def update_hold_flag(
  previous_hold: bool, selected_request: int, request_flags: int,
  vehicle_flags_08: int, vehicle_flags_14: int, raw_d9b8_bit16: bool,
  raw_d994: int, timer_e1a4: int,
) -> bool:
  """Exact hold-latch predicates from 13a180, evaluated AFTER allocation.

  Raw names are intentional. This includes the two sequential tests: a clear
  in the first test can be followed by a set in the second test in one call.
  Controller +0xe already holds THIS cycle's selected request at this stage.
  No speed or pressure test exists in these predicates.
  """
  enabled = bool(request_flags & (1 << 26))
  vehicle_bit25 = bool(vehicle_flags_08 & (1 << 25))
  hold = previous_hold
  if (raw_d9b8_bit16 and selected_request > 0 or not enabled
      or not vehicle_bit25 and raw_d994 == 0 or vehicle_flags_14 & (1 << 26)):
    hold = False
  ordinary = (not enabled or (
    (not request_flags & (1 << 28) and selected_request > 0
     or not vehicle_flags_14 & (1 << 24) and timer_e1a4 == 0 and not hold)
    and not vehicle_bit25))
  if not ordinary:
    hold = True
  return hold


@dataclass(frozen=True)
class VehicleModel:
  """139e50 fields used by 13bb20/13bbc0, raw calibration 23366550.

  Physical names follow dimensional arithmetic, not recovered OEM symbols.
  Mass is 0.1 kg/count, circumference mm, drag 0.001 N/(m/s)²/count,
  rolling and acceleration factors 0.001/count. Reloaded each 131440 call.
  """
  mass_deci_kg: int = 17760 # +0x10, cal 0x8b8
  circumference_mm: int = 2032 # +0x12, cal 0x8b4
  drag_milli: int = 250 # +0x14, cal 0x89a
  rolling_milli: int = 8 # +0x1a, cal 0x89c
  acceleration_factor_milli: int = 1000 # +0x1c, cal 0x89e


def model_acceleration(torque_nm: int, speed_centi: int, model: VehicleModel) -> int:
  """13bb20: torque to acceleration in 0.001 m/s²; nested integer divisions."""
  radius_mm = model.circumference_mm * 10000 // 62832
  drag = c_div(c_div(model.drag_milli * speed_centi, 100) * speed_centi, 100)
  force_milli = c_div(torque_nm * 1000, radius_mm) * 1000 - drag
  accel = c_div(force_milli * 10, model.mass_deci_kg) - c_div(model.rolling_milli * 9810, 1000)
  return c_div(accel * 1000, model.acceleration_factor_milli)


def model_torque(accel_milli: int, speed_centi: int, model: VehicleModel) -> int:
  """13bbc0: inverse vehicle model, BEFORE sign-dependent efficiency scaling.

  Quantization prevents exact round trips. Dynamics class +1 adds table 0x7fa
  to rolling_milli in 13a360 AFTER capability calculation and BEFORE this call.
  That temporary model also reaches 13a180; next cycle reload restores it.
  """
  radius_mm = model.circumference_mm * 10000 // 62832
  drag = c_div(c_div(model.drag_milli * speed_centi, 100) * speed_centi, 100)
  accel = c_div(model.rolling_milli * 9810, 1000) + c_div(accel_milli * model.acceleration_factor_milli, 1000)
  force = c_div(c_div(accel * model.mass_deci_kg, 10) + drag, 1000)
  return c_div(force * radius_mm, 1000)


def publish_brake_acceleration(brake_milli: int, lower_envelope_milli: int, dt_ms: int = 40) -> int:
  """131440 AFTER 139d80: slew toward envelope, then publish through c26a0.

  cal 0x5f6 supplies lower_envelope_milli, upper=2000, 0x620=10000 counts/s.
  Previous argument is the CURRENT allocation output, not last cycle's output!
  Consequently this can remain outside the envelope on a large excursion.
  Returned value overwrites 4001dae6 and becomes next cycle's prior brake demand.
  """
  target = min(max(brake_milli, lower_envelope_milli), 2000)
  return stock_integer_slew(target, brake_milli, -10000, 10000, dt_ms)


@dataclass(frozen=True)
class FeedbackMemory:
  """Mutable firmware state represented as an immutable snapshot (raw units).

  Integral accumulator has 1000 times the precision of acceleration milliunits.
  History stores previous selected requests, not this cycle's new selection.
  Fields correspond to 4001deb4 + offsets and the e17c/e182/e188/e184 globals.
  """
  history: tuple[int, ...] = (0,) * 100
  history_index: int = 0
  previous_request: int = 0
  corrected: int = 0
  stable_request_ms: int = 0
  reference_delay_ms: int = 0
  i_reference: int = 0
  active_ms: int = 0
  integral_accumulator: int = 0
  proportional: int = 0
  previous_request_flags: int = 0
  allocation_latch: bool = True


@dataclass(frozen=True)
class FeedbackResult:
  memory: FeedbackMemory
  p_reference: int
  i_reference_for_error: int # Taken BEFORE a possible transition reset.
  p_error: int
  i_error: int
  correction: int
  capability_ramp_active: bool # vehicle +0x14 bit27


def request_history(history: tuple[int, ...], index: int, delay_ms: int, dt_ms: int) -> int:
  """13a570: integer delay, clamped to 0..99 samples; no interpolation."""
  delay = min(max(c_div(delay_ms, dt_ms), 0), len(history) - 1)
  return history[(index - delay) % len(history)]


def update_feedback(
  old: FeedbackMemory, selected: int, request_state: int, request_flags: int,
  vehicle_flags_14: int, measured_accel: int, speed_centi: int,
  owner: Owner, owner_before_previous_allocation: Owner,
  gear_matches_previous: bool, previous_hold: bool,
  minimum_accel: int, maximum_accel: int, filtered_capability: int,
  previous_torque_nm: int, maximum_torque_nm: int,
  dynamics_class: int, alternate_entry_flag: bool, filtered_difference: int,
  lookup: Callable[[int, int], int], dt_ms: int = 40,
) -> FeedbackResult:
  """13a5d0 specialized to 23366550, in raw fixed-point units.

  Full active feedback branches, including the bit25 capability ramp. From
  firmware initialization, reference-rate and auxiliary-integral states remain
  zero: table 0x768 is all zero, and 0x74a/0x762 are zero. This specialization
  omits those disabled states, not just their contributions to the final sum.
  0x6ba=1 enables brake PI; 0x5df=0 disables alternate positive-I suppression.
  No short narrowing or 32-bit overflow is reproduced. Stock lookup callbacks
  must preserve integer interpolation and table order.
  """
  stable_ms = old.stable_request_ms
  if abs(old.history[old.history_index] - old.previous_request) <= 100:
    if stable_ms < 5000:
      stable_ms += dt_ms
  else:
    stable_ms = 0
  index = (old.history_index + 1) % 100
  history = list(old.history)
  history[index] = old.previous_request
  history = tuple(history)
  # Rate gain is zero, but its request difference is used to choose delay in
  # the generic firmware. Both signs select 120 ms in this calibration.
  delay_target = old.reference_delay_ms
  if gear_matches_previous or owner != Owner.TORQUE:
    if vehicle_flags_14 & (1 << 24):
      delay_target = 1000
    elif owner in (Owner.TORQUE, Owner.BRAKE):
      delay_target = 120
  else:
    delay_target += dt_ms
  delay = stock_integer_filter(delay_target, old.reference_delay_ms, 400 // dt_ms)
  p_reference = request_history(history, index, delay, dt_ms)
  i_reference = stock_integer_filter(p_reference, old.i_reference, 100 // dt_ms)
  i_reference_for_error = i_reference
  p_error, i_error = p_reference - measured_accel, i_reference - measured_accel
  if (vehicle_flags_14 & (1 << 24) and selected < 0) or previous_hold:
    p_error = i_error = 0
  enabled = bool(request_flags & (1 << 26))
  was_enabled = bool(old.previous_request_flags & (1 << 26))
  active_ms = old.active_ms
  if enabled and not request_flags & (1 << 24) and request_state not in (3, 4):
    if active_ms < 10000:
      active_ms += dt_ms
  else:
    active_ms = 0
  integral, latch = old.integral_accumulator, old.allocation_latch
  transition = (not was_enabled or request_flags & (1 << 24) or request_state in (3, 4)
                or owner in (Owner.TORQUE, Owner.BRAKE) and owner != owner_before_previous_allocation)
  if not enabled:
    integral = 0
  elif transition:
    i_reference = measured_accel
    integral = max(minimum_accel, (filtered_capability - measured_accel) * lookup(0x73E, speed_centi))
    latch = False
    if was_enabled and request_state in (3, 4):
      integral = stock_integer_filter(integral, old.integral_accumulator, 2000 // dt_ms)
  elif (abs(old.corrected) <= 5000 and abs(selected) <= 5000 and abs(i_error) <= 10000
        and previous_torque_nm <= c_div(250 * maximum_torque_nm, 100) + maximum_torque_nm):
    increment = lookup(0x736, speed_centi) * i_error
    if dynamics_class == -1 and alternate_entry_flag:
      increment = c_div(increment * 50, 100)
    integral += c_div(increment * dt_ms, 1000)
  correction = lookup(0x774, filtered_difference)
  p_target = c_div(p_error * lookup(0x74E, abs(selected) + 2 * abs(p_error)), 1000)
  proportional = 0 if active_ms == 0 else stock_integer_filter(
    p_target, old.proportional, lookup(0x756, active_ms if gear_matches_previous else 0))
  ramp_active = False
  if request_flags & (1 << 25):
    ramp_active = True
    corrected = stock_integer_slew(minimum_accel, old.corrected, -1500, 3000, dt_ms)
    if not request_flags & (1 << 23):
      if (owner == Owner.TORQUE and corrected <= minimum_accel or owner == Owner.BRAKE and minimum_accel <= corrected):
        ramp_active, corrected = False, minimum_accel
    else:
      corrected = stock_integer_slew(maximum_accel, corrected, -2000, 2000, dt_ms)
      if maximum_accel <= corrected or vehicle_flags_14 & (1 << 26):
        ramp_active = False
  else:
    corrected = selected + proportional + c_div(integral, 1000)
    if enabled:
      corrected += correction
  memory = FeedbackMemory(history, index, selected, corrected, stable_ms, delay, i_reference,
                          active_ms, integral, proportional, request_flags, latch)
  return FeedbackResult(memory, p_reference, i_reference_for_error, p_error, i_error, correction, ramp_active)


def first_object_stop_flags(object_state_3c: int, previous_state2_latch: bool) -> tuple[bool, bool]:
  """130cc0: return (4001dcc0 bit27, bit28) from first 64-byte object record.

  Startup descriptor 40220 initializes pointer 4001d7e0 to 4001dcb0.
  The loop writes object flags at pointer + index*0x44 +0x10. For index zero
  that is 4001dcc0. Input record byte +0x3c is copied from the c2c20 object list.
  previous_state2_latch is DAT_4001dc7a; save the returned first value there.
  CONFIRMED: 13d3c0/13d570 copy internal object +0x1b to record +0x3c,
  passing through values 0..4 (other values become 0).
  UNKNOWN: physical labels for states 1/2 and their perception-side producer.
  Do not assume state 1 means stationary or state 2 means moving.
  """
  state1 = object_state_3c == 1
  state2_or_retained = object_state_3c == 2 or previous_state2_latch and state1
  return state2_or_retained, state1


def hold_variant_4_allowed(speed_centi_kph: int, threshold_centi_kph: int,
                           raw_d959: int, raw_d95a: int, raw_d95b: int) -> bool:
  """133960 produces d8e2, with calibration 0x5de=1.

  This selects submode 4 instead of 5 only AFTER hold and <1.5 m/s gates.
  threshold_centi_kph comes from cal 0x5e4=300 (3 km/h).
  decode_hold_input_enums documents the recovered sources. UNKNOWN: physical
  names of d95a/d95b; plausible seat-belt/parking-brake labels are not evidence.
  """
  return (speed_centi_kph < threshold_centi_kph and (raw_d959 <= 1 or raw_d95a in (0, 1))
          and raw_d95b in (0, 2))


@dataclass(frozen=True)
class HoldInputEnums:
  door_d959: int
  unidentified_d95a: int
  unidentified_d95b: int


def decode_hold_input_enums(c61d0: int, c62a0: int, c62c0: int, c6200: int, c6220: int) -> HoldInputEnums:
  """132fb0: getter values -> the three enums consumed by hold_variant_4_allowed.

  Extended receive keys use ID & 0x03ffff00 (not unique full CAN identifiers):
    0x00630000 byte0 bit0   -> c61d0 (local DBC: DriverDoorOpened, ID 0x10630000)
    0x00608000 byte0 bits0/1 -> c62a0/c62c0
    0x00336000 byte0 bits0/1 -> c6200/c6220
  CONFIRMED: d959=1 means the getter indicated open. d959=2 includes other,
  potentially invalid getter values; it does not prove the door is closed.
  UNKNOWN: physical names for the latter two bit pairs and full stale-data
  policy. Accept the original getter integers here; do not coerce to booleans.
  """
  door = 1 if c61d0 == 1 else 2
  unidentified_a = 0 if c62c0 != 0 else 1 if c62a0 == 1 else 2
  unidentified_b = (1 if c6200 == 1 else 2) if c6220 == 0 and c6200 in (0, 1) else 0
  return HoldInputEnums(door, unidentified_a, unidentified_b)


def ratio_torque_output(
  owner: Owner, converted_target_nm: int, ratio: int, ratio_factor_milli: int, speed_weight_milli: int,
) -> tuple[int, int]:
  """13a360 +6 output, BEFORE primary torque transition seed/filter/slew.

  converted_target_nm already includes sign-dependent efficiency conversion.
  ratio is capability +0xa (unsigned), ratio_factor is +0x10 and speed_weight
  is lookup(0x790, speed). Return (output, updated ratio); firmware changes a
  zero divisor in shared capability state to 1, even outside torque ownership.
  CONFIRMED arithmetic, excluding machine narrowing/overflow.
  UNKNOWN: full physical meaning/units of this output and transfer endpoint.
  No actuator publication found. Do not substitute it for primary Nm output.
  """
  ratio = 1 if ratio == 0 else ratio
  blend = c_div(ratio_factor_milli * speed_weight_milli, 1000) + 1000 - speed_weight_milli
  output = c_div(c_div(converted_target_nm * 100, ratio) * blend, 1000)
  return (output if owner == Owner.TORQUE else -650), ratio


def auxiliary_torque_number(
  ordinary_branch: bool, owner: Owner, previous_owner: Owner,
  brake_accel_milli: int, proportional_milli: int, integral_milli: int, rate_milli: int,
  previous_auxiliary_nm: int, powertrain_entry_nm: int, request_bit22: bool,
  acceleration_to_torque: Callable[[int], int], dt_ms: int = 40,
) -> int:
  """13a180 numeric +8 output only; full routine also changes hold/vehicle flags.

  ordinary_branch is the result of 13a180's SECOND if condition (see
  update_hold_flag's `ordinary` local), not simply `not previous_hold`.
  acceleration_to_torque must use 13bbc0 with this cycle's model/speed, including
  the class +1 rolling adjustment already made by 13a360. No primary-torque
  efficiency conversion is applied on this branch.

  CONFIRMED: entry seed, -40 Nm ceiling, hold target and +/-10000 Nm/s slew.
  OMITTED: flag23 hysteresis and timer e178: ordinary brake uses corrected
  acceleration against cal 0x730/732 and reload 0x734/dt; ordinary nonbrake
  clears flag23 when the timer expires. Preserve those side effects in a full
  backend even though no actuator consumer of this numeric output was found.
  UNKNOWN: external meaning of that flag and the block-transfer endpoint.
  """
  if not ordinary_branch:
    # This branch sets hold even if the preceding condition just cleared it.
    target = acceleration_to_torque(proportional_milli + integral_milli + rate_milli - 4000)
    return stock_integer_slew(target, previous_auxiliary_nm, -10000, 10000, dt_ms)
  if owner != Owner.BRAKE:
    return 0
  if previous_owner != Owner.BRAKE:
    return powertrain_entry_nm  # Powertrain +0, distinct from minimum torque +2.
  target = min(acceleration_to_torque(brake_accel_milli), -40)
  # Caller 131440 sets request bit22 in the traced path.
  return stock_integer_slew(target, previous_auxiliary_nm, -10000, 10000, dt_ms) if request_bit22 else target
