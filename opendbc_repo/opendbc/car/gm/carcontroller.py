import numpy as np
from opendbc.can import CANPacker
from opendbc.car import Bus, DT_CTRL, structs
from opendbc.car.lateral import apply_driver_steer_torque_limits
from opendbc.car.gm import gmcan
from opendbc.car.gm.brake_characterization import brake_test_enabled, brake_test_valid
from opendbc.car.common.conversions import Conversions as CV
from opendbc.car.gm.values import CAR, DBC, CanBus, CarControllerParams, CruiseButtons
from opendbc.car.interfaces import CarControllerBase

VisualAlert = structs.CarControl.HUDControl.VisualAlert
NetworkLocation = structs.CarParams.NetworkLocation
LongCtrlState = structs.CarControl.Actuators.LongControlState

# Camera cancels up to 0.1s after brake is pressed, ECM allows 0.5s
CAMERA_CANCEL_DELAY_FRAMES = 10
# Enforce a minimum interval between steering messages to avoid a fault
MIN_STEER_MSG_INTERVAL_MS = 15


class CarController(CarControllerBase):
  def __init__(self, dbc_names, CP, CP_SP):
    super().__init__(dbc_names, CP, CP_SP)
    self.start_time = 0.
    self.apply_torque_last = 0
    self.apply_gas = 0
    self.apply_brake = 0
    self.last_steer_frame = 0
    self.last_button_frame = 0
    self.cancel_counter = 0

    self.lka_steering_cmd_counter = 0
    self.lka_icon_status_last = (False, False)

    self.params = CarControllerParams(self.CP)

    self.packer_pt = CANPacker(DBC[self.CP.carFingerprint][Bus.pt])
    self.packer_obj = CANPacker(DBC[self.CP.carFingerprint][Bus.radar])
    self.packer_ch = CANPacker(DBC[self.CP.carFingerprint][Bus.chassis])

    # stock ASCM longitudinal state
    self.brake_mode = False       # False: torque mode (stock mode 1), True: friction-brake mode (stock mode 2)
    self.brake_accel_cmd = 0.     # rate-limited brake-path accel command, m/s^2
    self.gas_cmd = 0.             # rate-limited torque-mode GasRegenCmd, Nm
    self.stock_creep_active = False
    self.brake_test_failed = False

  def stock_creep_weight(self, CS, stopping):
    # Hold/resume has additional OEM states; retain the existing stop/start sequence for now.
    if (not self.params.STOCK_CREEP_TRANSITIONS or self.CP.carFingerprint != CAR.CHEVROLET_VOLT or
        self.CP.networkLocation != NetworkLocation.gateway or CS.out.vEgo <= 0. or
        stopping or CS.out.standstill or CS.out.cruiseState.standstill):
      return 0.
    return float(np.interp(CS.out.vEgo, self.params.STOCK_CREEP_BLEND_BP, [1., 0.]))

  def stock_gas_brake(self, accel, CS, stopping):
    """OEM-inspired gas (Nm) and brake (counts) allocation from corrected acceleration.
    Uses FUN_0013afc0/0013a360 transitions in moving creep, with the existing stop/start path.
    The OEM request-state selector and disturbance compensation are not ported here.
    """
    p = self.params
    v = CS.out.vEgo
    dt = 4 * DT_CTRL  # 25 Hz

    # regen the ACC path can deliver right now, from the HPCM's live limit (0x1C5)
    t_min = CS.axle_torque_min if CS.axle_torque_min_valid else p.MAX_ACC_REGEN
    a_regen = p.regen_accel_available(t_min, v)

    was_braking = self.brake_mode
    creep_weight = self.stock_creep_weight(CS, stopping)
    self.stock_creep_active = creep_weight > 0.
    margin = float(np.interp(v, p.BRAKE_ENTRY_MARGIN_BP, p.BRAKE_ENTRY_MARGIN_V))
    thresh = a_regen + margin + (p.BRAKE_ENTRY_HYST if was_braking else 0.)
    if was_braking and self.stock_creep_active:
      retain_margin = float(np.interp(v, p.BRAKE_RETAIN_MARGIN_BP, p.BRAKE_RETAIN_MARGIN_V))
      # OEM branch using 0x81e=0, with disturbance correction omitted consistently on both paths.
      # Openpilot has no equivalent to the OEM request-state selector; do not invent a mapping.
      retain_thresh = a_regen + retain_margin
      thresh += creep_weight * (retain_thresh - thresh)
    self.brake_mode = accel < thresh or stopping

    if not self.brake_mode:
      # torque mode: physics feedforward on the gas/regen path, rate limited as stock, brakes idle
      target = float(np.clip(p.torque_ff(accel, v), p.MAX_ACC_REGEN, p.MAX_GAS))
      up = float(np.interp(v, p.GAS_RATE_UP_BP, p.GAS_RATE_UP_V)) * dt
      if (self.stock_creep_active and was_braking and CS.axle_torque_min_valid and
          np.isfinite(CS.axle_torque_min)):
        # OEM FUN_0013a360 seeds the first torque-mode output from 0x1C5 minimum torque.
        # This intentionally differs from slewing out of the stored -650 Nm brake-mode request.
        self.gas_cmd = float(np.clip(CS.axle_torque_min, p.MAX_ACC_REGEN, p.MAX_GAS))
      else:
        self.gas_cmd = float(np.clip(target, self.gas_cmd - p.GAS_RATE_DOWN * dt, self.gas_cmd + up))
      self.brake_accel_cmd = 0.
      return self.gas_cmd, 0

    # brake mode: fixed max ACC regen request (stock cal 0x834), whole decel target on the brake path
    self.gas_cmd = p.MAX_ACC_REGEN
    # Reduce moving-creep demand before the existing bounds and slew limit. Mode
    # selection still uses the unscaled corrected acceleration; integral feedback
    # can continue increasing demand up to the existing brake limit.
    brake_scale = 1. - creep_weight * (1. - p.CREEP_BRAKE_SCALE)
    target = min(accel, 0.) * brake_scale
    target = max(target, float(np.interp(v, p.STOCK_DECEL_FLOOR_BP, p.STOCK_DECEL_FLOOR_V)), p.ACCEL_MIN)
    step = p.BRAKE_JERK_LIMIT * dt
    self.brake_accel_cmd = float(np.clip(target, self.brake_accel_cmd - step, self.brake_accel_cmd + step))
    brake = int(round(-self.brake_accel_cmd * p.BRAKE_COUNTS_PER_MPS2))
    return self.gas_cmd, min(brake, p.MAX_BRAKE)

  def update(self, CC, CC_SP, CS, now_nanos):
    actuators = CC.actuators
    hud_control = CC.hudControl
    hud_alert = hud_control.visualAlert
    hud_v_cruise = hud_control.setSpeed
    if hud_v_cruise > 70:
      hud_v_cruise = 0

    # Send CAN commands.
    can_sends = []

    # Steering (Active: 50Hz, inactive: 10Hz)
    steer_step = self.params.STEER_STEP if CC.latActive else self.params.INACTIVE_STEER_STEP

    if self.CP.networkLocation == NetworkLocation.fwdCamera:
      # Also send at 50Hz:
      # - on startup, first few msgs are blocked
      # - until we're in sync with camera so counters align when relay closes, preventing a fault.
      #   openpilot can subtly drift, so this is activated throughout a drive to stay synced
      out_of_sync = self.lka_steering_cmd_counter % 4 != (CS.cam_lka_steering_cmd_counter + 1) % 4
      if CS.loopback_lka_steering_cmd_ts_nanos == 0 or out_of_sync:
        steer_step = self.params.STEER_STEP

    self.lka_steering_cmd_counter += 1 if CS.loopback_lka_steering_cmd_updated else 0

    # Avoid GM EPS faults when transmitting messages too close together: skip this transmit if we
    # received the ASCMLKASteeringCmd loopback confirmation too recently
    last_lka_steer_msg_ms = (now_nanos - CS.loopback_lka_steering_cmd_ts_nanos) * 1e-6
    if (self.frame - self.last_steer_frame) >= steer_step and last_lka_steer_msg_ms > MIN_STEER_MSG_INTERVAL_MS:
      # Initialize ASCMLKASteeringCmd counter using the camera until we get a msg on the bus
      if CS.loopback_lka_steering_cmd_ts_nanos == 0:
        self.lka_steering_cmd_counter = CS.pt_lka_steering_cmd_counter + 1

      if CC.latActive:
        new_torque = int(round(actuators.torque * self.params.STEER_MAX))
        apply_torque = apply_driver_steer_torque_limits(new_torque, self.apply_torque_last, CS.out.steeringTorque, self.params)
      else:
        apply_torque = 0

      self.last_steer_frame = self.frame
      self.apply_torque_last = apply_torque
      idx = self.lka_steering_cmd_counter % 4
      can_sends.append(gmcan.create_steering_control(self.packer_pt, CanBus.OBSTACLE, apply_torque, idx, CC.latActive))

    if self.CP.openpilotLongitudinalControl:
      # Gas/regen, brakes, and UI commands - all at 25Hz
      if self.frame % 4 == 0:
        stopping = actuators.longControlState == LongCtrlState.stopping
        brake_test_running = False
        test_requested = CC.enabled and CC.brakeTestActive and brake_test_enabled(self.CP, self.CP_SP)
        if not test_requested or not CC.longActive or CS.out.gasPressed or CS.out.brakePressed:
          self.brake_test_failed = False
        if not CC.longActive or (test_requested and (CS.out.gasPressed or CS.out.brakePressed)):
          # ASCM sends max regen when not enabled
          self.apply_gas = self.params.INACTIVE_REGEN
          self.apply_brake = 0
          self.brake_mode = False
          self.brake_accel_cmd = 0.
          self.stock_creep_active = False
        elif test_requested:
          if not self.brake_test_failed and not stopping and brake_test_valid(CC.brakeTestCommand, CC.brakeTestMonoTime, now_nanos, CS.out):
            # Characterize the EBCM with fixed gas/regen and direct counts. Bypass PI
            # mapping, creep scaling and mode selection only for this explicit test.
            brake_test_running = True
            self.brake_mode = True
            self.stock_creep_active = True  # retain active brake mode even at zero counts
            self.gas_cmd = self.apply_gas = self.params.MAX_ACC_REGEN
            self.apply_brake = int(round(CC.brakeTestCommand))
            self.brake_accel_cmd = -self.apply_brake / self.params.BRAKE_COUNTS_PER_MPS2
          else:
            # A stale/invalid test must not continue a held command or resume into torque.
            self.brake_test_failed = True
            stopping = True
            self.apply_gas, self.apply_brake = self.stock_gas_brake(-2., CS, True)
        else:
          # stock ASCM two-mode logic (see CarControllerParams)
          self.apply_gas, self.apply_brake = self.stock_gas_brake(actuators.accel, CS, stopping)

        idx = (self.frame // 4) % 4

        at_full_stop = CC.longActive and CS.out.standstill
        # Measure ordinary braking (0xA): the 0xB baseline built pressure at zero demand.
        # Abort/stopping paths retain the existing near-stop behavior.
        near_stop = (CC.longActive and self.brake_mode and not brake_test_running and
                     abs(CS.out.vEgo) < self.params.NEAR_STOP_SPEED)
        friction_brake_bus = CanBus.OBSTACLE
        # GM Camera exceptions
        # TODO: can we always check the longControlState?
        if self.CP.networkLocation == NetworkLocation.fwdCamera:
          at_full_stop = at_full_stop and stopping
          friction_brake_bus = CanBus.POWERTRAIN

        # Normally this bit describes ACC engagement, independently of actuation.
        gas_regen_active = CC.enabled
        if self.CP.carFingerprint == CAR.CHEVROLET_VOLT and self.CP.autoResumeSng:
          # Old kegman ZERO_GAS was raw 2048; this DBC uses signed Nm (zero = 0).
          resume_from_stop = (CC.longActive and CS.out.cruiseState.standstill and
                              not stopping and not CS.out.brakePressed and
                              self.apply_gas >= 0. and self.apply_brake == 0)
          at_full_stop = CC.longActive and CS.out.cruiseState.standstill and not resume_from_stop
          if resume_from_stop:
            gas_regen_active = False

        can_sends.append(gmcan.create_gas_regen_command(self.packer_pt, CanBus.OBSTACLE, self.apply_gas,
                                                       idx, gas_regen_active, at_full_stop))
        can_sends.append(gmcan.create_friction_brake_command(self.packer_ch, friction_brake_bus, self.apply_brake,
                                                             idx, CC.enabled, near_stop, at_full_stop, self.CP,
                                                             brake_active=(CC.longActive and self.stock_creep_active and
                                                                           self.brake_mode)))

        # Send dashboard UI commands (ACC status)
        send_fcw = hud_alert == VisualAlert.fcw
        can_sends.append(gmcan.create_acc_dashboard_command(self.packer_pt, CanBus.OBSTACLE, CC.enabled,
                                                            hud_v_cruise * CV.MS_TO_KPH, hud_control, send_fcw))

      # Radar needs to know current speed and yaw rate (50hz),
      # and that ADAS is alive (10hz)
      # tizi ASCM interceptor: stock ASCM stays alive, don't impersonate it
      if False:
        tt = self.frame * DT_CTRL
        time_and_headlights_step = 10
        if self.frame % time_and_headlights_step == 0:
          idx = (self.frame // time_and_headlights_step) % 4
          can_sends.append(gmcan.create_adas_time_status(CanBus.OBSTACLE, int((tt - self.start_time) * 60), idx))
          can_sends.append(gmcan.create_adas_headlights_status(self.packer_obj, CanBus.OBSTACLE))

        speed_and_accelerometer_step = 2
        if self.frame % speed_and_accelerometer_step == 0:
          idx = (self.frame // speed_and_accelerometer_step) % 4
          can_sends.append(gmcan.create_adas_steering_status(CanBus.OBSTACLE, idx))
          can_sends.append(gmcan.create_adas_accelerometer_speed_status(CanBus.OBSTACLE, abs(CS.out.vEgo), idx))

      if False:
        can_sends += gmcan.create_adas_keepalive(CanBus.POWERTRAIN)

    else:
      # While car is braking, cancel button causes ECM to enter a soft disable state with a fault status.
      # A delayed cancellation allows camera to cancel and avoids a fault when user depresses brake quickly
      self.cancel_counter = self.cancel_counter + 1 if CC.cruiseControl.cancel else 0

      # Stock longitudinal, integrated at camera
      if (self.frame - self.last_button_frame) * DT_CTRL > 0.04:
        if self.cancel_counter > CAMERA_CANCEL_DELAY_FRAMES:
          self.last_button_frame = self.frame
          can_sends.append(gmcan.create_buttons(self.packer_pt, CanBus.CAMERA, CS.buttons_counter, CruiseButtons.CANCEL))

    if self.CP.networkLocation == NetworkLocation.fwdCamera:
      # Silence "Take Steering" alert sent by camera, forward PSCMStatus with HandsOffSWlDetectionStatus=1
      if self.frame % 10 == 0:
        can_sends.append(gmcan.create_pscm_status(self.packer_pt, CanBus.CAMERA, CS.pscm_status))

    new_actuators = actuators.as_builder()
    if self.brake_test_failed:
      new_actuators.longControlState = LongCtrlState.stopping
    new_actuators.torque = self.apply_torque_last / self.params.STEER_MAX
    new_actuators.torqueOutputCan = self.apply_torque_last
    new_actuators.gas = self.apply_gas
    new_actuators.brake = self.apply_brake

    self.frame += 1
    return new_actuators, can_sends
