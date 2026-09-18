# Longitudinal Maneuvers Testing Tool

Test your vehicle's longitudinal control tuning with this tool. The tool will test the vehicle's ability to follow a few longitudinal maneuvers and includes a tool to generate a report from the route.

<details><summary>Sample snapshot of a report.</summary><img width="600px" src="https://github.com/user-attachments/assets/d18d0c7d-2bde-44c1-8e86-1741ed442ad8"></details>

## Current Volt default: brake characterization

The default for the Volt ASCM in longitudinal maneuver mode is **12 release
profiles, two runs each: 24 attempts total**. Direct releases run first, followed
by application-history checks and gradual descents. The previous sweeps and
hold profiles are preserved but are not included in this default suite.

Each attempt:

1. Settle at **3 mph for two seconds** using normal control.
2. Enter ordinary active brake mode **0xA** with **5 counts for two seconds**.
3. Ramp from 5 to the profile's peak at **0.5 count/second**, then hold the exact
   peak for the time listed below. Counts are rounded onto CAN, so the transmitted
   peak begins approximately one second before the exact requested peak.
4. Apply the listed release command or descending steps. Hold the **final count
   for eight seconds**, including when it is zero. Intermediate gradual steps
   last 1.5 seconds each; the final eight-second hold replaces that step duration.
5. End at profile completion or if speed leaves **0.4–2.0 m/s (0.9–4.5 mph)**,
   including a standstill indication. All guards remain active during release
   and zero-count holds. A guarded endpoint is useful data, not a completed hold.
6. The screen says **"Brake test ended"** with the endpoint reason. Stopping
   intent remains asserted until a throttle tap or disengagement. Recover to
   **3 mph** after acknowledgement, then advance to the next repeat or profile.

Every row below runs **twice consecutively**. Durations are per run and exclude
setup, stopping, acknowledgement and recovery.

| ID | Peak and exact-peak hold | Release sequence | Full duration | Question answered |
|---|---|---|---:|---|
| R01 | 12 for 4 s | Directly to 0 for 8 s | 28 s | Does active zero release pressure already applied? |
| R02 | 12 for 4 s | Directly to 5 for 8 s | 28 s | Does a large nonzero reduction release pressure? |
| R03 | 12 for 4 s | Directly to 8 for 8 s | 28 s | Is moderate reduction sufficient? |
| R04 | 13 for 3 s | Directly to 0 for 8 s | 29 s | Does zero release after a stronger application? |
| R05 | 13 for 3 s | Directly to 5 for 8 s | 29 s | Does the 5-count result survive a stronger application? |
| R06 | 13 for 3 s | Directly to 8 for 8 s | 29 s | Does the 8-count result survive a stronger application? |
| R07 | 12 for 4 s | Directly to 2 for 8 s | 28 s | Does near-zero differ from zero and 5? |
| R08 | 12 for 4 s | Directly to 10 for 8 s | 28 s | Does a longer observation change the previous retention result? |
| R09 | 12 for 2 s | Directly to 0 for 8 s | 26 s | Does shorter application history change zero-demand release? |
| R10 | 12 for 2 s | Directly to 5 for 8 s | 26 s | Does shorter application history change nonzero release? |
| R11 | 12 for 4 s | 10 → 8 → 6 → 4 → 2 → 0; 1.5 s steps, final 0 for 8 s | 35.5 s | Can a gradual descent locate the release region? |
| R12 | 12 for 4 s | 11 → 10 → … → 1 → 0; 1.5 s steps, final 0 for 8 s | 44.5 s | Do smaller, slower steps behave differently? |

The suite has approximately **12 minutes of measured profiles** if every attempt
completes, plus setup, acknowledgement and recovery. The gradual profiles run
last because retaining pressure at intermediate levels may reach the lower speed
guard before zero. The direct profiles provide independent chances to observe
zero and low-count release without traversing those intermediate holds.

During measurement, gas/regen stays at **−650 Nm** and brake mode stays **0xA**,
including the full zero-count hold. Zero does **not** mean inactive brake mode,
a torque handoff, or the end of the test. Setup, recovery, and endpoint or
invalid-command stopping retain their existing behavior. PI and the experimental
brake-demand scaling do not alter these direct commands.

Application is timed, not triggered by a pressure threshold. Check the logs to
verify that each run actually developed pressure before release. A run with no
pressure to begin with is not evidence of successful release. The 13-count
profiles provide additional application cases; they do not isolate peak magnitude
from hold duration because their exact-peak hold is shorter to preserve speed.

For each release, compare pressure before the drop, onset and extent of pressure
reduction, speed, acceleration, delivered axle torque and AxleTorqueMin. Pressure
is in raw units, and changing speed/torque can affect it. A reproducible active
zero release enables work on brake-demand reduction and torque handoff. If zero
retains pressure too, the next separate experiment is active-brake disengagement;
this suite does not mix mode switching into the numeric-demand comparison.

This is **EBCM demand characterization, not direct hydraulic-pressure control**:
the EBCM still blends braking internally, and constant commanded gas/regen does
not guarantee constant delivered axle torque. Keep full CAN rlogs. One command
count is a protocol unit, not a measured pressure or demonstrated physical
acceleration increment.

Direct commands require per-drive `LongitudinalManeuverMode`, Volt gateway
hardware, engaged longitudinal control, valid CAN, and a fresh plan no older than
250 ms. Stale/invalid commands latch stopping until the test request ends; the
screen reports **"controller stopped test"** and waits for acknowledgement. Pedal overrides or inactive
longitudinal control cancel the direct output. Normal driving defaults this path
off. The old acceleration suite is used on unsupported configurations.

### Plot the release response

After fetching the route's full rlogs, run:

```sh
python openpilot/tools/longitudinal_maneuvers/plot_brake_characterization.py \
  '/path/to/drive_NAME--*/rlog.zst' --output /path/to/brake_report
```

The report writes PNG/PDF time traces for requested/sent brake counts, filtered
and raw speed, acceleration, and raw pressure. `command_response.png` compares
speed, acceleration, and pressure against **actual CAN brake counts** across
repeats. Per-trial CSVs also include brake mode, gas/regen request, engagement,
and pedal state. Endpoint reasons are preserved in `trials.json`.

Use the traces to locate where pressure and deceleration begin changing, then
check whether that location repeats. Speed integrates acceleration, so a bend
in speed alone is not a steady-state brake calibration. No automatic inflection
finder or fitted pressure model is used.

The default profiles are built by `brake_release_maneuvers()` in `maneuversd.py`.
Their descriptions include R01–R12, the mode, peak hold, and release sequence.
The active alert shows the current requested count. Compare each repeat
separately and exclude fallback stopping commands after a guard triggers.

To select a previous suite instead, set `MANEUVERS` to:

- `BRAKE_HOLD_MANEUVERS`: nine earlier 11/12/13-count hold-and-release attempts.
- `BRAKE_SWEEP_MANEUVERS`: three earlier 5–20-count sweeps at 0.25 count/second.
- `STANDARD_MANEUVERS`: the preserved acceleration suite described below.

Only the selected suite runs.

## Preserved acceleration comparison suite

The following section describes `STANDARD_MANEUVERS`, not the current Volt
sweep default. Set `MANEUVERS = STANDARD_MANEUVERS` to run it again.

The suite contains **22 runs: eleven creep scenarios, each repeated twice**. The
original eight scenarios remain first, with identical active commands, durations,
and order for comparison with the previous 16-run drive. Setup and recovery now
use 3 mph instead of the earlier 8 mph excursions; compare the measured entry
speed and acceleration when evaluating results across that change. Three moving transition
scenarios follow. The test portion starts at 3 mph or below. The old higher-speed braking and regen trials have
been removed.

Every run follows the same sequence:

1. Reach **3 mph** and settle there for **two continuous seconds** while showing
   the upcoming test.
2. Perform the creep test below. The three added moving tests first request
   **-0.15 m/s²** and start their timed commands on the first downward crossing of
   **1.0 m/s (2.2 mph)**; they do not require stable creep.
3. Return to **3 mph** and stay near that speed for three seconds before advancing.
   Stop-and-hold tests wait for driver acknowledgement first, as described below.

Setup and recovery target 3 mph, with a 0.1 m/s settling tolerance. They use up to
+0.75 m/s² acceleration and -0.5 m/s² deceleration. The stop timeout starts when the
actual test begins, excluding setup and recovery.

| Runs | Command after settling at 3 mph | What it measures |
|---|---|---|
| 2 | -0.15 m/s² to standstill, hold 3 s | very gentle approach and extended creep-speed tail |
| 2 | -0.3 m/s² to standstill, hold 3 s | normal creep stop and brake hold |
| 2 | -0.5 m/s² to standstill, hold 3 s | firmer low-speed stopping transition |
| 2 | stop at -0.3, then three 0.1 s pulses at +0.05 m/s², hold 3 s | brief stop-flag interruptions |
| 2 | stop at -0.3, then three 0.3 s pulses at +0.05 m/s², hold 3 s | repeated stop-flag flapping |
| 2 | stop at -0.3, then three 0.4 s pulses at +0.08 m/s², hold 3 s | longer, stronger creep requests during a hold |
| 2 | -0.4 for 2 s, 0 for 4 s, -0.15 for 4 s, 0 for 2 s | crawl near 0.5 m/s, gentle braking to a stop, and release |
| 2 | -0.3 for 2 s, -0.15 for 2 s, 0 for 3 s, +0.15 for 2 s, 0 for 3 s | feathering the brake and re-entering positive torque at creep speed |

All accelerations are in m/s². Pulse tests drop stopping intent during each pulse;
pulses start one second after first reaching standstill and are spaced 1.5 s apart.
The final three-second hold only counts after the last pulse. Zero target acceleration
is speed holding, not a guarantee of zero gas or brake actuation.

### Added moving transition trials (runs 17–22)

The earlier timed crawl could overshoot into the stopping controller before its
zero-acceleration interval. After the 3 mph setup, these additions
request a fixed -0.15 m/s² until measured speed first reaches 1.0 m/s or below.
The timed profile starts immediately after that crossing, without a speed-hold
or acceleration-settling requirement. The former two-second hold near 1.8 mph
blocked every added trial in route 68, so it is no longer a prerequisite.

Both approach and active commands are acceleration requests without added speed
correction. The initial speed and acceleration remain visible in the rlogs;
compare those initial conditions when evaluating different drives. Starting at
1.0 m/s leaves more room for braking overshoot before the low-speed guard.

| Runs | Commands after crossing 1.0 m/s | What it measures |
|---|---|---|
| 17–18 | -0.15 for 0.5 s, then 0 for 6 s | speed drift, residual braking, and brake-mode chatter near zero requested acceleration |
| 19–20 | -0.15 for 0.5 s; 0, +0.05, -0.05, +0.15, -0.05 for 1 s each; +0.3 and -0.15 for 0.75 s each; 0 for 1 s | small positive requests while braking, followed by torque handoff and brake re-entry |
| 21–22 | -0.15 for 0.5 s; linear ramp -0.15 → +0.3 → -0.15 over 4 s; 0 for 2 s | transition hysteresis and acceleration discontinuities under a gradual request |

All accelerations are in m/s². A small initial braking request exercises the
brake path; confirm actual mode from CAN, since PI-corrected actuator acceleration
can differ from the planner request. A zero-acceleration request tests whether
speed stays steady; it does not impose a target speed during the active trial.

During acquisition or the active trial, standstill, speed below **0.4 m/s**, or
speed above **1.5 m/s** invalidates the run. Acquisition also times out after
**20 seconds**. The screen shows **"Creep test invalid: tap throttle or disengage"** with the
reason. Until acknowledgement,
stopping intent stays asserted. Then recover to 3 mph with longitudinal control
active; that failed attempt advances to the next repetition or scenario so one
poorly tracked trial cannot block the rest. Its outcome is logged as **failed**,
not completed. Interruptions before any failure still retry the same attempt.
The report marks an aborted active trial invalid; acquisition failures are
logged but have no active interval to plot. Normal stop/resume logic is retained.

These trials exercise moving control above the GM standstill threshold, not
0.2 mph crawling or launch from rest. Existing stop and feather trials remain
regression checks for those transitions. For analysis, compare acceleration
error, speed drift, brake-mode switch count, pressure release, and torque jump
at handoff alongside `AxleTorqueMin`. The added trials need their own baseline
run with the old controller and the same revised entry procedure for an exact
before/after comparison; the first 16 runs can be compared directly with the previous drive.

### Stops, recovery, and status

A stop must report standstill with speed below 0.1 m/s and then hold for three
continuous seconds. Movement resets the hold timer. Until the hold is complete,
the screen says **"Maneuver Active: holding stop"**.

After **"Stop complete: tap throttle"** appears, tap the throttle
to acknowledge the completed hold. The tool releases stopping intent and recovers to
3 mph once longitudinal control is active again. Alternatively, disengage, manually
move above the minimum engagement speed (3 mph on this branch), and re-engage to
recover. Completed stop holds do not automatically launch without acknowledgement.

The two original timed crawl tests and successful added moving trials enter recovery
automatically after their timed commands. Failed moving trials wait for acknowledgement first.
If stock cruise holds the car stopped, tap the throttle when **"Test complete: tap throttle"** appears.
While moving, the screen says **"Recovering to 3 mph"**. A run is only counted after
the 3 mph recovery has settled. This includes the final run; then the screen shows
**"Maneuvers Finished"**. Take control to end the drive.

During longitudinal maneuver testing, the low-speed steering warning is suppressed
so test progress and completion remain visible. Normal driving retains the warning.
Other alerts and the actual steering-assist speed limit are unchanged.

A stop/hold that has not completed within **20 seconds of braking onset** shows
**"Stop timed out: take control"**. Pulse trials allow 30 seconds.
A timed-out stop maintains stopping intent until takeover; disengage and re-engage
to retry the same run. Interrupting setup or an unfinished test also restarts that
run from the 3 mph setup. Interrupting recovery pauses it; re-engagement resumes
recovery without repeating the completed test.

Alerts identify the run number and phase. Phase changes, failed attempts, and completed trials are
also written to the log. Keep full rlogs, including CAN, for torque and controller
analysis; the generated report alone does not include all of that feedback.

Record the software commit and the pack voltage at rest (or state of charge) for
each route, and keep the same road direction when comparing tunes.

## Instructions

1. Check out this branch on your comma device so the targeted sequence is used.
2. Locate either a large empty parking lot or road devoid of any car or foot traffic. Flat, straight road is preferred. Leave enough room for the 3 mph setup and recovery on every run. Disengage and take control before turning around.
3. Turn off the vehicle and set this parameter which will signal to openpilot to start the longitudinal maneuver daemon:

   ```sh
   echo -n 1 > /data/params/d/LongitudinalManeuverMode
   ```

4. Turn your vehicle back on. You will see the "Longitudinal Maneuver Mode" alert:

   ![videoframe_6652](https://github.com/user-attachments/assets/e9d4c95a-cd76-4ab7-933e-19937792fa0f)

5. Ensure the road ahead is clear, as openpilot will not brake for any obstructions in this mode. Once you are ready, press "Set" on your steering wheel to start the tests. For the default Volt release suite, allow 24 attempts (12 profiles, two runs each) and acknowledge each endpoint. For the preserved acceleration suite, allow 16 original runs and six added moving attempts (22 total). The first 12 are stop-and-hold trials requiring acknowledgement before recovery; the next four are the original timed crawl trials, followed by six moving transition attempts. A failed moving attempt requires acknowledgement and recovery before advancing. Press "Cancel" to disengage before turning around. Re-engage only when ready on the next clear, straight section; an interrupted trial starts over unless it has already failed and is awaiting acknowledgement.

   **Note:** Every run settles at 3 mph before the test and recovers to 3 mph afterward. Review the stop acknowledgement and timeout behavior above before enabling maneuver mode.

   ![cog-clip-00 01 11 250-00 01 22 250](https://github.com/user-attachments/assets/c312c1cc-76e8-46e1-a05e-bb9dfb58994f)

6. When the testing is complete, you'll see an alert that says "Maneuvers Finished." Complete the route by pulling over and turning off the vehicle.

   ![fin2](https://github.com/user-attachments/assets/c06960ae-7cfb-44af-beaa-4dc28848e49d)

7. Visit https://connect.comma.ai and locate the route(s). They will stand out with lots of orange intervals in their timeline. Ensure "All logs" show as "uploaded."

   ![image](https://github.com/user-attachments/assets/cfe4c6d9-752f-4b24-b421-4b90a01933dc)

8. For the current brake sweep, use `plot_brake_characterization.py` above. For the preserved acceleration suite, gather the route ID and run the original report generator. The file will be exported to the same directory:

    ```sh
    $ python openpilot/tools/longitudinal_maneuvers/generate_report.py 57048cfce01d9625/0000010e--5b26bc3be7 'Volt creep baseline'

    processing report for CHEVROLET_VOLT
    plotting maneuver: creep stop and hold: -0.15m/s^2 from 3mph, runs: 2
    plotting maneuver: creep stop and hold: -0.3m/s^2 from 3mph, runs: 2
    ...

    Report written to /home/batman/openpilot/tools/longitudinal_maneuvers/longitudinal_reports/CHEVROLET_VOLT_57048cfce01d9625_0000010e--5b26bc3be7.html
    ```

You can reach out on [Discord](https://discord.comma.ai) if you have any questions about these instructions or the tool itself.
