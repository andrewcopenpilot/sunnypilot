# ASCM dynamics and output follow-up

Scope: MPU1 OS 84876565, VSC 84059606, DYN 84059607, vehicle configuration
23366555 and ACC 23366550. This continues [the loop audit](ASCM_FIRMWARE_AUDIT.md).
Addresses below are firmware addresses; offsets are bytes unless an array index
is explicitly shown. The findings come from local firmware, not an OEM drive.

## What is now clearer

The two inputs to the −1/0/+1 classifier share an acceleration sensor source.
One is a filtered sensor-versus-vehicle-acceleration difference. The other is a
separately conditioned sensor-versus-wheel-acceleration residual. They are not
two independent physical sensors, and neither is directly an angle or percentage.

**Correction to the earlier audit:** the path to `bf9b0` does not run through
`cb120`. That routine processes a neighboring channel. The relevant chain is
`cbc10 -> cbdb0 -> cc070/cbf30 -> cc8e0`. Resolving the output offsets and the
stack arguments distinguishes two easily confused outputs: the residual's input
and the acceleration estimate that already uses disturbance compensation.

The auxiliary torque and ratio fields have a confirmed consumer in a raw memory
transfer table. No actuator-command consumer of either numeric field was found
in the traced MPU1 command path. The auxiliary routine still has control-relevant
side effects: it updates the hold latch and vehicle flags.

## Shared sensor source and exact output mapping

```text
8-byte CAN 0x140, signed low 12 bits of bytes 4/5, divided by 64
  -> 484c0 -> c32c0/c32d0
     |-> 1344b0: subtract 4001d938, integer filter -> first classifier input
     |
     `-> ce970 input +0x10
          -> c8eb0 working +0x29c
          -> cbc10 working +0x58             conditioned first sensor channel
          -> cbdb0 working +0x50             geometric correction and bounds
          -> cc070/cbf30 working +0x44       initialized bias subtracted
          -> cc8e0 working +0x38             validity selection / retained value
          -> cd920 final output +0x44 = 400101d4
          -> cecd0 -> bf9a0/bf9b0
          -> e3050 input +0x14 -> dfad0      sensor minus wheel comparison
          -> e31f0 -> c1240/c1250
          -> 1344b0: multiply by 1000 -> second classifier input
```

The sensor-processing object is `4000fac0`; `cd920`'s working base is object
+0xc and its final-output base is object +0x6d0 = `40010190`.
In the C export, `param_2` is a four-byte-element array: `param_2[0xe]` means
working **+0x38**, while `param_6[0x11]` means output **+0x44**. Mixing array
indices with byte offsets leads to the wrong sensor branch.

The neighboring final output +0 (`40010190`, published by `bfa00/bfa10`) comes
from working +0x34. That is the blended, disturbance-compensated branch.
`dfad0` receives **bf9b0**, not bfa10. This distinction matters because `c1250`
is also fed back into the sensor processor to compensate the neighboring
acceleration estimate; it is not subtracted on the bf9b0 branch itself.

## Sensor conditioning and bias: recovered arithmetic

For the first channel, `cbc10` accepts new data only when its status and fault
gates allow it. Consecutive accepted samples use coefficient **0.21**
(VSC +0x69c); an initial/reaccepted sample seeds the state directly. When the
acceptance predicate is false, the stored sensor value remains unchanged.

`cbdb0` adds `VCFG[0x30] * z`, where `z` is working +0xac. The coefficient is
**0.00693000015**. It clamps the product and then the sum through `cbd70`, whose
bounds are **−16.0, +15.99951171875** (flash `141674`, `141670`). The physical
name of `z` is not assigned here. It is a separately processed channel, not the
wheel residual. This is more specific than assuming an unmodified CAN sample.

In the first `cbf30` call, let `s` be the conditioned/corrected sensor value,
`b0` the initialized bias, `b` the adaptive bias bounded to ±0.981, `d` the
filtered disturbance compensation and `w` the blending factor. Its two numeric
outputs are:

```text
uncompensated = clamp(s - b0, -16, 15.99951171875)
compensated   = clamp((1-w)*(s - b0 - d) + w*(s - b), same bounds)
```

These outputs are selected/retained separately by `cc8e0/ca5c0`. The
**uncompensated** output is the one ultimately published by bf9b0.
Here “uncompensated” means no subtraction of `d`; sensor conditioning and
initialized-bias subtraction have already happened.

The missing arguments in Ghidra's `cc070 -> cbf30` call are recoverable from
assembly. In the first call at `cc506`, argument 22 points to stack +0x68;
`cbf30` stores the uncompensated result there. `cc610..cc618` copies that value
to working +0x44, as established by the caller's argument at `ce130..ce134`.
The blended result instead goes through stack +0x64 to working +0x3c.

`c8df0` initializes `b0` (working +0xc0) from `4000d7f8` once, guarded by its
initialization flag. `cc070` subsequently updates `4000d7f8` from the adaptive
bias output. That does not make `b0` an every-cycle copy of the adaptive bias.
The storage path is now traced: `12c090` defaults the bias to zero; `bc380`
reads record **100** through `45410/b5770` into `40037764`, and copies its fifth
float (`40037774`) into `4000d7f8` on a successful read. `bc9d0` copies the
updated bias back into that record and submits it through `45460/b67a0`.
The record descriptor at `14e5b0` gives a 36-byte payload and a zero-filled
default at `14ddac`. This supports persistence across sessions, unlike the
per-cycle-overwritten mass estimate. A save request is not proof that a
particular vehicle's storage write completed; replay needs the actual starting
record or must explicitly assume the zero default.

`ca5c0` uses the new value only if all five supplied acceptance/fault conditions
are zero; otherwise it uses the retained value. `ca610` saves the selected
value for the next call. The remaining uncertainty is the external meaning and
production of every fault flag, not whether this branch retains prior data.

## Wheel comparison and the second classifier input

`e1390` derives wheel-channel acceleration from a change in its motion estimate
divided by elapsed time, then applies its distance/radius-related scale.
`e15e0 -> e1c30/e1af0 -> e1e10 -> e2bd0 -> e3900` carries four such derivative
outputs to `c1680/c16b0/c16e0/c1710`. The chosen final fields trace to the
**derivative** outputs; nearby speed outputs are different fields.

DYN +1 is **0**, so `dfad0` selects the average of `c16e0` and `c1710`.
Other values select the other pair (1), or all four (neither 0 nor 1).
The exact axle/wheel names are not necessary to establish the derivative role
and are not assigned here.

For accepted/retained sensor input `u` and selected wheel acceleration `a_w`,
the numeric part of `dfad0` is:

```text
wheel_target = clamp(a_w, u - 2.37930012, u + 2.37930012)
wheel_filtered += alpha * (wheel_target - wheel_filtered)
residual_filtered += 0.118100002 * ((u - wheel_filtered) - residual_filtered)
limited_residual = clamp(residual_filtered, -2.37930012, +2.37930012)
output += 0.00999999978 * (limited_residual - output)
```

`alpha` is 0.01999999955 while its rejection/retention condition is true,
otherwise 0.118100002. Initialization flags seed the corresponding states rather
than applying these recurrences. The unclamped `residual_filtered` is saved
before its clamp; the last output has separate state. This distinction matters
when reconstructing transients.

The 10 ms task calls the sensor processor first, wheel processing next, then the
residual estimator (`bcfc0`, calls at `bd074`, `bd09e`, `bd0f2`). Thus sensor
conditioning reads the previously published residual/wheel values, while
`dfad0` sees the newly published conditioned sensor and wheel derivatives.
A sequential replay must preserve this order and the slower 40 ms ACC sampling.

**Established interpretation:** an acceleration-domain sensor/wheel discrepancy,
with initialization, validity retention, filtering and saturation. Positive
means sensor-derived acceleration exceeds the filtered wheel comparison.
Gravity projected along the sensor axis is a plausible contributor, as are
sensor bias, pitch transients and wheel-estimation errors. The equations alone
do not identify which contributor caused an observed value or prove an
uphill/downhill sign convention.

`1344b0` itself reads the two numbers without checking their accompanying
validity getters. Do not add an automatic “invalid means zero class” rule to
that routine. Upstream fault handling and system disengagement remain separate. In particular,
`1333f0` tests `c3060()==0x24` (the status paired with c32d0) and sets fault
aggregate `4001d967`; `132c70` then includes that aggregate in `4001d8e0`.
Thus the lack of a local validity test in the classifier does **not** mean
that the full ACC system ignores a bad sensor.

## Extra outputs: consumer search and its limits

The reference scan covered all listed code/data references and scalar operands
targeting `4001d7d0..4001db00` (47 functions). It includes accesses expressed as
base-plus-offset, such as the caller's `4001d8b0 + 0x234` output pointer.
The output pointer is passed through `139d80` to feedback, allocation,
`13a360` and `13a180`; their output-field accesses were also inspected.

| Field | Confirmed use in the traced control path |
|---|---|
| +2 / `4001dae6` brake acceleration | Final envelope shaping and `c26a0` publication |
| +4 / `4001dae8` primary torque | Feedback gating and `c26d0` publication |
| +6 / `4001daea` ratio output | Written by `13a360`; prior value copied to `4001e172`; no subsequent numeric control use found |
| +8 / `4001daec` auxiliary torque | Written by `13a180`; prior value feeds that routine's own slew state `4001e176`; no actuator publication found |

A scan of two-byte-aligned 32-bit literals in the OS found a pointer to the
output block in flash at **14d5e0**. Its record at **14d5d8** is:

```text
00440000 00000014 4001dae4
record tag      length=20   source address
```

This is record 42 (zero-based) in the 61-record table at `14d3e0`, referenced
by table directory entry `14d6c8`. `b36a0` passes the record's source and length
to `b3300`, and `b3620/b3710` sequence the headers and blocks. `b3300` programs
hardware transfer registers, including source at `fff45620`, count at
`fff45628` and destination `20000000`. The 20-byte block includes both numeric
fields. This is a confirmed block-transfer consumer, not evidence of another
actuator command. The receiving endpoint remains unestablished. The enable is now resolved:
`b3380` reads stored record **8**, length one, and sets `4000a168=1` only if the
read succeeds and the value is **0x5a**. The descriptor at `14dff0` points to a
zero default at `14d7d8`. `b3570` can request changing this stored byte; therefore
the firmware default disables the path, but an actual module's stored value
cannot be inferred from the OS image.

The evidence supports treating these as **computed internal outputs with a
recording/transfer path**, rather than adding imagined actuator effects to the
reference. It is not a proof of absence of every possible indirect consumer,
other processor use, or diagnostic memory read. The hold and status writes in
`13a180` must still be modeled even if its auxiliary torque number is unused
by the actuator publisher.

## Next evidence that would close the remaining questions

1. Correlate CAN 0x140 with a known sensor definition or synchronized vehicle
   data to establish sender and physical sign. The initialized-bias storage
   lifecycle is now recovered; actual stored values remain runtime inputs.
2. Follow `b3300`'s transfer endpoint if the goal includes
   determining whether these internal values can be observed during operation.
3. Replay the recovered stages in scheduling order with recorded inputs/state.
   Recovered-C comparisons alone cannot establish real timing or OEM behavior.

Exports, assembly argument checks, transfer-table bytes, calibration values and
reference-scan results are preserved in
[ascm_reference_evidence](ascm_reference_evidence/README.md). No production
controller or firmware image was changed.

## Hold inputs: extended receive map recovered

The earlier receive list stopped at 153 standard-frame entries. The next
**39 entries** are extended-frame filters, not an unrelated data table.
`a8460` matches extended identifiers using **ID & 0x03ffff00**; the low eight
bits and upper priority bits are not part of this software key. `a87e0` uses
the message-index permutation to check DLC, run the callback and copy data to
the raw buffer. The three relevant callbacks simply accept the message.

| Filter key | List / message index | Buffer | Field / downstream enum |
|---|---|---|---|
| `0x00630000` | 190 / 165 | `400049dc` | byte0 bit0 -> c61d0 -> d959 |
| `0x00608000` | 191 / 167 | `40004a54` | byte0 bits0/1 -> c62a0/c62c0 -> d95a |
| `0x00336000` | 177 / 175 | `40004a60` | byte0 bits0/1 -> c6200/c6220 -> d95b |

All three have DLC 1. The local `gm_global_a_lowspeed.dbc` defines CAN
**0x10630000**, byte0 bit0, as **DriverDoorOpened**. Its identifier matches the
first filter exactly after masking, and its bit position matches `79250`.
This corroborates the door interpretation with both a receive mapping and a
signal definition. `d959=1` means the getter indicated open; `d959=2` is the
other branch and can include non-1 invalid getter values, so it should not
unconditionally be called “door closed.”

The other two physical labels are still unknown. They now have concrete filter
keys and payload bits for a CAN-definition search or synchronized observation;
there is no need to search arbitrary IPC slots for these particular inputs.
Do not label them seat belt or parking brake solely because those would be
plausible hold-related signals.

In `132fb0`, d95a is 0 when c62c0 is nonzero, otherwise 1 when c62a0==1, else 2.
d95b is 1 when c6200==1 and c6220==0, 2 when both are zero, otherwise 0.
`133960`'s variant-4 predicate remains:

```text
calibration enabled AND speed < 3 km/h
AND (d959 <= 1 OR d95a in {0,1}) AND d95b in {0,2}
```

This helps identify the conditions for selecting the variant, but does not
supply the EBCM's physical meaning for mode 0xC versus 0xD.
