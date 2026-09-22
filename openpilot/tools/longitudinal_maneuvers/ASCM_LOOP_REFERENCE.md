# Reading the ASCM longitudinal loop

Start at `read_one_cycle()` in [ascm_loop_reference.py](ascm_loop_reference.py).
Read [ASCM_FIRMWARE_AUDIT.md](ASCM_FIRMWARE_AUDIT.md) for the firmware recheck,
corrections, numeric calibrations, state map and remaining questions.
The [dynamics/output follow-up](ASCM_DYNAMICS_AND_OUTPUTS.md) traces the shared
sensor source, bias/validity branches and extra-output consumers.

This is an explanatory reference. The individual translated stages can be
exercised, but `read_one_cycle()` is an interface requiring a backend, not a
complete ASCM simulator. No vehicle controller, CAN parser or maneuver changes.

## The cycle

```text
prepare vehicle state, dynamics and upstream requests
    -> reload vehicle-model calibration
    -> prepare actual/minimum/maximum powertrain capability
    -> select an acceleration request
    -> update delayed references and acceleration feedback
    -> allocate brake/torque and choose brake submode
    -> convert and shape primary torque
    -> update auxiliary torque and hold latch
    -> attempt model adaptation and record response history
    -> reshape brake command and publish outputs/enables
```

The main arithmetic runs at 40 ms. Vehicle-dynamics estimation feeding it has a
separate 10 ms schedule. Feedback sees last cycle's owner and hold; allocation
chooses the new owner, and the subsequent hold update affects the next allocation.

The model reload and final publication are in the caller `131440`. They matter:
the reload overwrites the mass adaptation, and publication changes the brake
demand before storing it for the next cycle. The first reference omitted them.

## Reading the Python

Earlier ordinary-path excerpts use SI units. New complete branch excerpts use
firmware integers: acceleration in 0.001 m/s², speed generally 0.01 m/s, torque
in Nm. Dynamics classification instead gates on speed in **0.01 km/h**.
`UNKNOWN` comments mark open questions, `OMITTED` marks firmware not translated
in that excerpt, and `INFERRED` marks interpretations rather than recovered OEM
names. These distinctions appear at the relevant functions and cycle stages.
Sensor arithmetic uses floating-point acceleration-domain values and explicit
state snapshots; it does not reproduce every float32 rounding operation.
Each function documents its units. Do not connect differently scaled functions
without conversion.

| Function | What it establishes |
|---|---|
| `read_one_dynamics_tick` | Separate 10 ms sensor → wheel → residual ordering, including previous/new data dependencies |
| `condition_dynamics_sensor`, `correct_sensor_geometry` | Sensor acceptance/retention, 0.21 filter and bounded geometric correction |
| `split_sensor_bias_paths`, `retain_sensor_output` | Initialized versus adaptive bias, separate compensated/uncompensated outputs and retained values |
| `select_wheel_acceleration`, `update_sensor_wheel_residual` | Wheel derivative selection and the three-state residual filter; upstream gates remain supplied inputs |
| `decode_dynamics_0x140` | Eight-byte receive field, signed 12-bit decode, scale and raw validity bit |
| `stock_integer_filter`, `stock_lookup`, `stock_integer_slew` | Actual integer helper behavior, including truncation, filter anti-stall and table-order effects |
| `update_acceleration_difference`, `classify_dynamics` | Numeric difference and separate −1/0/+1 state |
| `select_request` | All request-state branches, sentinels, candidate selection and override scaling |
| `update_feedback` | Active PI, delayed references, resets/gates and capability-ramp override for calibration 23366550 |
| `ordinary_feedback_sum` | Short SI explanation of the generic sum; individual terms are supplied |
| `allocation_threshold`, `ordinary_moving_allocation` | Short SI explanation of ordinary entry/exit hysteresis |
| `allocate_acceleration` | All outer-owner branches for the examined calibration, including retained outputs and forced torque |
| `select_brake_submode`, `encode_brake_mode` | Brake submode priority, history, active retention and nibble construction |
| `first_object_stop_flags` | Producers of the two formerly unresolved object-related stop qualifiers |
| `decode_hold_input_enums`, `hold_variant_4_allowed`, `update_hold_flag` | Variant-selection predicate and the separate sequential hold-latch update |
| `model_acceleration`, `model_torque` | Nested integer vehicle-model equations |
| `primary_torque_output` | Primary torque seed/filter/slew ordering; conversion and shaping supplied by callbacks |
| `ratio_torque_output`, `auxiliary_torque_number` | Separate numeric outputs; auxiliary hold/flag policy is explicitly outside the numeric excerpt |
| `publish_brake_acceleration` | Final publication-stage slew toward the calibrated brake envelope |

## What the feedback is doing

The controller compares measured acceleration with delayed versions of the
selected request. P and I use different references. Integral presets on
engagement, certain request states and actuator transitions coordinate the
feedback with the powertrain boundary. The main integral remains enabled in
brake mode in this calibration.

Its ordinary active sum is selected request + P + I + mapped dynamics correction
when enabled. Generic firmware also contains a reference-rate term and an
auxiliary integral, but both stay zero from initialization with these calibration
values. `update_feedback()` specializes to that fact. A request-bit override
instead ramps toward capability and bypasses the ordinary sum.

The dynamics path produces two different results. Its numeric correction enters
the sum and allocation threshold. Its class changes gains and output/model
branches. Class −1 is prohibited below **40 km/h**; class +1 can affect low-speed
output conversion. Both classifier inputs share the same acceleration sensor source, with different
conditioning and reference accelerations. Neither class should receive a
physical slope label merely from its sign.

## Why brake/torque selection is more than the sign of acceleration

The decision boundary includes minimum-powertrain acceleration, speed-dependent
hysteresis, mapped dynamics and request state. A positive corrected acceleration
can still select brake below that boundary.

The ordinary brake target subtracts the same mapped correction added by feedback,
but that correction still influences the selection threshold. Some retention
branches instead use corrected acceleration directly, or preserve prior outputs.
A generic subtraction rule for every branch would be incorrect.

Stop/hold is separate from outer brake ownership. The normal 0xB→0xA→torque
sequence follows from the previous-submode interlock. Force-torque branches can
bypass it. The object-derived stop qualifiers, OEM standstill and special timer
are distinct inputs. Low speed alone does not select 0xB.

On torque entry, the acceleration side can select minimum capability and the
primary torque routine independently seeds both its command and filter from the
capability-adjusted minimum torque. These are coordinated state transitions.

## Established versus remaining

The audit now supplies branch-level translations of request selection, active
feedback, allocation, brake submodes and hold-latch predicates. It recovers a
missing twelve-state upstream state machine, the aliased stop-flag producers,
and the second dynamics input's output-pointer mapping. The sensor arithmetic, auxiliary torque number, ratio output and hold-input
enum mapping now have executable excerpts. Their boundary conditions remain
explicit inputs: sensor acceptance, bias learning/blend, residual status gates
and auxiliary flag/timer policy are not silently replaced with defaults.
Model adaptation, response-history scoring and the upstream supervisor remain
untranslated stages, with comments at their call sites. The verifier now checks 80,000 recovered-C snapshots and 6,000
carried-state request/feedback/allocation cycles against recovered C.

Still unresolved are some physical enum/signal meanings, full fault-to-exit
timing, the endpoint of the extra-output block transfer, and whole-firmware
runtime equivalence. The transfer enable itself is resolved: stored record 8
must read as 0x5a; its actual value on a particular module is a runtime input. The recovered logic does not identify an EBCM pressure-control law.
Details and reproducible evidence are in the audit and
[ascm_reference_evidence/README.md](ascm_reference_evidence/README.md).

## Source map

| Reference stage | Firmware address |
|---|---|
| Caller, model reload, main sequence | `131440`, `139e50`, `139d80` |
| Dynamics input/filter/classification | `81410`, `79b00`, `484c0`, `1344b0` |
| Second dynamics input | `e3050`, `dfe90`, `dfad0`, `e31f0` |
| Request and feedback | `13ade0`, `13a5d0`, `13a570` |
| Allocation, submodes, hold | `13afc0`, `13a180`, `133960` |
| Object stop flags | `130cc0`, pointer `4001d7e0 -> 4001dcb0` |
| Torque and model | `13a360`, `139ce0`, `1399a0`, `13bb20`, `13bbc0` |
| Adaptation and response history | `13b6c0`, `13b910` |
| Recovered upstream state machine | `138c90..13926f`, startup descriptor `40220` |

Firmware source files are under
`/home/acremins/volt_reverse_engineering/ASCM/decoded/`.
ACC calibration 23366550 uses big-endian fields at file offset `0xa0 + offset`.
The evidence directory records hashes and selected exports. Python preserves
relevant integer divisions but generally omits machine overflow and narrowing.
The native comparison checks are against recovered C, not CPU emulation.

See [the remaining-question review](ASCM_REMAINING_QUESTIONS.md) for the gap
assessment after tracing the dynamics sources and extra-output consumers.

See [ASCM_RAMPS.md](ASCM_RAMPS.md) for calibration plots and pseudocode showing
how acceleration targets pass through allocation, slew limits and the final
brake envelope, with downloadable SVG and CSV artifacts.
