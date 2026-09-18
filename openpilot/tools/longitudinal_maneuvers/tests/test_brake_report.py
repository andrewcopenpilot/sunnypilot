import unittest
import numpy as np

from opendbc.can import CANPacker
from opendbc.car.gm import gmcan
from opendbc.car.gm.tests.test_longitudinal import make_controller
from openpilot.cereal import log
from openpilot.tools.longitudinal_maneuvers.plot_brake_characterization import extract, trial_samples, COLUMNS
from openpilot.selfdrive.car.helpers import convert_to_capnp
from opendbc.car import structs


def event(kind, timestamp):
  msg = log.Event.new_message()
  msg.logMonoTime = int(timestamp * 1e9)
  msg.init(kind)
  return msg


def synthetic_events():
  """Small artificial log fixture; deliberately not a vehicle-response model."""
  controller = make_controller()
  packer = CANPacker('gm_global_a_chassis')
  for tick in range(121):
    t = 1. + tick * .05
    m = event('alertDebug', t)
    m.alertDebug.alertText1 = 'Maneuver Active: brake sweep' if tick < 120 else 'Brake test ended: profile complete'
    m.alertDebug.alertText2 = 'brake characterization: synthetic fixture'
    yield m
    if tick == 120:
      break
    count = max(0., (tick * .05 - 2.) * .5)
    m = event('carState', t)
    m.carState.vEgo = 1.34 - .015 * (tick * .05) ** 2
    m.carState.vEgoRaw = m.carState.vEgo
    m.carState.aEgo = -.03 * tick * .05
    yield m
    m = event('carControl', t)
    m.carControl.brakeTestActive = True
    m.carControl.brakeTestCommand = count
    m.carControl.longActive = True
    yield m
    m = event('carOutput', t)
    m.carOutput.actuatorsOutput.gas = -650.
    yield m
    packet = gmcan.create_friction_brake_command(packer, 1, round(count), tick % 4, True, True, False, controller.CP, brake_active=True)
    m = log.Event.new_message()
    m.logMonoTime = int(t * 1e9)
    can = m.init('sendcan', 1)[0]
    can.address, can.dat, can.src = packet
    yield m
    m = log.Event.new_message()
    m.logMonoTime = int(t * 1e9)
    can = m.init('can', 1)[0]
    can.address, can.src = 0x170, 2
    can.dat = b'\x00\x00' + int(round(count) * 100).to_bytes(2, 'big') + bytes(4)
    yield m


class TestBrakeReport(unittest.TestCase):
  def test_can_decode_alignment_and_endpoint(self):
    arrays, trials = extract(synthetic_events())
    self.assertEqual(len(trials), 1)
    self.assertEqual(trials[0]['outcome'], 'Brake test ended: profile complete')
    values = trial_samples(arrays, trials[0])
    self.assertEqual(values.shape, (120, len(COLUMNS)))
    self.assertTrue(np.all(values[:, 5] == 11))
    np.testing.assert_allclose(values[:, 4], np.rint(values[:, 1]))
    np.testing.assert_allclose(values[:, 11], values[:, 4] * 100.)
    self.assertTrue(np.all(values[:, 12] == -650.))
    self.assertEqual(values[0, 0], 0.)
    self.assertLess(values[-1, 0], 6.)

  def test_drive_authorization_survives_serialization(self):
    cp = structs.CarParamsSP()
    self.assertFalse(convert_to_capnp(cp).longitudinalManeuverMode)
    cp.longitudinalManeuverMode = True
    self.assertTrue(convert_to_capnp(cp).longitudinalManeuverMode)
