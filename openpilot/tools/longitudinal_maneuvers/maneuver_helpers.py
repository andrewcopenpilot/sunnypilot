from enum import IntEnum

class Axis(IntEnum):
  TIME = 0
  EGO_POSITION = 1
  LEAD_DISTANCE= 2
  EGO_V = 3
  LEAD_V = 4
  EGO_A = 5
  D_REL = 6

axis_labels = {Axis.TIME: 'Time (s)',
               Axis.EGO_POSITION: 'Ego position (m)',
               Axis.LEAD_DISTANCE: 'Lead absolute position (m)',
               Axis.EGO_V: 'Ego Velocity (m/s)',
               Axis.LEAD_V: 'Lead Velocity (m/s)',
               Axis.EGO_A: 'Ego acceleration (m/s^2)',
               Axis.D_REL: 'Lead distance (m)'}


def collect_maneuvers(messages):
  maneuvers = []
  active_prev = False
  description_prev = None
  for msg in messages:
    if msg.which() == 'alertDebug':
      active = 'Maneuver Active' in msg.alertDebug.alertText1
      # Retain the failure marker even though it ends the active interval.
      if active_prev and msg.alertDebug.alertText1.startswith(('Creep test invalid:', 'Brake test ended:')):
        maneuvers[-1][1][-1].append(msg)
      if active and not active_prev:
        if msg.alertDebug.alertText2 == description_prev:
          maneuvers[-1][1].append([])
        else:
          maneuvers.append((msg.alertDebug.alertText2, [[]]))
        description_prev = maneuvers[-1][0]
      active_prev = active
    if active_prev:
      maneuvers[-1][1][-1].append(msg)
  return maneuvers
