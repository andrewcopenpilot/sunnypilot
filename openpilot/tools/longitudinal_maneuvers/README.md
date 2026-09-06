# Longitudinal Maneuvers Testing Tool

Test your vehicle's longitudinal control tuning with this tool. The tool will test the vehicle's ability to follow a few longitudinal maneuvers and includes a tool to generate a report from the route.

<details><summary>Sample snapshot of a report.</summary><img width="600px" src="https://github.com/user-attachments/assets/d18d0c7d-2bde-44c1-8e86-1741ed442ad8"></details>

## Volt tuning suite

This branch runs a 16-run suite designed to score a longitudinal tune in one session:

| Runs | Setup speed | Command | What it measures |
|---|---|---|---|
| 2 each | 20 mph | -0.75, -1.25, -2.0 m/s² held 5 s, then 0 for 2 s | regen-only tracking, the regen-to-friction hand-off, friction delivery; steady state after the transient; brake release |
| 2 | 20 mph | ramp 0.5 m/s³ down to -1.5, hold 2 s, then 0 | a planner-shaped request; separates actuator delay from gain |
| 2 | 40 mph | sweep 0 to -2.5 m/s² over 10 s, then 0 | one continuous map of command vs delivered torque: dead band, friction gain, regen saturation |
| 2 | 40 mph | -1.0 held 4 s, then 0 | regen at the breakpoint where the pack power cap binds at high charge |
| 2 | 40 mph | -1.5 held 3 s, then -0.5 held 3 s, then 0 | the same plus a partial release (integrator unwind) |
| 2 | 10 mph | stop at -0.75 to standstill, hold 3 s | stopping transition and brake hold (see stop-test procedure below) |

Zero target acceleration is speed holding, not a guarantee of zero gas or brake actuation.
Between runs the tool returns to the setup speed and waits for its three-second ready
condition. The 40 mph runs need more road; the sweep covers roughly 180 m of braking and ends
near 12 mph so the tool can recover to the next setup speed on its own.

The two stops from 10 mph behave as before: each continues until standstill is reported
and speed is below 0.1 m/s, then maintains stopping intent for three continuous seconds.
If the car moves during the hold, the hold timer restarts.

Before the first stop test, disengage and take control. When ready on a clear,
straight section, manually move above the car's minimum engagement speed (3 mph
on this branch) and engage; the tool sets up at 10 mph and waits three seconds.
After each stop, wait for **"Stop complete: take control before next run"**, then
take control and disengage. The tool keeps stopping intent until disengagement;
it does **not** automatically accelerate out of a completed stop. Manually set up
and re-engage for the next trial. Disengage after the final hold too, to acknowledge
completion and reach "Maneuvers Finished."

A stop/hold that has not completed within **20 seconds of braking onset** shows
**"Stop timed out: take control; retry required"**. It keeps stopping intent and
suppresses automatic resume until you take control; the failed trial must be retried.
During any active trial, disengagement discards that attempt and restarts the same
trial from speed setup on re-engagement. It does not count as a completed run.
Disengagement during a completed stop hold acknowledges success instead.

Alerts identify the run number and phase. Phase changes and completed trials are
also written to the log. Keep full rlogs, including CAN, for torque and controller
analysis; the generated report alone does not include all of that feedback.

Record the software commit and the pack voltage at rest (or state of charge) for
each route, and keep the same road direction when comparing tunes.

## Regen-only characterisation (optional)

To measure what the ACC regen path alone delivers versus speed, create the flag file on the device:

```sh
echo -n 1 > /data/params/d/VoltRegenOnlyTest
```

While that file exists, the car controller sends **zero friction brake** whatever openpilot asks for,
and the maneuver daemon runs a two-run list instead of the suite: a -2 m/s² request from 40 mph held
for 25 s, then release. The request saturates regen; the car slows only as fast as regen allows
(roughly -0.8 m/s² fading to nothing near 1.5 m/s), so allow about 200 m of clear road per run and
expect a slow finish. **Your brake pedal disengages as normal.** Remove the flag before any other
driving or the stop tests, since nothing will stop the car through the tool:

```sh
rm /data/params/d/VoltRegenOnlyTest
```

The flag is re-read once a second, so no restart is needed to toggle it. Read the result as delivered
axle torque (0x0D3) against speed with the request (0x2CB) held at -650 Nm.

## Instructions

1. Check out this branch on your comma device so the targeted sequence is used.
2. Locate either a large empty parking lot or road devoid of any car or foot traffic. Flat, straight road is preferred. The full maneuver suite can take 1 mile or more if left running, however it is recommended to disengage openpilot between maneuvers and turn around if there is not enough space.
3. Turn off the vehicle and set this parameter which will signal to openpilot to start the longitudinal maneuver daemon:

   ```sh
   echo -n 1 > /data/params/d/LongitudinalManeuverMode
   ```

4. Turn your vehicle back on. You will see the "Longitudinal Maneuver Mode" alert:

   ![videoframe_6652](https://github.com/user-attachments/assets/e9d4c95a-cd76-4ab7-933e-19937792fa0f)

5. Ensure the road ahead is clear, as openpilot will not brake for any obstructions in this mode. Once you are ready, press "Set" on your steering wheel to start the tests. Allow time for 16 successful runs. The first 14 automatically recover to their setup speed between runs; the two stops require driver takeover between runs as described above. Press "Cancel" to disengage before turning around. Re-engage only when ready on the next clear, straight section; an interrupted trial starts over.

   **Note:** The step, ramp and sweep runs start at 20 or 40 mph; the final two start at 10 mph and stop completely. Review the setup, takeover and timeout behavior above before enabling maneuver mode.

   ![cog-clip-00 01 11 250-00 01 22 250](https://github.com/user-attachments/assets/c312c1cc-76e8-46e1-a05e-bb9dfb58994f)

6. When the testing is complete, you'll see an alert that says "Maneuvers Finished." Complete the route by pulling over and turning off the vehicle.

   ![fin2](https://github.com/user-attachments/assets/c06960ae-7cfb-44af-beaa-4dc28848e49d)

7. Visit https://connect.comma.ai and locate the route(s). They will stand out with lots of orange intervals in their timeline. Ensure "All logs" show as "uploaded."

   ![image](https://github.com/user-attachments/assets/cfe4c6d9-752f-4b24-b421-4b90a01933dc)

8. Gather the route ID and then run the report generator. The file will be exported to the same directory:

    ```sh
    $ python openpilot/tools/longitudinal_maneuvers/generate_report.py 57048cfce01d9625/0000010e--5b26bc3be7 'Volt braking baseline'

    processing report for CHEVROLET_VOLT
    plotting maneuver: brake step and release: -0.5m/s^2 from 20mph, runs: 3
    plotting maneuver: brake step and release: -0.75m/s^2 from 20mph, runs: 3
    ...

    Report written to /home/batman/openpilot/tools/longitudinal_maneuvers/longitudinal_reports/CHEVROLET_VOLT_57048cfce01d9625_0000010e--5b26bc3be7.html
    ```

You can reach out on [Discord](https://discord.comma.ai) if you have any questions about these instructions or the tool itself.
