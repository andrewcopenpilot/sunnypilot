# Staged implementation toward stock-like GM ACC

Basis: the current `ascm_loop_reference.py`, `ASCM_FIRMWARE_AUDIT.md`,
`ASCM_DYNAMICS_AND_OUTPUTS.md`, and the route 7b signed-request results.
This is a proposed development plan; it does not change vehicle control.

## Objective and integration boundary

First obtain smooth moving creep, including small accelerations with friction
braking still present and a repeatable handoff to propulsion. Then add the
recovered dynamics correction and explicit stop/hold/release sequencing.

Keep openpilot's planner as the source of desired acceleration and stop intent.
Adapt the recovered downstream controller to that interface. OEM request
candidates, perception enums, and supervisor flags do not have established
one-to-one openpilot equivalents. Do not invent equivalent values to make a
nominally complete OEM port run.

Use the signal categories established in the ASCM loop: vehicle speed and
acceleration, actual/minimum/maximum axle torque, the relevant drivetrain and
engagement states, and eventually the verified sensor/wheel dynamics inputs.
Pressure remains a diagnostic measurement, not a new production control input.

Initial vehicle validation is on the tested Volt gateway configuration. Shared
code can remain suitable for other GM vehicles, but Volt calibration and sensor
availability must not be assumed fleet-wide. Existing signed Panda/interceptor
limits remain -400 to +200; this plan requires no additional limit expansion.

## 1. Establish a measurable baseline and explicit control state

Relevant code: `stock_gas_brake()` in `opendbc_repo/opendbc/car/gm/carcontroller.py`,
model/calibration helpers in `values.py`, and `LongControl` in
`openpilot/selfdrive/controls/lib/longcontrol.py`.

Extract the existing GM allocation state into a small component while preserving
its behavior. Distinguish actuator owner, brake request, torque request, brake
submode, and active bit. Keep the explanatory firmware reference independent
from runtime code: it mixes raw integer and SI excerpts and has unresolved inputs.

Log the planner request, corrected request, P and I contributions, references,
current/previous owner, prepared minimum capability, entry/exit thresholds,
pre/post-shaping requests, limits, submode, and transition reason. Record these
at their actual control update times. Reuse existing log fields where meanings
match; add a small explicit debug record for missing internal decisions.

Extend the existing sequential comparison only as needed to cover the adopted
stages, including output state written back for the next cycle. Recovered-C
agreement checks arithmetic; recorded-data replay checks interfaces and timing.
Replay with recorded vehicle feedback is not a prediction of how the vehicle
would respond to different commands. Neither is a substitute for a live test.

Exit criterion: the extracted baseline reproduces existing command decisions
on representative creep, engagement, and handoff traces, and the diagnostic
record explains each transition. Obtain a short current closed-loop baseline;
route 7b is a direct-command test and cannot supply closed-loop tracking metrics.

## 2. Enable useful signed brake control while moving

The present brake target is `min(accel, 0) * brake_scale`. Remove that zero clamp
in the selected moving-creep path and bound the signed request explicitly through
to packing. Preserve mode 0xA for negative, zero, and positive requests while the
allocator owns the brakes. Stopping remains a separate decision.

This must include a usable brake-retention boundary. Currently the margin is
half the recovered OEM table: +0.125 rather than +0.250 m/s² at zero speed.
With a positive received minimum torque, the existing capability conversion
clamps its modeled torque to zero, yielding about -0.079 m/s² capability. Around
1.5 mph, the current exit threshold and 0.8 brake scale allow only about +3–4
counts before leaving brake mode. Merely allowing signed values would miss the
+6/+10 partial-release range demonstrated by route 7b.

Restore the recovered brake-retention margin in the selected creep region as
part of this functional change. Preserve the entry threshold, feedback gains,
0.8 demand scale, and torque shaping for this comparison. Keep existing output
bounds and use explicit active state rather than the sign of the packed count.
The 0.050 request-state offset is not itself the OEM ownership hysteresis and
should not be stacked onto a recovered margin without an explicit mapping.

Test: fixed-time speed cycles 1.5 -> 2 -> 1.5 mph and 1 -> 1.5 -> 1 mph, two
runs each. Confirm positive requests occur while owner remains BRAKE and mode
remains 0xA; assess speed response and whether mode cycling decreases. A request
crossing zero must not independently trigger a torque handoff.

Exit criterion: repeatable partial release under feedback, no unintended stop,
and no persistent brake/torque oscillation. This stage does not establish grade
handling or sub-1-mph performance. If response oscillates, inspect the logged
feedback/allocation sequence before changing several gains together.

## 3. Reproduce the primary torque handoff more closely

Port capability preparation and primary torque transition treatment as separate,
reviewable changes. The current code already seeds torque from live minimum
on a creep brake exit and already has the OEM-style torque slew rates. It lacks
the recovered command filter and the complete capability adjustment.

The ASCM lowers its prepared minimum when actual torque is below the reported
minimum, then uses that adjusted value for the transition seed. Validate actual,
minimum, and maximum torque inputs and freshness before adopting this arithmetic.
Keep raw torque capability distinct from the minimum-acceleration model: the
OEM minimum-path model clamps converted torque to nonpositive values. Passing
positive creep torque straight through that model would be an extension, not a
faithful restoration of stock behavior.

Seed both the torque command and its filter from prepared minimum, then apply
the recovered filter and slew on subsequent torque-owned cycles. Account for
these states in disengagement and reengagement. The torque-side acceleration
seed and the Nm output seed are distinct stages.

Test: creep -> 3 mph -> creep, including repeated crossings of the ownership
boundary and throttle interruption/reengagement. Compare handoff jerk, speed
overshoot, output continuity, and immediate reversals of ownership.

Exit criterion: a single intended handoff without repeated reversals or a
propulsion surge. Match recovered arithmetic offline; evaluate comfort against
the preceding accepted vehicle baseline.

## 4. Give feedback and allocation a coherent update order

Target architecture: one GM-specific coordinator owns acceleration feedback,
allocation, and output shaping at the existing 25 Hz actuation cadence. Common
openpilot code retains the longitudinal engagement/stop-state interface.

Today generic `LongControl` runs feedback at 100 Hz and sends an already corrected
acceleration to the 25 Hz GM allocator. Its Volt P and I use the same delayed,
filtered reference. The OEM uses a delayed P reference, a separately filtered I
reference, and feedback that sees previous owner/hold before allocation chooses
new owner. Its delay state is itself filtered.

First make the raw planner acceleration and the common stop/engagement decision
available through an explicit interface. When GM feedback owns correction,
bypass the existing PI correction for that configuration; never stack both PI
loops or silently change the meaning of `actuators.accel` for every platform.
Wire its P/I/output diagnostics back into the appropriate logs.

Adopt in separate comparisons:

1. Reference timing, independent P/I references, and explicit previous-cycle
   ownership, initially retaining current gain magnitudes.
2. Transition initialization and bounded integration/anti-windup using actual
   output limits and owner state. Preserve the ability of the I contribution to
   move demand in either direction. OEM transition presets exist; do not assume
   stock simply preserves or clears I on every handoff. At <=1 m/s its preset
   gain is zero, and raw accumulator units matter.
3. Recovered gain schedules and P filtering as a candidate calibration. Do not
   simultaneously replace timing, gains, and demand scale. OEM Kp is 0.02–0.20;
   Ki is 0.225 at <=5 m/s, but these numbers alone do not reproduce its response.

The unusually large P-filter table values are direct filter weights, not time
constants in milliseconds. Preserve units and update rate. Retain explicit final
command limits even where OEM internal arithmetic has no independent I clamp or
only approaches an envelope by slew.

After this is stable, independently test removing the empirical 0.8 creep brake
scale to approach the OEM acceleration mapping. Do not remove it during the
first signed-request comparison.

Exit criterion: reduced tracking error and overshoot, no sustained limit-induced
I growth, and smooth engagement/owner transitions. Existing direct-command
profiles remain characterization references, not closed-loop acceptance tests.

## 5. Add the recovered dynamics correction for grade changes

Start with passive decoding/replay. The eight-byte 0x140 source must be verified
on the actual available bus, including sign, scaling, and validity handling; it
is distinct from the three-byte turn-signal message. Establish which available
wheel channels reproduce the traced derivative inputs. Recover or explicitly
bound the starting sensor bias instead of assuming a stored value is known.

Implement the two distinct sensor/vehicle and sensor/wheel residual paths with
the recovered conditioning, initialization, and retained-state behavior. Their
10 ms task ordering differs from the 40 ms ACC loop. Their residual is not a
measured road angle, and injecting already disturbance-compensated acceleration
into the uncompensated branch would create the wrong feedback path.

Once passive behavior is credible, enable the numeric correction and allocation
weights as one coordinated feature: ordinary feedback adds the mapped correction,
ordinary brake output subtracts it, and ownership thresholds use their own
weights. Adding an independent hill feedforward to every output would count the
same effect twice. Preserve the recovered class +1 rolling adjustment at the
output-model stage, after capability preparation, when that feature is adopted.

The class -1 branch is gated below 40 km/h. Do not introduce its reduced Ki or
alternate torque slew into creep as a supposed OEM downhill feature.

Test: identical creep speed profiles on level ground, then mild uphill/downhill,
including crossing from a grade onto level ground. Confirm I can increase brake
demand downhill and release braking/advance to propulsion uphill without rapid
owner switching. Add steeper grades only after those responses are repeatable.

Exit criterion: improved grade-transition tracking without persistent bias or
an abrupt torque change. Unresolved source identity/sign/validity blocks enabling
this feature, not the earlier moving-creep work.

## 6. Add explicit stopping, holding, and launch sequencing

Use openpilot's stop intent as an explicit integration input. It is not proven
equivalent to the OEM perception enums. A small positive creep target alone
must not select stopping merely because speed is low.

Represent owner, brake submode, active retention, and hold as separate state.
Adapt recovered 0xA/0xB/hold/release ordering using confirmed inputs. Hold updates
occur after allocation and affect the next cycle. The recovered ordinary path
can include a 0xB -> 0xA cycle before torque ownership; force-torque branches can
bypass it. The post-hold active timer produces a possible 0x9 interval separately
from the normal braking request and eventual 0x1.

Validate each piece separately: creep -> requested stop, stationary hold, then
launch. Do not assume a fixed 0x9 dwell alone proves the EBCM retained request
has cleared, or map unidentified hold-input enums to guessed driver conditions.

Exit criterion: stop without an unintended restart, hold without repeated apply/
release cycles, and launch without a pressure/torque surge. Preserve the ability
to cancel and interrupt; exercise those transitions in the state tests.

## 7. Expand operating range and simplify

After moving creep, grades, and stop/launch pass, expand the revised controller
through the existing creep blend boundary and then the broader speed range.
Review transition continuity and regression behavior before removing the initial
speed restriction. Validate additional GM vehicles against their signal units,
calibrations, and actual responses before claiming fleet equivalence.

Remove superseded empirical patches only after an isolated comparison shows
that the replacement makes them unnecessary. Do not copy disabled reference-rate
or auxiliary-I terms, the mass update overwritten every cycle, or auxiliary/
ratio numbers with no established actuator publication. Their relevant hold/
state side effects are separate from those unused numeric outputs.

## Compact test cadence and proposed acceptance targets

Reuse the same short closed-loop suite across revisions. Start at 1.5 and 1 mph;
add 0.5 mph after those pass, then 0.25 mph when measurement and stopping margins
permit. Use fixed-duration holds and explicit deadlines so failure to stabilize
produces a recorded failure rather than preventing the test from running.
Two runs per profile are the initial screen, not statistical proof.

Proposed initial targets for settled level-ground 1–2 mph holds: mean absolute
speed error <=0.15 mph over the final three seconds of an eight-second hold,
overshoot <=0.30 mph, and no unintended stop. Track peak/filtered jerk and RMS
error against the preceding accepted baseline. A monotonic transition should
not produce repeated brake/torque ownership reversals; grade-limited cases must
be distinguished from controller oscillation. Record timeouts and failed runs
alongside successful runs.

At every live stage verify actual downstream request values/modes, timing,
interceptor health and Panda counters. These are proposed test gates, not
performance already demonstrated by route 7b. The next implementation consists
of baseline/state visibility followed by the signed-request/retention change;
feedback gain replacement and dynamics compensation follow later.
