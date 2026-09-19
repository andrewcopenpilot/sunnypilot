"""Compare reference branches against recovered C, not against CPU emulation.

Requires Linux, gcc, and the exact calibration in evidence.json. See README.md
for ABI repairs and limitations. Run in a fresh process (maps emulated RAM).
"""

from pathlib import Path
from dataclasses import replace
import ctypes as C
import importlib.util
import random
import struct
import subprocess
import sys
import os
import tempfile
import hashlib
import json

evidence = Path(__file__).resolve().parent
p = evidence.parent / 'ascm_loop_reference.py'
fw = Path(os.environ.get('ASCM_FIRMWARE_ROOT', str(Path.home() / 'volt_reverse_engineering/ASCM')))
temporary = tempfile.TemporaryDirectory(prefix='ascm-reference-')
work = Path(temporary.name)
spec = importlib.util.spec_from_file_location('ascm_ref', p)
ref = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = ref
spec.loader.exec_module(ref)
source = evidence / 'exports'
header = '''#include <stdint.h>
#include <stdbool.h>
#include <sys/mman.h>
#include <string.h>
typedef unsigned char byte; typedef unsigned short ushort; typedef unsigned int uint;
typedef long long longlong; typedef unsigned long long ulonglong;
typedef uint8_t undefined1; typedef uint16_t undefined2; typedef uint32_t undefined4; typedef int64_t undefined8;
'''
scalars = {
  '40037a40': 'uint32_t',
  '4001d998': 'int16_t',
  '4001e1b0': 'int16_t',
  '4001e171': 'uint8_t',
  '4001d8f2': 'int16_t',
  '4001e184': 'uint8_t',
  '4001e1a6': 'uint8_t',
  '4001e188': 'int32_t',
  '4001d9a0': 'uint32_t',
  '4001d91c': 'int16_t',
  '4001d928': 'uint8_t',
  '4001da04': 'uint32_t',
  '4001d93f': 'uint8_t',
  '4001d8e2': 'uint8_t',
  '4001dc30': 'uint16_t',
  '4001e170': 'uint8_t',
  '4001dcc0': 'uint32_t',
  '4001e1a4': 'uint16_t',
  '4001e176': 'int16_t',
  '4001e178': 'uint16_t',
  '4001d9b8': 'uint32_t',
  '4001d994': 'int16_t',
}
scalars.update(
  {
    '4001d8f4': 'int16_t',
    '4001e17c': 'uint32_t',
    '4001e182': 'int16_t',
    '4001e1ac': 'int32_t',
    '4001e18c': 'int32_t',
    '4001dae8': 'int16_t',
    '4001dc94': 'int16_t',
    '4001d924': 'int16_t',
    '4001d990': 'uint8_t',
    '4001e180': 'int16_t',
  }
)
for addr, t in scalars.items():
  header += f'#define DAT_{addr} (*({t}*)0x{addr}UL)\n'
header += '''longlong FUN_0012e580(longlong a,longlong b){return (int)a<(int)b?a:b;}
longlong FUN_0012e590(longlong a,longlong b){return (int)a>(int)b?a:b;}
longlong FUN_0012e5a0(longlong a,longlong b,longlong c){return FUN_0012e590(FUN_0012e580(b,c),FUN_0012e580(a,FUN_0012e590(b,c)));}
longlong FUN_0012e630(longlong target,longlong prev,longlong lo,longlong hi,longlong dt){
int rate=((int)target-(int)prev)*1000/(int)dt; rate=FUN_0012e5a0(rate,lo,hi);return prev+rate*(int)dt/1000;}
'''
header += source.joinpath('FUN_0012e3e0.c').read_text()
header += source.joinpath('FUN_0013bbc0.c').read_text() + source.joinpath('FUN_0013bb20.c').read_text()
header += source.joinpath('FUN_0013afc0.c').read_text()
header += (
  source.joinpath('FUN_0013ade0.c')
  .read_text()
  .replace('FUN_0012e590();', 'FUN_0012e590(*param_4, *(short *)(param_5 + 4));')
  .replace('*(undefined2 *)(param_5 + 0xe)', '*(short *)(param_5 + 0xe)')
)
# Restore signed argument extensions verified at 13a25e, 13a2d4/2da,
# 13a2e4/2f0 and 13a30c. Ghidra's undefined2 otherwise promotes unsigned.
header += (
  source.joinpath('FUN_0013a180.c').read_text()
  .replace('undefined2 uVar3;', 'short uVar3;')
  .replace('*(undefined2 *)(param_5 + 2)', '*(short *)(param_5 + 2)')
  .replace('param_4,*param_3', 'param_4,*(short *)param_3')
  .replace('*(undefined2 *)(DAT_40037a40 + 0x83a)', '*(short *)(DAT_40037a40 + 0x83a)')
)
header += 'longlong FUN_0012e610(longlong a){return a<0?-a:a;}\n'
header += source.joinpath('FUN_0012e5e0.c').read_text()
header += source.joinpath('FUN_0013a570.c').read_text()
header += (
  source.joinpath('FUN_0013a5d0.c')
  .read_text()
  .replace('SUB168(SEXT216(1000),0)', '1000')
  .replace('FUN_0012e3e0(DAT_40037a40 + 0x736,2);', 'FUN_0012e3e0(DAT_40037a40 + 0x736,2,*param_3);')
)

header += '''int setup(void){return mmap((void*)0x40000000,0x40000,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE,-1,0)==MAP_FAILED?-1:0;}
void allocate(int dt){FUN_0013afc0(dt,(short*)0x4001dae4,0x4001dc80,0x4001dea0,0x4001deb4,0x4001d978);}
void request(int dt){FUN_0013ade0(dt,0x4001dc90,(undefined2*)0x4001d998,(short*)0x4001dc80,0x4001dea0,(short*)0x4001deb4);}
void feedback(int dt){FUN_0013a5d0(dt,0x4001dc90,(short*)0x4001d998,0x4001dae4,0x4001dc80,(short*)0x4001dea0,(short*)0x4001deb4);}
void hold(int dt){FUN_0013a180(dt,(undefined2*)0x4001dc90,(undefined2*)0x4001d998,0x4001e148,0x4001dae4,0x4001dc80,0x4001deb4);}
'''
(work / 'oracle.c').write_text(header)
subprocess.run(['gcc', '-shared', '-fPIC', '-O0', '-w', '-o', str(work / 'oracle.so'), str(work / 'oracle.c')], check=True)
lib = C.CDLL(str(work / 'oracle.so'))
assert lib.setup() == 0
ram = (C.c_ubyte * 0x40000).from_address(0x40000000)


def put(addr, fmt, value):
  struct.pack_into('<' + fmt, ram, addr - 0x40000000, value)


def get(addr, fmt):
  return struct.unpack_from('<' + fmt, ram, addr - 0x40000000)[0]


cal_file = (fw / 'decoded/23366550.bin').read_bytes()
assert hashlib.sha256(cal_file).hexdigest() == json.loads((evidence / 'evidence.json').read_text())['firmware']['23366550.bin']
cal = cal_file[0xA0:]
tables = {0x708: 3, 0x714: 3, 0x720: 3, 0x810: 3, 0x7DE: 3, 0x7EA: 3, 0x736: 2, 0x73E: 3, 0x74E: 2, 0x756: 3, 0x768: 3, 0x774: 6}


def init():
  C.memset(0x40000000, 0, 0x40000)
  put(0x40037A40, 'I', 0x40030000)
  for off in [
    0x78C,
    0x78E,
    0x808,
    0x80A,
    0x80E,
    0x81C,
    0x81E,
    0x820,
    0x822,
    0x824,
    0x832,
    0x7A6,
    0x7A8,
    0x7F6,
    0x730,
    0x732,
    0x734,
    0x838,
    0x83A,
    0x764,
    0x766,
    0x79C,
    0x79E,
    0x7A0,
    0x7A2,
    0x7A4,
    0x828,
    0x82A,
    0x82C,
    0x82E,
    0x830,
  ]:
    put(0x40030000 + off, 'h', struct.unpack_from('>h', cal, off)[0])
  for off in [0x806, 0x80C, 0x83C, 0x6BA, 0x5DF, 0x72C, 0x72D]:
    put(0x40030000 + off, 'B', cal[off])
  for off, n in tables.items():
    for k in range(n * 2):
      put(0x40030000 + off + 2 * k, 'h', struct.unpack_from('>h', cal, off + 2 * k)[0])
  for off in [0x700, 0x704, 0x6D0, 0x6D4, 0x6D8]:
    put(0x40030000 + off, 'i', struct.unpack_from('>i', cal, off)[0])
  for off, val in [(0x10, 17760), (0x12, 2032), (0x14, 250), (0x1A, 8), (0x1C, 1000)]:
    put(0x4001E148 + off, 'h', val)


def lookup(off, arg):
  return ref.stock_lookup(tuple(struct.unpack_from('>hh', cal, off + k * 4) for k in range(tables[off])), arg)


r = random.Random(84876565)
for i in range(20000):
  init()
  owner = ref.Owner(r.randrange(3))
  state = r.randrange(6)
  speed = r.choice([-100, 0, 149, 150, 151, 500, 3000])
  correction = r.randrange(-2200, 2201)
  amin = r.randrange(-2000, 1)
  cls = r.choice([-1, 0, 1])
  alt = r.choice([False, True])
  flags = r.getrandbits(7) << 22
  stand = r.choice([False, True])
  special = r.randrange(2)
  hold = r.choice([False, True])
  sub = r.randrange(1, 6)
  latch = r.choice([False, True])
  main = r.choice([False, True])
  supp = r.choice([False, True])
  variant = r.choice([False, True])
  stop27 = r.choice([False, True])
  stop28 = r.choice([False, True])
  history = r.randrange(3)
  timer = r.randrange(64)
  margin = lookup(0x708 if owner == ref.Owner.BRAKE else 0x720 if cls == -1 and alt else 0x714, speed) + ref.c_div(
    (400 if owner == ref.Owner.BRAKE else 200) * correction, 1000
  )
  threshold = amin + margin + (50 if state == 2 else 0)
  corrected = r.choice([threshold - 1, threshold, threshold + 1, r.randrange(-5000, 3001)])
  prev = ref.RawAllocation(owner, r.randrange(-2000, 2001), r.randrange(-5000, 3001), latch)
  for a, f, v in [
    (0x4001DAEE, 'B', owner),
    (0x4001DAF2, 'B', sub),
    (0x4001DAE4, 'h', prev.torque_accel),
    (0x4001DAE6, 'h', prev.brake_accel),
    (0x4001E147, 'B', state),
    (0x4001D998, 'h', speed),
    (0x4001DEC0, 'h', correction),
    (0x4001DEC4, 'h', corrected),
    (0x4001DEA4, 'h', amin),
    (0x4001D8F2, 'h', cls),
    (0x4001D990, 'B', alt),
    (0x4001DC8C, 'I', flags),
    (0x4001D9A0, 'I', int(stand) << 25),
    (0x4001D91C, 'h', special),
    (0x4001DF9C, 'B', hold),
    (0x4001E184, 'B', latch),
    (0x4001D928, 'B', main),
    (0x4001DA04, 'I', int(supp) << 26),
    (0x4001D93F, 'B', supp),
    (0x4001D8E2, 'B', variant),
    (0x4001DCC0, 'I', (int(stop27) << 27) | (int(stop28) << 28)),
    (0x4001E170, 'B', history),
    (0x4001DC30, 'H', timer),
  ]:
    put(a, f, v)
  expected = ref.allocate_acceleration(prev, state, flags, corrected, correction, amin, threshold, stand, special, hold, sub)
  es = ref.select_brake_submode(expected.owner, owner, speed, main, supp, hold, variant, stop27, stop28, stand, special, ref.BrakeSubmode(sub, timer, history))
  lib.allocate(40)
  actual = (get(0x4001DAEE, 'B'), get(0x4001DAE4, 'h'), get(0x4001DAE6, 'h'), bool(get(0x4001E184, 'B')))
  assert actual == (expected.owner, expected.torque_accel, expected.brake_accel, expected.latch_e184), (i, actual, expected)
  assert (get(0x4001DAF2, 'B'), get(0x4001DC30, 'H'), get(0x4001E170, 'B')) == (es.submode, es.active_timer, es.history_e170)
print('20,000 allocation + submode comparisons passed')
for i in range(10000):
  init()
  a = r.choice([-6000, r.randrange(-4000, 3001)])
  b = r.choice([a, 3000, r.randrange(-4000, 3001)])
  minimum = r.randrange(-3000, 1)
  integ = r.randrange(-2000, 2001)
  prev = r.choice([-1, 0, 1, 100])
  vpred = r.randrange(-100, 400)
  speed = r.randrange(3000)
  gear = r.randrange(2)
  flags = r.getrandbits(7) << 22
  vf = r.getrandbits(7) << 22
  timer = r.randrange(60)
  for addr, fmt, v in [
    (0x4001DC80, 'h', a),
    (0x4001DC82, 'h', b),
    (0x4001DEA4, 'h', minimum),
    (0x4001DEBA, 'h', integ),
    (0x4001DEC2, 'h', prev),
    (0x4001DEAE, 'h', vpred),
    (0x4001D998, 'h', speed),
    (0x4001DC9E, 'B', gear),
    (0x4001DC8C, 'I', flags),
    (0x4001D9AC, 'I', vf),
    (0x4001E1A4, 'H', timer),
  ]:
    put(addr, fmt, v)
  expected = ref.select_request(a, b, minimum, integ, prev, vpred, speed, gear, flags, vf, timer, lookup)
  lib.request(40)
  actual = (get(0x4001DEB4, 'h'), get(0x4001E147, 'B'), get(0x4001D9B5, 'B'), get(0x4001E1A4, 'H'))
  assert actual == (expected.request_milli, expected.state, expected.source, expected.timer_e1a4), (
    i,
    actual,
    expected,
    a,
    b,
    minimum,
    integ,
    prev,
    vpred,
    speed,
    hex(flags),
    lookup(0x7DE, vpred),
  )
print('10,000 request-selection comparisons passed')
for _i in range(10000):
  init()
  old = r.randrange(2)
  req = r.choice([-1, 0, 1])
  flags = r.getrandbits(7) << 22
  v8 = r.getrandbits(7) << 22
  v14 = r.getrandbits(7) << 22
  d16 = r.randrange(2)
  d994 = r.randrange(2)
  timer = r.randrange(2)
  for a, f, v in [
    (0x4001DF9C, 'B', old),
    (0x4001DEC2, 'h', req),
    (0x4001DC8C, 'I', flags),
    (0x4001D9A0, 'I', v8),
    (0x4001D9AC, 'I', v14),
    (0x4001D9B8, 'I', d16 << 16),
    (0x4001D994, 'h', d994),
    (0x4001E1A4, 'H', timer),
  ]:
    put(a, f, v)
  expected = ref.update_hold_flag(bool(old), req, flags, v8, v14, bool(d16), d994, timer)
  lib.hold(40)
  assert get(0x4001DF9C, 'B') == expected
print('10,000 hold-latch comparisons passed')
for _i in range(10000):
  init()
  t = r.randrange(-3000, 3001)
  v = r.randrange(-100, 3001)
  a = r.randrange(-6000, 3001)
  assert C.c_int16(lib.FUN_0013bb20(t, 0x4001E148, v)).value == ref.model_acceleration(t, v, ref.VehicleModel())
  assert C.c_int16(lib.FUN_0013bbc0(a, 0x4001E148, v)).value == ref.model_torque(a, v, ref.VehicleModel())
print('20,000 vehicle-model comparisons passed')
for i in range(10000):
  init()
  old = ref.FeedbackMemory(
    tuple(r.randrange(-3000, 2001) for _ in range(100)),
    r.randrange(100),
    r.randrange(-3000, 2001),
    r.randrange(-3000, 2001),
    r.randrange(5001),
    r.randrange(1201),
    r.randrange(-2000, 2001),
    r.randrange(10001),
    r.randrange(-2000000, 2000001),
    r.randrange(-500, 501),
    r.getrandbits(7) << 22,
    bool(r.randrange(2)),
  )
  selected = r.randrange(-3000, 2001)
  state = r.randrange(5)
  flags = r.getrandbits(7) << 22
  vf = r.getrandbits(7) << 22
  measured = r.randrange(-3000, 2001)
  speed = r.randrange(3001)
  owner = ref.Owner(r.randrange(3))
  olderowner = ref.Owner(r.randrange(3))
  gear = r.randrange(2)
  hold = bool(r.randrange(2))
  amin = r.randrange(-3000, 1)
  amax = r.randrange(0, 3001)
  filteredcap = r.randrange(-3000, 2001)
  torque = r.randrange(-650, 1501)
  tmax = r.randrange(1501)
  cls = r.choice([-1, 0, 1])
  alt = bool(r.randrange(2))
  difference = r.randrange(-3000, 3001)
  for off, fmt, value in [
    (0, 'h', selected),
    (2, 'h', old.corrected),
    (4, 'h', old.proportional),
    (6, 'h', ref.c_div(old.integral_accumulator, 1000)),
    (0xE, 'h', old.previous_request),
    (0xE0, 'B', old.history_index),
    (0xE2, 'H', old.reference_delay_ms),
    (0xE4, 'H', old.stable_request_ms),
    (0xE6, 'H', old.active_ms),
    (0xE8, 'B', hold),
    (0x293, 'B', state),
  ]:
    put(0x4001DEB4 + off, fmt, value)
  for j, value in enumerate(old.history):
    put(0x4001DEB4 + 0x18 + j * 2, 'h', value)
  for addr, fmt, value in [
    (0x4001E182, 'h', old.i_reference),
    (0x4001E188, 'i', old.integral_accumulator),
    (0x4001E1AC, 'i', old.integral_accumulator),
    (0x4001E17C, 'I', old.previous_request_flags),
    (0x4001E184, 'B', old.allocation_latch),
    (0x4001DC8C, 'I', flags),
    (0x4001D9AC, 'I', vf),
    (0x4001D99A, 'h', measured),
    (0x4001D998, 'h', speed),
    (0x4001DAEE, 'B', owner),
    (0x4001E171, 'B', olderowner),
    (0x4001DC9E, 'B', 0),
    (0x4001DC9F, 'B', 0 if gear else 1),
    (0x4001DEA0, 'h', filteredcap),
    (0x4001DEA4, 'h', amin),
    (0x4001DEA6, 'h', amax),
    (0x4001DAE8, 'h', torque),
    (0x4001DC94, 'h', tmax),
    (0x4001D8F2, 'h', cls),
    (0x4001D990, 'B', alt),
    (0x4001D8F4, 'h', difference),
  ]:
    put(addr, fmt, value)
  expected = ref.update_feedback(
    old, selected, state, flags, vf, measured, speed, owner, olderowner, bool(gear), hold, amin, amax, filteredcap, torque, tmax, cls, alt, difference, lookup
  )
  lib.feedback(40)
  actual = (
    get(0x4001DEB6, 'h'),
    get(0x4001DEB8, 'h'),
    get(0x4001E188, 'i'),
    get(0x4001E182, 'h'),
    get(0x4001DF96, 'H'),
    get(0x4001DF9A, 'H'),
    bool(get(0x4001E184, 'B')),
    get(0x4001DEC0, 'h'),
    bool(get(0x4001D9AC, 'I') & (1 << 27)),
  )
  e = expected.memory
  wanted = (
    e.corrected,
    e.proportional,
    e.integral_accumulator,
    e.i_reference,
    e.reference_delay_ms,
    e.active_ms,
    e.allocation_latch,
    expected.correction,
    expected.capability_ramp_active,
  )
  assert actual == wanted, (
    i,
    actual,
    wanted,
    old,
    selected,
    state,
    hex(flags),
    hex(vf),
    measured,
    speed,
    owner,
    olderowner,
    gear,
    hold,
    amin,
    amax,
    filteredcap,
  )
print('10,000 feedback comparisons passed')

# Cross-stage regression examples: retained 0xB, then 0xA, then torque.
previous = ref.RawAllocation(ref.Owner.BRAKE, 0, -200, True)
held = ref.allocate_acceleration(previous, 1, 1 << 26, 500, 0, -300, -100, False, 125, False, 3)
assert held == previous
submode = ref.select_brake_submode(held.owner, previous.owner, 100, True, False, False, False, False, False, False, 125, ref.BrakeSubmode(3, 0, 0))
assert ref.encode_brake_mode(held.owner, submode)[0] == 0xA
released = ref.allocate_acceleration(held, 1, 1 << 26, 500, 0, -300, -100, False, 125, False, submode.submode)
assert released == ref.RawAllocation(ref.Owner.TORQUE, -300, 0, True)
assert ref.publish_brake_acceleration(3000, -1500) == 2600
assert ref.publish_brake_acceleration(-3000, -1500) == -2600
object_flag = False
observed = []
for object_state in (2, 1, 1, 0):
  object_flag, state1 = ref.first_object_stop_flags(object_state, object_flag)
  observed.append((object_flag, state1))
assert observed == [(True, False), (True, True), (True, True), (False, False)]
assert ref.hold_variant_4_allowed(299, 300, 1, 2, 2)
assert not ref.hold_variant_4_allowed(300, 300, 1, 2, 2)
assert not ref.hold_variant_4_allowed(0, 300, 2, 2, 2)
print('Release-sequence, envelope, object-state and hold-boundary regressions passed')


# Stateful request -> feedback -> allocation/submode replay. External inputs are
# synthetic: this checks carried state and stage order, not supervisor reachability,
# torque generation, sensor scheduling or vehicle response.
sequence_coverage = {'request': set(), 'owner': set(), 'submode': set()}
for sequence in range(3):
  init()
  memory = ref.FeedbackMemory()
  allocation = ref.RawAllocation(ref.Owner.INACTIVE, 0, 0, True)
  older_owner = ref.Owner.INACTIVE
  brake_state = ref.BrakeSubmode(1, 0, 0)
  request_timer = 0
  ramp_flag = 0
  put(0x4001E184, 'B', 1)
  put(0x4001DAF2, 'B', 1)
  for cycle in range(2000):
    phase = (cycle // 25) % 8
    speed = (0, 149, 150, 500, 1600)[(cycle // 80 + sequence) % 5]
    a, b = ((0, 0), (400, 400), (-900, -1100), (-6000, -500), (300, 3000), (-700, -900), (600, 600), (500, 300))[phase]
    flags = (1 << 22) | ((phase != 0) << 26)
    if phase == 5:
      flags |= (1 << 25) | (1 << 23)
    if phase == 6:
      flags |= 1 << 28
    if phase == 7 and cycle % 3:
      flags |= 1 << 24
    vehicle_flags = ramp_flag | ((phase == 6) << 24)
    measured = (-200, 200, -700, -400, 300, -600, 0, 250)[phase] + sequence * 20
    minimum, maximum, cap = -350, 2000, -100
    torque, tmax = (300 if allocation.owner == ref.Owner.TORQUE else -650), 1600
    cls = -1 if speed >= 1200 and phase == 2 else 1 if phase == 6 else 0
    alternate = bool(sequence % 2)
    difference = (0, 100, -600, 0, 300, -100, 900, 200)[phase]
    hold = phase in (2, 3) and cycle % 25 > 10
    standstill = phase == 2 and speed < 150
    special = 0 if phase == 3 and cycle % 25 > 20 else 125
    gear = not (phase == 4 and cycle % 25 < 5)
    stop27, stop28 = phase == 2, phase == 3
    variant = bool((cycle // 50 + sequence) % 2)
    for addr, fmt, value in [
      (0x4001DC80, 'h', a),
      (0x4001DC82, 'h', b),
      (0x4001DEAE, 'h', speed),
      (0x4001DC8C, 'I', flags),
      (0x4001D9AC, 'I', vehicle_flags),
      (0x4001D99A, 'h', measured),
      (0x4001D998, 'h', speed),
      (0x4001DC9E, 'B', 1),
      (0x4001DC9F, 'B', 1 if gear else 0),
      (0x4001DEA0, 'h', cap),
      (0x4001DEA4, 'h', minimum),
      (0x4001DEA6, 'h', maximum),
      (0x4001DAE8, 'h', torque),
      (0x4001DC94, 'h', tmax),
      (0x4001D8F2, 'h', cls),
      (0x4001D990, 'B', alternate),
      (0x4001D8F4, 'h', difference),
      (0x4001DF9C, 'B', hold),
      (0x4001D9A0, 'I', int(standstill) << 25),
      (0x4001D91C, 'h', special),
      (0x4001D928, 'B', 1),
      (0x4001D8E2, 'B', variant),
      (0x4001DCC0, 'I', (int(stop27) << 27) | (int(stop28) << 28)),
    ]:
      put(addr, fmt, value)
    selected = ref.select_request(
      a, b, minimum, ref.c_div(memory.integral_accumulator, 1000), memory.previous_request, speed, speed, True, flags, vehicle_flags, request_timer, lookup
    )
    lib.request(40)
    assert (get(0x4001DEB4, 'h'), get(0x4001E147, 'B'), get(0x4001E1A4, 'H')) == (selected.request_milli, selected.state, selected.timer_e1a4), (
      'sequence request',
      sequence,
      cycle,
    )
    request_timer = selected.timer_e1a4
    result = ref.update_feedback(
      memory,
      selected.request_milli,
      selected.state,
      flags,
      vehicle_flags,
      measured,
      speed,
      allocation.owner,
      older_owner,
      gear,
      hold,
      minimum,
      maximum,
      cap,
      torque,
      tmax,
      cls,
      alternate,
      difference,
      lookup,
    )
    lib.feedback(40)
    memory = result.memory
    actual_memory = ref.FeedbackMemory(
      tuple(get(0x4001DECC + j * 2, 'h') for j in range(100)),
      get(0x4001DF94, 'B'),
      get(0x4001DEC2, 'h'),
      get(0x4001DEB6, 'h'),
      get(0x4001DF98, 'H'),
      get(0x4001DF96, 'H'),
      get(0x4001E182, 'h'),
      get(0x4001DF9A, 'H'),
      get(0x4001E188, 'i'),
      get(0x4001DEB8, 'h'),
      get(0x4001E17C, 'I'),
      bool(get(0x4001E184, 'B')),
    )
    assert actual_memory == memory, ('sequence feedback', sequence, cycle, actual_memory, memory)
    assert get(0x4001DEC0, 'h') == result.correction
    ramp_flag = int(result.capability_ramp_active) << 27
    assert get(0x4001D9AC, 'I') & (1 << 27) == ramp_flag
    prior = replace(allocation, latch_e184=memory.allocation_latch)
    correction_weight = 400 if prior.owner == ref.Owner.BRAKE else 200
    table = 0x708 if prior.owner == ref.Owner.BRAKE else 0x720 if cls == -1 and alternate else 0x714
    threshold = minimum + lookup(table, speed) + ref.c_div(correction_weight * result.correction, 1000)
    threshold += 50 if selected.state == 2 else 0
    allocation = ref.allocate_acceleration(
      prior, selected.state, flags, memory.corrected, result.correction, minimum, threshold, standstill, special, hold, brake_state.submode
    )
    brake_state = ref.select_brake_submode(allocation.owner, prior.owner, speed, True, False, hold, variant, stop27, stop28, standstill, special, brake_state)
    lib.allocate(40)
    assert (get(0x4001DAEE, 'B'), get(0x4001DAE4, 'h'), get(0x4001DAE6, 'h'), bool(get(0x4001E184, 'B'))) == (
      allocation.owner,
      allocation.torque_accel,
      allocation.brake_accel,
      allocation.latch_e184,
    ), ('sequence allocation', sequence, cycle)
    assert (get(0x4001DAF2, 'B'), get(0x4001DC30, 'H'), get(0x4001E170, 'B')) == (brake_state.submode, brake_state.active_timer, brake_state.history_e170), (
      'sequence submode',
      sequence,
      cycle,
    )
    older_owner = prior.owner
    assert get(0x4001E171, 'B') == older_owner
    memory = replace(memory, allocation_latch=allocation.latch_e184)
    # The full caller's envelope/retention stage is outside this three-stage test.
    sequence_coverage['request'].add(selected.state)
    sequence_coverage['owner'].add(int(allocation.owner))
    sequence_coverage['submode'].add(brake_state.submode)
assert sequence_coverage == {'request': set(range(5)), 'owner': set(range(3)), 'submode': set(range(1, 6))}, sequence_coverage
print('6,000 carried-state request/feedback/allocation cycles passed; all request states, owners and submodes exercised')

# Numeric auxiliary output compared with the full recovered 13a180. Supply
# branch conditions deliberately: disabled request -> ordinary; enabled with
# vehicle bit25 -> hold. This does not validate a whole supervisor trajectory.
aux_random = random.Random(23366550)
aux_coverage = set()
for i in range(10000):
  init()
  ordinary = bool(aux_random.randrange(2))
  owner = ref.Owner(aux_random.randrange(3))
  prior_owner = ref.Owner(aux_random.randrange(3))
  slew_enabled = bool(aux_random.randrange(2))
  speed = aux_random.randrange(3001)
  brake = aux_random.randrange(-5000, 2001)
  proportional = aux_random.randrange(-500, 501)
  integral = aux_random.randrange(-1000, 1001)
  rate = aux_random.randrange(-500, 501)
  previous_aux = aux_random.randrange(-2000, 1001)
  entry_torque = aux_random.randrange(-1000, 501)
  flags = (int(not ordinary) << 26) | (int(slew_enabled) << 22)
  for address, fmt, value in [
    (0x4001DAEE, 'B', owner), (0x4001E171, 'B', prior_owner),
    (0x4001D998, 'h', speed), (0x4001DAE6, 'h', brake),
    (0x4001DEB8, 'h', proportional), (0x4001DEBA, 'h', integral),
    (0x4001DEBE, 'h', rate), (0x4001DAEC, 'h', previous_aux),
    (0x4001DC90, 'h', entry_torque), (0x4001DC8C, 'I', flags),
    (0x4001D9A0, 'I', int(not ordinary) << 25),
  ]:
    put(address, fmt, value)
  put(0x400307F8, 'h', struct.unpack_from('>h', cal, 0x7F8)[0])
  expected = ref.auxiliary_torque_number(
    ordinary, owner, prior_owner, brake, proportional, integral, rate,
    previous_aux, entry_torque, slew_enabled,
    lambda acceleration, speed=speed: ref.model_torque(acceleration, speed, ref.VehicleModel()),
  )
  lib.hold(40)
  assert get(0x4001DAEC, 'h') == expected, ('auxiliary', i, ordinary, owner, prior_owner, expected)
  aux_coverage.add((ordinary, owner, prior_owner, slew_enabled))
assert len(aux_coverage) == 36
print('10,000 auxiliary numeric-output comparisons against recovered 13a180 passed')

# Illustrative regressions for the new floating-point excerpts. These are
# semantic boundary checks, NOT recovered-C or SPE/float32 equivalence checks.
channel = ref.SensorChannelMemory(2.0, True)
channel = ref.condition_dynamics_sensor(100.0, channel, accepted=False, initialize=False)
assert channel.value == 2.0 and not channel.previously_accepted
channel = ref.condition_dynamics_sensor(4.0, channel, accepted=True, initialize=False)
assert channel.value == 4.0  # Reacceptance seeds rather than slowly approaching.
channel = ref.condition_dynamics_sensor(14.0, channel, accepted=True, initialize=False)
assert abs(channel.value - 6.1) < 1e-12
assert ref.correct_sensor_geometry(-10.0, 10000.0) == 5.99951171875  # Product clamps first.
outputs = ref.split_sensor_bias_paths(2.0, 0.5, 0.2, 1.0, 0.0)
assert outputs.residual_input == 1.5 and outputs.compensated_acceleration == 0.5
assert ref.split_sensor_bias_paths(2.0, 0.5, 0.2, 1.0, 1.0).residual_input == 1.5
assert ref.retain_sensor_output(3.0, 1.0, (0, 0, 1, 0, 0)) == 1.0
assert ref.select_wheel_acceleration(100.0, 100.0, 2.0, 4.0, 0) == 3.0
residual = ref.update_sensor_wheel_residual(0.0, 0.0, ref.WheelResidualMemory(0.0, 100.0, 0.0), False, False, False)
assert residual.residual_unclamped > 80.0 and 0.023 < residual.output < 0.024
seeded = ref.update_sensor_wheel_residual(10.0, 0.0, residual, False, True, True)
assert abs(seeded.output - 2.37930012) < 1e-12
assert ref.decode_hold_input_enums(1, 1, 0, 0, 0) == ref.HoldInputEnums(1, 1, 2)
assert ref.decode_hold_input_enums(3, 3, 3, 3, 3) == ref.HoldInputEnums(2, 0, 0)
assert ref.ratio_torque_output(ref.Owner.TORQUE, 100, 200, 500, 1000) == (25, 200)
assert ref.ratio_torque_output(ref.Owner.BRAKE, 100, 0, 500, 1000) == (-650, 1)
print('Sensor retention/bias/filter-state, hold-enum and ratio illustrative regressions passed')
