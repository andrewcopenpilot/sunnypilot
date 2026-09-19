# ASCM longitudinal firmware audit, 2026-09-18

This audit checks MPU1 OS **84876565** and ACC calibration **23366550** against
[the Python reference](ascm_loop_reference.py). It changes study files only.
It establishes control-flow and arithmetic behavior; it does not establish the
EBCM's hydraulic response or prove equivalence to an observed OEM drive.

## Corrections that change how to read the loop

1. **The main function is not the whole cycle.** `131440` reloads the vehicle
   model through `139e50`, calls the inner loop `139d80`, then reshapes and publishes
   its commands. The earlier overview omitted the model reload and final shaping.
2. **Two extra feedback terms are inactive in this calibration.** Table `0x768`
   is entirely zero; reference-rate feedforward stays zero from initialization.
   Auxiliary-integral gain `0x74a` and bound `0x762` are zero. Its accumulator also
   remains zero from initialization. Their presence in generic firmware is not
   evidence of an additional active creep controller.
3. **Class −1 cannot activate during creep.** `4001d934` is signed speed in
   0.01 km/h. `0x69a=4000` prohibits negative classification below **40 km/h**.
   This excludes both its reduced integral-gain branch and its alternate torque
   slew branch at creep speeds. Class +1 has no equivalent speed gate.
4. **The adaptation update is overwritten.** `13b6c0` writes `4001e158`, the mass
   field. `139e50` unconditionally reloads that field before the next inner-loop
   call. Do not describe this path as a persistent learned mass used next cycle.
   Its counters and residual filters persist; its mass write does not survive
   the caller's next reload. This conclusion concerns this traced caller.
5. **Torque handoff may use an adjusted minimum.** `139ce0` lowers the minimum
   to actual torque if actual is below the received minimum, and adjusts its
   modeled actual-torque slot by the same discrepancy. `13a360` seeds from that
   resulting minimum slot, not necessarily the untouched CAN minimum.
6. **The final brake envelope is approached, not hard-clamped.** `131440` clamps
   a temporary target, then slews from the *current allocation result* toward
   it at 10 m/s³. For example, +3.0 m/s² becomes +2.6 in one 40 ms call even
   though the upper envelope is +2.0. The result overwrites the brake slot and
   becomes the next allocation's previous brake demand.

## Inner-loop state map

All offsets here are bytes. Bits use least-significant-bit numbering, **not**
the bit numbers printed in PowerPC `se_btsti` instructions.

| Base | Important fields |
|---|---|
| `4001dc90` powertrain | +2 minimum torque, +4 maximum, +6 actual, +8 adjusted/model actual; +0xe/+0xf gear states |
| `4001d998` vehicle | +0 speed (0.01 m/s), +2/+4 acceleration (0.001 m/s²), +8/+0xc/+0x14 status words |
| `4001dc80` request | +0 candidate A, +2 candidate B, +0xc request flags |
| `4001dea0` capability | +0 filtered model capability, +2 actual acceleration, +4 minimum, +6 maximum, +0xa rotational ratio, +0xe predicted speed |
| `4001deb4` feedback | +0 selected, +2 corrected, +4 P, +6 I, +8 auxiliary I, +0xa rate term, +0xc mapped dynamics, +0xe previous selected, +0x10 corrected copy |
| Same feedback block | +0x18 request history; +0xe0 ring index, +0xe2 delay, +0xe4 stable-request timer, +0xe6 active timer, +0xe8 hold, +0xea I reference, +0xec P reference, +0x293 request state |
| `4001dae4` allocation/output | +0 torque-path acceleration, +2 brake acceleration, +4 primary torque, +6 ratio output, +8 auxiliary torque, +0xa owner, +0xe submode |
| `4001e148` model | +0x10 mass, +0x12 circumference, +0x14 drag coefficient, +0x16 minimum-path efficiency, +0x1a rolling coefficient, +0x1c acceleration factor |

The two owner histories are distinct. At feedback time, allocation +0xa is the
last cycle's selected owner, while `e171` records the owner preceding that
allocation. This is how feedback detects the transition one cycle later.
The integral-reset branch clears `e184`; allocation can set it again later in
the same cycle. Never carry the allocation latch independently of feedback.

## Request selection: states have concrete arithmetic meanings

`13ade0` decrements `e1a4`, then selects in this priority order. A and B are
upstream acceleration candidates. I is the previous main integral contribution;
`amin` is the prepared minimum-powertrain acceleration.

| Condition | State | Selected value |
|---|---:|---|
| request bit26 clear | 0 | 0 |
| A == B and current gear byte nonzero | 2 | A |
| B == +3.000 and gear nonzero | 4 | A |
| A == −6.000 | 3 | B |
| B + I < amin | 1 | B |
| amin < A + I | 1 | A |
| otherwise | 1 | max(A, amin) |

The last expression is **not** `amin - I`. Assembly `13aeaa..13aeca` supplies
A and amin to `12e590` (max); the old decompilation omitted both arguments.
Sentinels +3000/−6000 are raw milli-acceleration values at `0x7a6/0x7a8`.

After this selection, request bit28 scales the request using `0x7de` at predicted
speed. Vehicle +0x14 bit24, or a remaining `e1a4` timer, also forces state 3;
that bit reloads the timer to 50 cycles. Otherwise request bit27 and a positive
previous selected request force state 4 and use speed table `0x7ea`.
These are raw logical roles, not recovered pedal/switch labels.

**Table-order trap:** `0x7de` contains `(200,1000), (100,500), (0,100)`.
`12e3e0` assumes ordered traversal but does not sort. Consequently its actual
result is 1000 at arguments ≤200 and 100 above 200, not an interpolated ramp.
`13aefc` loads the argument with signed `e_lha`; treating Ghidra's `undefined2`
as an unsigned host integer gives the wrong answer for negative predicted speed.

## Feedback: what actually runs

`update_feedback()` now translates the active branches for this calibration.
All calculations below refer to raw milli-acceleration unless SI is stated.

- The 100-entry request ring receives the **previous selected request**. Delay
  lookup floors delay/dt and clamps to 0..99 samples; it does not interpolate.
  Normal delay target is 120 ms in torque and brake. Vehicle +0x14 bit24 chooses
  1000 ms. A gear mismatch in torque mode grows the delay target by one dt.
  The delay itself is filtered with integer weight `400/dt`.
- P reference is the delayed ring value. I reference is that value filtered
  with weight `100/dt`. Both errors subtract measured acceleration. Previous hold,
  or vehicle +0x14 bit24 together with a negative selection, sets both errors to 0.
- Request bit26 clear resets the main accumulator. Rising enable, request bit24,
  request states 3/4, or a detected torque/brake transition presets it. The
  preset is `max(amin, (filtered_capability - measured_accel) * lookup(0x73e,v))`
  in **accumulator units**, then the contribution is accumulator/1000. At speeds
  ≤1 m/s the preset gain is zero. States 3/4 while already enabled filter this
  preset against `e1ac` with weight `2000/dt`. Resetting the I reference happens
  after this cycle's error was computed: it does not recompute that error.
- Otherwise integration requires absolute previous corrected request ≤5 m/s²,
  absolute selected request ≤5 m/s², absolute I error ≤10 m/s², zero auxiliary
  accumulator, and prior primary torque ≤`Tmax + trunc(2.5*Tmax)`. That last gate
  is not simply “command ≤ maximum torque.” Gain `0x736` is 0.225 at ≤5 m/s and
  rises to 0.600 at ≥15 m/s. Class −1 with `d990==1` halves the increment.
  There is no independent main-integral clamp in this routine.
- Kp is 0.020..0.200 from table `0x74e`, indexed by
  `abs(selected) + 2*abs(P_error)`. The P contribution is zero when the active
  timer is zero. Otherwise its filter uses the **table result directly as a
  filter weight**, not as milliseconds divided by dt. `0x756` returns weights
  1000, 300, 200 at active times 500, 1000, 2000 ms. This is heavy smoothing.
- Ordinary corrected acceleration is selected + P + I + mapped dynamics when
  enabled. The rate and auxiliary terms remain zero with these calibration values.
- Request bit25 replaces the ordinary sum with a capability ramp. First it
  slews toward amin at −1.5/+3.0 m/s³; request bit23 adds a second slew toward
  amax at ±2.0 m/s³. Owner/direction and a vehicle status bit clear its active
  flag. This override does not add mapped dynamics.

The integer filter is `(previous*weight + target)/(weight+1)`, with division
toward zero and a one-count step if rounding would stall. Thus a “2000 ms” filter
at 40 ms uses weight 50 and gain 1/51, not exactly a 2.000-second continuous filter.

## Allocation, stop/hold and output

`allocate_acceleration()` includes states 0..4 and retention branches.
For states 1/2, the threshold is amin + a speed margin + a weighted mapped
dynamics correction. Previous brake owner uses `0x708` and weight 0.4;
other owners use `0x714` (or conditional `0x720`) and weight 0.2. State 2 adds
0.050 m/s²; state 1 adds zero. Brake retention includes amin because `0x83c=1`.
The low-speed margins are +0.250 for brake exit and −0.065 for ordinary entry.

Below the threshold, ordinary brake demand is corrected minus mapped dynamics.
Entering brake assigns it immediately: the entry preset is disabled (`0x806=0`).
Already in brake, it slews at ±5 m/s³ (`0x810` is constant 5000). Therefore entry
and subsequent demand changes do **not** have identical slew behavior.

Above the threshold, ordinary release requires no OEM standstill, a nonzero
special timer, hold clear, and previous submode not 3. A set `e184` seeds the
acceleration side at amin. If hold/submode blocks release, both prior numeric
outputs and the owner are retained. Standstill or expired special timer instead
retains brake and assigns corrected directly, with no correction subtraction
and no write to the old torque-acceleration slot. State 3 uses a separate
brake-or-forced-torque branch; state 4 forces torque.

Submode priority is fully represented in `select_brake_submode()`: off/suppressed
→1, hold below 1.5 m/s→4/5, qualified stop with previous brake owner→3, else→2.
Submode 5 reloads active retention to 62 integer cycles, and the publication stage
decrements it in that same cycle. The CAN mode combines submode with a separate
active bit, so submode 1 can produce 0x9. The normal sequence 0xB→0xA→torque has
one intervening control cycle. Force-torque branches can bypass it.

The special timer is separately controlled by signed speed <−0.5 km/h. Forward
or stationary operation reloads it to 125 cycles; it is not a five-second
stationary stop trigger. Its helper sets it to zero immediately or counts down,
depending on the separate enable argument.

`update_hold_flag()` translates both sequential predicates in `13a180`. A clear
in the first test can be followed by a set in the second test. There is no speed
or pressure test in these predicates. Hold affects the **next** allocation;
its auxiliary-torque calculation uses the newly updated hold decision now.

The auxiliary output at allocation +8 has its own behavior. In the ordinary
brake branch it converts brake acceleration to torque and applies
`min(converted_torque, -40 Nm)` (`0x83a`). Entry seeds it from the powertrain
block's +0 torque input; continuing brake can slew at ±10000 Nm/s when request
bit22 is set. That bit is set by `131440` immediately before the inner loop.
Outside brake the ordinary auxiliary output is zero. In the hold branch the
converted acceleration is P + I + rate −4 m/s², with the same ±10000 Nm/s slew.
The auxiliary output is distinct from the published primary torque command.
The follow-up found a raw block-transfer consumer of this field, but no actuator
publication in the traced MPU1 path; see [the consumer trace](ASCM_DYNAMICS_AND_OUTPUTS.md).

The primary torque routine converts torque-path acceleration through the model,
then applies sign-dependent efficiency (0.88 here). It seeds both command and
filter from the capability-adjusted minimum when entering torque. Continuing
torque uses filter weight `150/40=3`, downward slew −4000 Nm/s, and upward slew
1000→600→500 Nm/s at 0→5→30 m/s. Outside torque, primary command is −650 Nm.
The ratio-dependent output is calculated separately and is also −650 outside
torque; its existence does not establish a second independent acceleration loop.

Final brake publication has lower-envelope points `(speed m/s, accel m/s²)`:
`(0,-1.5), (1.5,-1.5), (2.5,-2), (5.5,-5), (11.6,-4.4), (20.5,-4.4),
(25,-3.5), (30,-3.5)`, upper +2.0, and the 10 m/s³ envelope approach described
above. Powertrain enable is separate: it requires owner 1 or 2 and upstream
state byte `4001d9c6` in 2..4. A torque number alone is not an enabled command.

## Vehicle model, adaptation and history

`model_acceleration()` and `model_torque()` preserve the nested integer divisions
of `13bb20/13bbc0` without overflow/narrowing. Dimensional interpretation is:

```text
a ≈ [ (T/r − drag*v²)/mass − rolling*g ] / acceleration_factor
T ≈ r * [ mass*(acceleration_factor*a + rolling*g) + drag*v² ]
```

Calibration supplies mass 1776 kg, circumference 2.032 m, drag 0.250 N/(m/s)²,
rolling coefficient 0.008 and acceleration factor 1.0. These physical labels are
inferred from the equations and scale factors. Integer radius is 323 mm.
Minimum torque is converted with its own negative-path efficiency, then clamped
to −5000..0 Nm. Positive CAN minimum does not enter this model as positive creep
capability. Class +1 temporarily adds `0x7fa` to the rolling coefficient **after**
capability preparation: at speeds ≤2 m/s, 0.008 becomes 0.048 for subsequent output
conversions. This adds roughly 0.392 m/s² of modeled resistance; it is an active
class-dependent path the earlier torque excerpt did not display.

`13b6c0` compares integral residuals collected in positive and negative request
windows, above 10 m/s, and attempts to update the mass field. The next caller
reload overwrites that mass update, as noted above.

`13b910` accumulates the I reference and measured acceleration until elapsed time
is ≥100 ms. With a 40 ms invocation this commits every **120 ms**. Its subsequent
history lookup nevertheless assumes a 100 ms sample interval. The nominal
three-second comparison therefore spans 3.6 seconds at this scheduling rate.
It forms demeaned request/response differences and a filtered 0..100 score;
it is not an additional integral controller. Do not relabel that score as a
validated physical “response quality” without tracing its consumers.

## Dynamics: resolved arithmetic versus physical interpretation

The CAN `0x140` eight-byte signed field and its filter/classification translation
remain consistent with the firmware. Table `0x774` maps the filtered difference
roughly as 0.7333 times the input, with saturation at ±2.2 m/s². Classification
requires both inputs, not just this mapped correction:

- Positive evidence: second input >0.500 and raw filtered difference >0.500.
  Counter activates at +25 and saturates at +50 at 40 ms.
- Negative evidence: second input <−0.275 and filtered difference <−0.375.
  Below 40 km/h the counter resets; otherwise it activates at −25 and reaches
  a lower limit of −31 (1250/40 integer division).
- Without either evidence condition, the counter moves one step toward zero.

The second input's previously missing pointer mapping is now resolved:
`e3260` operates on object `40010e98`; `dfe90`'s final output is object +0x160
(`40010ff8`). `dfad0` writes its residual to working-state +0, copied to final
output +0xc (`40011004`). `e31f0 -> c1240 -> c1250` publishes that value.
This is **not** output +4, the separate vehicle-motion estimate.

In `dfad0`, input `bf9b0` is compared with a selected pair/average of four
wheel-processing outputs `c1680/c16e0/c16b0/c1710`. The selection byte at DYN
calibration +1 is zero here, selecting the latter pair in the function's
parameter order. The wheel comparison is bounded to the input ±2.379300,
filtered (coefficient 0.02 or 0.1181 depending on state), subtracted from the
input, filtered by 0.1181, bounded to ±2.379300, and filtered again by 0.01.
Initialization flags bypass the corresponding filters on first use. This
computation runs in the 10 ms vehicle-dynamics task, not the 40 ms ACC task.

The input `bf9b0` is published by `cecd0` from `400101d4`. **Follow-up correction:**
its processing is `cd920 -> cbc10 -> cbdb0 -> cc070/cbf30 -> cc8e0`, with
validity retention and initialized-bias subtraction. `cb120` belongs to a
neighboring channel and was incorrectly included in the earlier audit. The four comparison outputs come
through `e3750 -> e2bd0 -> e3900`, including wheel processing and derivative paths.
The [follow-up](ASCM_DYNAMICS_AND_OUTPUTS.md) establishes that this path shares
the same `c32d0` sensor source as the first classifier input, and distinguishes
its uncompensated output from the adjacent disturbance-compensated estimate.
These findings support an acceleration-disturbance interpretation. They do not
by themselves establish an OEM grade signal, pitch angle, slope percentage, or
sending ECU. The sign of a physical hill still needs signal-level corroboration.

## Recovering the missing upstream state machine

The old `138c90` export was only 96 bytes of recognized function body and ended
at an unresolved indirect jump. The complete function occupies `138c90..13926f`.
A startup copy descriptor at flash **0x40220** contains:

```text
source 0x154fe0 -> RAM 0x4001d7d0, length 0xe68
```

It places the twelve-entry jump table at flash `0x155070` into RAM `4001d860`.
Restoring these exact bytes in a **read-only Ghidra session** and extending the
function body recovers all cases 0..11. The recovery script and recovered C are
in [ascm_reference_evidence](ascm_reference_evidence/README.md).

Assembly `131d2e..131d4c` also resolves an omitted ninth argument: `1397c0`
receives state base **4001d9b8**. The recovered state machine consumes that block;
it is distinct from the object-record flags at `4001dcc0`. Restoring the
initialized object-array pointer resolves those flags through a different path
(described below), preventing conflation of similarly structured flag words.

Request bit26 is the enable consumed by the inner loop; bit25 selects the
capability ramp, bit24 can force torque, and bit23 changes that ramp/allocation.
The recovered state machine shows their producers and transitions. For example,
upstream states 8/9 set bits26/23 and clear bit25; state9 sets bit24 while state8
clears it. States5/10 set bit25 during their release sequence. Upstream states
are not the inner request states 0..4 and are not the CAN brake submodes.

## The formerly unresolved stop flags: an aliased object record

The same startup-copy descriptor initializes **4001d7e0 to 4001dcb0**.
`130cc0` walks six records with stride 0x44; record zero's flag word at +0x10
is exactly **4001dcc0**. Its source is a six-record, 64-byte-per-record list
from `c2c20` (buffer `400371a8`). The incoming first record's byte +0x3c
sets these fields:

```python
flag28 = (object_state == 1)                       # via 4001dc78
flag27 = (object_state == 2) or (old_dc7a and flag28)  # via dc79
dc7a = flag27
```

Thus object state 2 can remain represented by flag27 through a following state 1.
The flag clears when neither condition holds. These are object-derived stop
qualifiers, not additional EBCM pressure or pedal signals. They are written
before allocation in the same ACC scheduling sequence. The previous direct-xref
scan missed the writes because they use the initialized pointer plus record offset.

The list publisher is `13cfe0 -> c2b80`. In this calibration (`0x8d8=0`),
`13d3c0` maps its selected internal object's byte +0x1b to output +0x3c through
`13d570`. Values 0..4 pass through; other values become 0. This recovers the
producer chain without assigning unsupported stationary/stopped/moving labels
to the perception enum.

`133960` also resolves the hold-variant predicate. Calibration `0x5de=1`
enables variant 4 only when speed < **3 km/h** (`0x5e4=300`),
`d959 <= 1 or d95a in {0,1}`, and `d95b in {0,2}`. `132fb0` builds those enums
from getters `c61d0/c62a0/c62c0/c6200/c6220`. This is separate from the allocator's
<1.5 m/s hold gate and from the hold latch itself. The follow-up maps c61d0 to
the extended-CAN driver-door-open signal, and locates the other two fields at
filter keys 0x00608000 and 0x00336000. Their physical names and the EBCM
distinction between variants 4 and 5 remain unresolved.

## Remaining limits, with concrete evidence needed

| Unresolved | What would close it |
|---|---|
| OEM physical names, sender and validity policy for the dynamics fields | Trace remaining sensor normalization/bias helper ABIs and corroborate with a known CAN definition or synchronized OEM data |
| Physical names for first-object states 1/2 | Corroborate the perception enum; the complete pointer/producer chain and sticky transition are now recovered |
| Hold/suppression/override physical labels | Driver-door signal and two other hold receive mappings are recovered; correlate the remaining fields with definitions or traces |
| Extra-output transfer endpoint and enable | A raw 20-byte block-transfer consumer is confirmed; no numeric actuator use was found in the traced MPU1 path. Follow its hardware endpoint/enable if needed |
| Behavior at every runtime state | 70,000 stage snapshots and 6,000 carried-state request/feedback/allocation cycles pass against recovered C; binary/OEM trace comparison and supervisor reachability remain |
| EBCM response to a signed request and submode | EBCM firmware or measurements; ASCM arithmetic alone cannot supply this answer |

The reference is substantially more complete, but the whole vehicle control
system is **not fully solved**. Unknown labels above are not silently substituted
with “grade,” “pedal,” “ABS,” or “hold pressure.”

The [remaining-question review](ASCM_REMAINING_QUESTIONS.md) records the next
evidence needed and the scope of the state-carrying sanity check.
