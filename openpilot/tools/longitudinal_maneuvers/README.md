# Longitudinal Maneuvers Testing Tool

Test your vehicle's longitudinal control tuning with this tool. The tool will test the vehicle's ability to follow a few longitudinal maneuvers and includes a tool to generate a report from the route.

<details><summary>Sample snapshot of a report.</summary><img width="600px" src="https://github.com/user-attachments/assets/d18d0c7d-2bde-44c1-8e86-1741ed442ad8"></details>

## Volt creep tuning suite

The suite contains **16 runs: eight creep scenarios, each repeated twice**. The test
portion starts at 3 mph or below. The old higher-speed braking and regen trials have
been removed.

Every run follows the same sequence:

1. Accelerate to **8 mph** and stay near that speed for three seconds while showing
   the upcoming test.
2. Slow to **3 mph** and settle there for **two continuous seconds**.
3. Perform the creep test below.
4. Return to **8 mph** and stay near that speed for three seconds before advancing.
   Stop-and-hold tests wait for driver acknowledgement first, as described below.

Setup and recovery target 8 mph, with a 0.1 m/s settling tolerance. They use up to
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

### Stops, recovery, and status

A stop must report standstill with speed below 0.1 m/s and then hold for three
continuous seconds. Movement resets the hold timer. Until the hold is complete,
the screen says **"Maneuver Active: holding stop"**.

After **"Stop complete: tap throttle"** appears, tap the throttle
to acknowledge the completed hold. The tool releases stopping intent and recovers to
8 mph once longitudinal control is active again. Alternatively, disengage, manually
move above the minimum engagement speed (3 mph on this branch), and re-engage to
recover. Completed stop holds do not automatically launch without acknowledgement.

The two moving crawl tests enter recovery automatically after their timed commands.
If stock cruise holds the car stopped, tap the throttle when **"Test complete: tap throttle"** appears.
While moving, the screen says **"Recovering to 8 mph"**. A run is only counted after
the 8 mph recovery has settled. This includes the final run; then the screen shows
**"Maneuvers Finished"**. Take control to end the drive.

During longitudinal maneuver testing, the low-speed steering warning is suppressed
so test progress and completion remain visible. Normal driving retains the warning.
Other alerts and the actual steering-assist speed limit are unchanged.

A stop/hold that has not completed within **20 seconds of braking onset** shows
**"Stop timed out: take control"**. Pulse trials allow 30 seconds.
A timed-out stop maintains stopping intent until takeover; disengage and re-engage
to retry the same run. Interrupting setup or an unfinished test also restarts that
run from the 8 mph setup. Interrupting recovery pauses it; re-engagement resumes
recovery without repeating the completed test.

Alerts identify the run number and phase. Phase changes and completed trials are
also written to the log. Keep full rlogs, including CAN, for torque and controller
analysis; the generated report alone does not include all of that feedback.

Record the software commit and the pack voltage at rest (or state of charge) for
each route, and keep the same road direction when comparing tunes.

## Instructions

1. Check out this branch on your comma device so the targeted sequence is used.
2. Locate either a large empty parking lot or road devoid of any car or foot traffic. Flat, straight road is preferred. Leave enough room for the 8 mph setup and recovery on every run. Disengage and take control before turning around.
3. Turn off the vehicle and set this parameter which will signal to openpilot to start the longitudinal maneuver daemon:

   ```sh
   echo -n 1 > /data/params/d/LongitudinalManeuverMode
   ```

4. Turn your vehicle back on. You will see the "Longitudinal Maneuver Mode" alert:

   ![videoframe_6652](https://github.com/user-attachments/assets/e9d4c95a-cd76-4ab7-933e-19937792fa0f)

5. Ensure the road ahead is clear, as openpilot will not brake for any obstructions in this mode. Once you are ready, press "Set" on your steering wheel to start the tests. Allow time for 16 successful runs. The first 12 are stop-and-hold trials requiring acknowledgement before recovery; the final four are timed crawl trials. Press "Cancel" to disengage before turning around. Re-engage only when ready on the next clear, straight section; an interrupted trial starts over.

   **Note:** Every run reaches 8 mph before slowing to 3 mph for the test, then returns to 8 mph. Review the stop acknowledgement and timeout behavior above before enabling maneuver mode.

   ![cog-clip-00 01 11 250-00 01 22 250](https://github.com/user-attachments/assets/c312c1cc-76e8-46e1-a05e-bb9dfb58994f)

6. When the testing is complete, you'll see an alert that says "Maneuvers Finished." Complete the route by pulling over and turning off the vehicle.

   ![fin2](https://github.com/user-attachments/assets/c06960ae-7cfb-44af-beaa-4dc28848e49d)

7. Visit https://connect.comma.ai and locate the route(s). They will stand out with lots of orange intervals in their timeline. Ensure "All logs" show as "uploaded."

   ![image](https://github.com/user-attachments/assets/cfe4c6d9-752f-4b24-b421-4b90a01933dc)

8. Gather the route ID and then run the report generator. The file will be exported to the same directory:

    ```sh
    $ python openpilot/tools/longitudinal_maneuvers/generate_report.py 57048cfce01d9625/0000010e--5b26bc3be7 'Volt creep baseline'

    processing report for CHEVROLET_VOLT
    plotting maneuver: creep stop and hold: -0.15m/s^2 from 3mph, runs: 2
    plotting maneuver: creep stop and hold: -0.3m/s^2 from 3mph, runs: 2
    ...

    Report written to /home/batman/openpilot/tools/longitudinal_maneuvers/longitudinal_reports/CHEVROLET_VOLT_57048cfce01d9625_0000010e--5b26bc3be7.html
    ```

You can reach out on [Discord](https://discord.comma.ai) if you have any questions about these instructions or the tool itself.
