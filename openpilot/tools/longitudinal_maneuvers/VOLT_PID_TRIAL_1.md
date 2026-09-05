# Volt ASCM longitudinal gain trial 1

Baseline: `edff7a668d`, containing the 15 brake/release trials and six stop/hold trials.
Use that baseline commit to record the added stops before testing the new gains. It is an experimental candidate, not a validated improvement.

| Setting | Baseline | Trial |
|---|---|---|
| P gain | 0 | 0.10 |
| I gain at 5 m/s and below | 2.40 | 1.92 |
| I gain at 35 m/s and above | 1.50 | 1.20 |
| I gain between breakpoints | Linear interpolation | Linear interpolation |
| D gain | 0 | 0 |
| Feedforward | Target acceleration | Target acceleration |

The gain-only candidate comes from the earlier historical-data model estimate,
including acceleration-feedback noise. It reduces integral gain by 20% and adds
a small proportional correction. It does not include the proposed inverse actuator
feedforward, whose candidate gains are different.

This POC branch sets P directly to 0.10 in LongControl and updates the existing GM
ASCM I values to [1.92, 1.20]. There is no vehicle-specific trial gate. These gains
apply during PID control for both acceleration and braking, including ordinary
driving outside maneuver mode. Production scoping belongs in a separate upstream change.

Actuator mapping, acceleration limits, stopping ramp, integrator reset on stopping,
and maneuver commands are unchanged. Low-speed PID gains clamp to the 5 m/s values;
the new baseline stop trials are needed to assess that region. A successful approach
to zero speed does not establish that final brake hold or planner-controlled stops
are fixed.

First inspect the baseline stop rlogs for engagement, low-speed acceleration,
oscillation, actuator output and stopping-state transitions. Then, if this remains
an appropriate candidate, repeat the same 21-trial suite on the same road/direction
and similar battery charge. Compare response error and oscillation by speed band,
not only mean deceleration. Confirm ordinary planner-controlled stops separately.
Record the software commit with each route.

Unit checks exercise the configured gain schedule, actual P/I/feedforward output,
and unchanged stopping/disengagement behavior.
They cannot establish on-car stability or improved stopping comfort.
