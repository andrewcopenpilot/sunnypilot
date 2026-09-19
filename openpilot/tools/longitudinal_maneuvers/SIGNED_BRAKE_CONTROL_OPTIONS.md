# Signed brake control options — 2026-09-18

Design review after route `0000007a--37e2cdee0a`, while the speed-triggered
+3/+6/+10/+15/+20/+200 suite is being driven. No controller behavior changed in
this review. Results from that new suite are not yet incorporated.

Update after the ASCM input audit: production feedback must be limited to
signals traced into the stock longitudinal loop. See
[ASCM_LONGITUDINAL_INPUTS.md](ASCM_LONGITUDINAL_INPUTS.md). Numeric hydraulic
pressure has not been established as such an input; the earlier pressure-based
handoff recommendation is withdrawn. Pressure remains a test-log diagnostic.

## The decision to make

The sign of desired vehicle acceleration does not identify the required actuator.
The relevant boundary is the acceleration the car would produce with the brake
controller released and the powertrain at its minimum available torque.

Illustrative examples, not measurements:

| Condition | Acceleration at minimum torque with brakes released | Desired acceleration | Required action |
|---|---:|---:|---|
| Flat-road creep below natural creep speed | +0.20 m/s² | +0.05 m/s² | Retain braking, reduce it enough to accelerate gently |
| Downhill | +0.80 m/s² | +0.10 m/s² | Retain braking despite positive acceleration |
| Uphill | −0.20 m/s² | 0.00 m/s² | Release braking and request more powertrain torque |

Negative desired acceleration can also require positive powertrain torque on a
sufficiently steep uphill. Avoid using either the sign of acceleration or a
fixed speed alone as the ownership decision.

Keep the domains explicit: the EBCM receives a signed vehicle-acceleration
request; the HPCM receives torque in Nm. They are not complementary force
commands that can simply be added or interpolated. The EBCM also participates in
regen blending, so zero friction pressure alone does not prove that EBCM control
and powertrain-only control are equivalent.

## What was rechecked in the ASCM

Decompilations below are under
`/home/acremins/volt_reverse_engineering/ASCM/decoded/ghidra_longitudinal/mpu1/`.

- `FUN_00139d80.c` calls capability preparation, request selection, acceleration
  feedback, allocation, and torque output in that order.
- `FUN_0013afc0.c` uses different entry/retention tables depending on previous
  actuator mode, a capability term, a filtered disturbance correction, and
  upstream request state. Ordinary retained-brake branches pass corrected
  acceleration minus the disturbance term to the signed brake request, without
  a blanket upper clamp at zero.
- `FUN_0013a360.c` initializes torque output and its filter from the reported
  minimum torque on entry to torque mode. Subsequent cycles filter and slew
  torque. In brake mode it uses the fixed calibrated torque request, −650 Nm in
  this calibration.
- `FUN_0013a5d0.c` adjusts reference-filter and integral state on transitions.
  The calibration enables brake-path PI. This supports coordinated feedback and
  handoff, not copying an integrator reset everywhere.
- `FUN_001399a0.c` converts a bounded minimum torque to acceleration. Calibration
  offsets `0x68e/0x690` are −5000/0: stock caps this particular intermediate at
  zero torque. Preserving positive AxleTorqueMin in a creep estimate would be our
  extension, not a recovered OEM rule.

Calibration source: `ASCM/decoded/23366550.bin`, big-endian values at file offset
`0xa0 + calibration_offset`; SHA-256
`de42f846cf8852e987af67f453ce98cf75835d63ffbdab677cbc9d847c497030`.
Rechecked `0x78c=600`, `0x78e=800`, `0x81c=50`, `0x81e=0`, `0x834=-650` and
byte flags `0x6ba=1`, `0x83c=1`. In the ordinary branch described in the earlier
review, stock adds disturbance correction upstream, then subtracts it again on
the brake output. It also affects selection thresholds. Adding the same hill
compensation independently to both commands would not reproduce this structure.

Some upstream state-bit meanings remain unresolved. These facts support the
architecture; they do not justify transplanting every branch or claiming that
stock holds arbitrary sub-1-mph speeds.

## Current implementation gaps

`gm/carcontroller.py:stock_gas_brake()` already has mode hysteresis, live minimum
torque, torque feedforward and a minimum-torque handoff seed. However:

1. `target = min(accel, 0.) * brake_scale` removes positive brake-path requests.
2. `gm/values.py:regen_accel_available()` uses `min(t, 0.)`, so the selector does
   not see the positive minimum torque observed during creep.
3. Without grade/disturbance compensation, that capability calculation describes
   the nominal road-load model rather than the actual slope.
4. LongControl's PI knows its overall acceleration limits but not downstream
   command scaling, ownership changes or torque slew limits.

At 1.5 mph with positive AxleTorqueMin, the current clamp gives a nominal
capability near −0.079 m/s² and a retained-brake exit threshold near +0.043 m/s².
Consequently, removing the command clamp alone provides only a narrow positive
range before the existing selector exits braking. The current 0.8 creep scaling
also means corrected acceleration and the actual brake request differ.

## Option 1: enable signed requests within the current allocator

Keep the existing mode selection and torque path. Permit a bounded positive
brake request while brake mode is retained. Preserve the existing negative-side
calibration initially, explicitly handle the positive side, and log both the
corrected acceleration and transmitted signed request.

The existing integral can then raise the signed request to reduce braking when
the car accelerates too slowly, or lower it to increase braking when it accelerates
too quickly. Avoid resetting it merely because the request crosses zero.

**Benefit:** the smallest controlled experiment; answers whether ordinary PI can
make useful fine adjustments through signed EBCM requests.

**Limit:** the unchanged allocation boundary can still release braking too early
on a downhill or discard useful creep-torque context. This is a low-speed
experiment, not a complete hill solution. Broadly increasing a fixed retention
threshold instead would risk sluggish uphill handoff. Do not tune that threshold
and the PI gains simultaneously in the first comparison.

## Option 2: coordinate handoff using ASCM inputs and state

Retain brake and torque modes, signed EBCM requests, minimum-torque capability,
and separate entry/exit margins. Use acceleration error, request history and
previous actuator mode to coordinate feedback across the transition. On exit,
withdraw EBCM control, initialize torque from a valid minimum-torque input, then
filter/slew toward the target. Keep explicit stop/hold handling separate.

This option no longer uses pressure to decide whether braking has released.
ASCM status bits may eventually help, but their physical meaning must be traced
before assigning them that role. Acceleration shortfall alone also cannot
identify residual braking versus insufficient powertrain torque during a delay.

**Benefit:** improves the transition and PI behavior using established stock
input categories, without a pressure sensor dependency.

**Limit:** this is a design direction, not yet a complete hill-aware selector.
The capability/disturbance boundary in option 3 is still needed to distinguish
positive acceleration with braking downhill from a need for torque uphill.
Trace the unresolved ASCM correction inputs before claiming OEM equivalence.

## Option 3: model-based capability with a slow learned correction

Estimate acceleration at minimum powertrain torque on the current road:

```
a_min_powertrain = accel_from_torque(T_min, speed) + external_accel
```

Here `external_accel` is our explicitly defined residual, positive when the road
adds forward acceleration. It is not an assertion about the OEM variable's sign.
Use a filtered/bounded positive AxleTorqueMin where validated, rather than
clamping all positive values away. Combine nominal feedforward with a small,
slow correction from measured response.

Compare desired vehicle acceleration with this estimated boundary, with separate
entry and exit margins. Below it, retain EBCM control and send a signed vehicle-
acceleration request; above it, use torque conversion with the road contribution
removed once. This naturally allows positive acceleration with brakes downhill,
and torque for zero or mildly negative acceleration uphill.

Learn a residual such as `a_measured - accel_from_torque(T_actual, speed)` only
when braking is demonstrably absent, signals are valid and transitions are
settled. During friction braking that residual includes brake deceleration; it
cannot be treated as grade. Filter and bound the estimate, avoid learning from
pedal interventions, and retain feedback for stale estimates or grade changes.

**Benefit:** anticipates the correct handoff and is closer to stock's capability
plus disturbance architecture. Fits the earlier preference for a precomputed
model with measured torque providing a nudge.

**Cost/limits:** more estimation and validation work. AxleTorqueMin is a
state-dependent capability signal, not a direct grade measurement; actual torque,
regen availability and road load can differ. The learning gate must use verified control state and valid settled response;
do not introduce pressure as a production gate. The residual formula above is
our candidate estimator, not a recovered OEM formula. Trace the unresolved
stock correction inputs before choosing its implementation.

## Integral state and stopping: common requirements

The integral must remain able to move the signed brake request through zero and,
when needed, transfer control to torque. Uphill error should release braking and
then increase torque; downhill error should increase braking. Do not freeze I
throughout creep, or interpret it as hydraulic pressure.

The required steady correction can differ between EBCM acceleration control and
powertrain torque control, particularly on a grade. Blindly preserving the same
number can create a jump; clearing it unconditionally loses useful correction.
Track/reseed feedback at a handoff to match the initialized actuator output, and
apply anti-windup to actual limiting/slew behavior. Keep any slow road estimate
separate from transient PI correction so grade compensation is not counted twice.
The stock transition presets are inspiration, not a verified formula to copy.

Reserve stopping/hold behavior for explicit stopping intent and the appropriate
vehicle state. Moving slowly, requesting zero acceleration, or crossing zero in
the brake request is not by itself a reason to enter mode 0xB or 0xD. The OEM
0xD→0x9→0x1 launch sequence is a separate hold-exit question, not the moving-creep
handoff being designed here.

## Development sequence tied to evidence

1. Use the current six-level test to establish release delay, partial-pressure
   response and whether returning to zero arrests acceleration. +200 tests large
   release authority; it should not become a routine creep command by default.
2. Make the signed-path experiment from option 1, with existing gains and clear
   low-speed scope. Measure speed error, acceleration error, pressure, torque and
   mode switches. Keep the acquisition/suite logic independent of controller gains.
3. Add option 2's coordinated transition behavior as its own feature. Test flat creep, uphill
   release-to-torque and downhill acceleration-with-braking separately. Targets
   are repeatable tracking, no sustained brake/torque oscillation, and no lurch
   from feedback state carried across the transition. Exact tolerances should be
   chosen from the new logs, not invented from the two existing repeats.
4. Add option 3's slow correction only if logs show systematic grade/capability
   errors or excessive handoff delay that feedback alone does not resolve.

The upcoming logs may change the recommendation: if low positive requests
produce only all-or-nothing release or an unacceptably long dead time, do not
assume a linear signed acceleration PI will solve creep merely because the
protocol accepts the values.
