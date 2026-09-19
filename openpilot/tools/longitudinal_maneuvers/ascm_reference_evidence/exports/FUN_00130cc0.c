
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00130cc0(undefined8 param_1)

{
  byte bVar1;
  byte bVar2;
  uint uVar3;
  undefined4 uVar4;
  int iVar5;
  short sVar7;
  ulonglong uVar6;
  bool bVar8;
  bool bVar9;
  uint uVar10;
  undefined4 *puVar11;
  undefined4 *puVar12;
  char cVar16;
  float fVar14;
  undefined8 uVar13;
  undefined4 *puVar15;
  int iVar17;
  uint uVar18;
  int iVar19;
  int iVar20;
  undefined4 *puVar21;
  int iVar22;
  ulonglong uVar23;
  longlong lVar24;
  undefined4 local_230;
  undefined4 local_22c;
  undefined4 local_228;
  undefined4 local_224;
  undefined4 local_220;
  undefined4 local_21c;
  undefined4 local_218;
  undefined1 local_214 [68];
  float local_1d0 [7];
  float local_1b4;
  char local_1a8 [8];
  float local_1a0 [3];
  byte local_194 [404];
  
  FUN_001338f0();
  FUN_001344b0(param_1);
  iVar17 = 0;
  if (*(char *)(DAT_40037a40 + 0x625) == '\x01') {
    DAT_4001dc24 = ((uint)LZCOUNT(DAT_4001d966 - 1) & 0x20) << 0x18 | DAT_4001dc24 & 0xdfffffff;
  }
  else {
    if ((DAT_4001d966 == 1) || (DAT_4001d93b == '\x01')) {
      iVar17 = 1;
    }
    DAT_4001dc24 = iVar17 << 0x1d | DAT_4001dc24 & 0xdfffffff;
  }
  DAT_4001dc1c = DAT_4001da0c;
  DAT_4001dc1e = DAT_4001da0e;
  DAT_4001dc2c = 0;
  DAT_4001dc2d = 0;
  uVar18 = DAT_4001d9c6 + 0xfe & 0xff;
  DAT_4001dc18 = DAT_4001da04 & 0x20000000 |
                 (~uVar18 | 2) - (2 - uVar18 >> 1) >> 6 & 0x2000000 | DAT_4001dc18 & 0x1ffffff;
  DAT_4001dc24 = ((uint)LZCOUNT(DAT_4001d963 - 3) & 0x20) << 0x1a |
                 (DAT_4001d957 & 1) << 0x1e | DAT_4001dc24 & 0x3fffffff;
  DAT_4001dc28 = (DAT_4001d93f & 1) << 0x1a | DAT_4001dc28 & 0x3fffff;
  cVar16 = FUN_000c0c10();
  if (cVar16 == '\0') {
    DAT_4001dc28 = DAT_4001dc28 & 0xfeffffff;
    DAT_4001d8b6 = 0;
  }
  else if ((ushort)((int)(uint)*(ushort *)(DAT_40037a40 + 0x2c4) / (int)param_1) < DAT_4001d8b6) {
    DAT_4001dc28 = DAT_4001dc28 | 0x1000000;
  }
  else {
    DAT_4001dc28 = DAT_4001dc28 & 0xfeffffff;
    DAT_4001d8b6 = DAT_4001d8b6 + 1;
  }
  FUN_00045520(0x19);
  fVar14 = (float)FUN_000c0d50();
  fVar14 = fVar14 * 1000.0;
  if (fVar14 < 0.0) {
    uVar23 = (ulonglong)-fVar14;
    if (0x80000000 < uVar23) {
      uVar23 = 0;
    }
    DAT_4001dc12 = -(short)uVar23;
  }
  else {
    uVar23 = (ulonglong)fVar14;
    if (0x7fffffff < uVar23) {
      uVar23 = 0x7fffffff;
    }
    DAT_4001dc12 = (short)uVar23;
  }
  fVar14 = (float)FUN_000bfa60();
  fVar14 = fVar14 * 1000.0;
  if (fVar14 < 0.0) {
    uVar23 = (ulonglong)-fVar14;
    if (0x80000000 < uVar23) {
      uVar23 = 0;
    }
    DAT_4001dc14 = -(short)uVar23;
  }
  else {
    uVar23 = (ulonglong)fVar14;
    if (0x7fffffff < uVar23) {
      uVar23 = 0x7fffffff;
    }
    DAT_4001dc14 = (short)uVar23;
  }
  fVar14 = (float)FUN_000c0de0();
  fVar14 = fVar14 * 100.0;
  if (fVar14 < 0.0) {
    uVar23 = (ulonglong)-fVar14;
    if (0x80000000 < uVar23) {
      uVar23 = 0;
    }
    DAT_4001dc10 = -(short)uVar23;
  }
  else {
    uVar23 = (ulonglong)fVar14;
    if (0x7fffffff < uVar23) {
      uVar23 = 0x7fffffff;
    }
    DAT_4001dc10 = (short)uVar23;
  }
  FUN_00045560(0x19);
  DAT_4001dc20 = 18000;
  FUN_00045520(0x17);
  uVar13 = FUN_000c2c20();
  FUN_000bc1a0(local_1d0,uVar13,0x180);
  FUN_00045560(0x17);
  local_1b4 = local_1b4 * 1000.0;
  if (local_1b4 < 0.0) {
    uVar23 = (ulonglong)-local_1b4;
    if (0x80000000 < uVar23) {
      uVar23 = 0;
    }
    sVar7 = -(short)uVar23;
  }
  else {
    uVar23 = (ulonglong)local_1b4;
    if (0x7fffffff < uVar23) {
      uVar23 = 0x7fffffff;
    }
    sVar7 = (short)uVar23;
  }
  if ((((byte)(local_1a8[0] - 2U) < 2) && (local_194[0] != 4)) && (local_194[0] != 5)) {
    DAT_4001dc74 = FUN_0012e5e0(sVar7,DAT_4001dc74,600 / (int)param_1);
  }
  else {
    DAT_4001dc74 = 0;
  }
  uVar18 = (uint)LZCOUNT(local_194[0] - 1) >> 5;
  DAT_4001dc78 = (byte)uVar18;
  DAT_4001dc79 = (byte)((uint)LZCOUNT(local_194[0] - 2) >> 5);
  if ((DAT_4001dc7a == '\x01') && (uVar18 == 1)) {
    DAT_4001dc79 = 1;
  }
  if ((*(char *)(DAT_40037a40 + 0x8c7) == '\0') || (DAT_4001dc10 < *(short *)(DAT_40037a40 + 0x8c8))
     ) {
    uVar23 = -(ulonglong)(byte)local_1a8[4] >> 0x1f & 1;
  }
  else {
    uVar23 = 0;
  }
  DAT_4001d8b1 = (undefined1)((uint)LZCOUNT(local_194[3] - 1) >> 5);
  uVar18 = 0;
  DAT_4001dc7a = DAT_4001dc79;
  do {
    iVar17 = (uVar18 & 0xff) * 0x44;
    bVar2 = *(byte *)(DAT_4001d7e0 + iVar17 + 0x16);
    uVar3 = *(uint *)(DAT_4001d7e0 + iVar17 + 0x10);
    FUN_00136ba0();
    if ((uVar18 & 0xff) < 6) {
      uVar10 = uVar18 & 0xff;
      iVar5 = uVar10 * 0x40;
      bVar1 = local_194[iVar5 + 1];
      if (bVar1 == 0) {
        *(undefined1 *)(DAT_4001d7e0 + iVar17 + 0xd) = 1;
      }
      else if (bVar1 == 1) {
        *(undefined1 *)(DAT_4001d7e0 + iVar17 + 0xd) = 1;
      }
      else if (bVar1 == 2) {
        *(undefined1 *)(DAT_4001d7e0 + iVar17 + 0xd) = 2;
      }
      else if (bVar1 == 3) {
        *(undefined1 *)(DAT_4001d7e0 + iVar17 + 0xd) = 3;
      }
      else if (bVar1 == 4) {
        *(undefined1 *)(DAT_4001d7e0 + iVar17 + 0xd) = 4;
      }
      else {
        *(undefined1 *)(DAT_4001d7e0 + iVar17 + 0xd) = 1;
      }
      if ((uVar18 & 0xff) == 0) {
        DAT_4001dc18 = -(uint)(byte)local_1a8[iVar5 + 2] >> 4 & 0x8000000 |
                       DAT_4001dc18 & 0xf7ffffff;
      }
      fVar14 = local_1d0[uVar10 * 0x10 + 1] * 100.0;
      if (fVar14 < 0.0) {
        uVar6 = (ulonglong)-fVar14;
        if (0x80000000 < uVar6) {
          uVar6 = 0;
        }
        sVar7 = -(short)uVar6;
      }
      else {
        uVar6 = (ulonglong)fVar14;
        if (0x7fffffff < uVar6) {
          uVar6 = 0x7fffffff;
        }
        sVar7 = (short)uVar6;
      }
      *(short *)(DAT_4001d7e0 + iVar17 + 6) = sVar7;
      fVar14 = local_1d0[uVar10 * 0x10] * 100.0;
      if (fVar14 < 0.0) {
        uVar6 = (ulonglong)-fVar14;
        if (0x80000000 < uVar6) {
          uVar6 = 0;
        }
        sVar7 = -(short)uVar6;
      }
      else {
        uVar6 = (ulonglong)fVar14;
        if (0x7fffffff < uVar6) {
          uVar6 = 0x7fffffff;
        }
        sVar7 = (short)uVar6;
      }
      *(short *)(DAT_4001d7e0 + iVar17 + 4) = sVar7;
      *(char *)(DAT_4001d7e0 + iVar17 + 0x16) = local_1a8[iVar5 + 3];
      *(byte *)(DAT_4001d7e0 + iVar17 + 0x38) = bVar2;
      iVar22 = 0;
      bVar9 = false;
      bVar8 = true;
      if ((local_1a8[iVar5] != '\x03') && (bVar8 = true, local_1a8[iVar5] != '\x02')) {
        bVar8 = false;
      }
      if ((bVar8) && (bVar9 = true, local_194[iVar5] == 4)) {
        bVar9 = false;
      }
      if ((bVar9) && (iVar22 = 1, local_194[iVar5] == 5)) {
        iVar22 = 0;
      }
      *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) =
           iVar22 << 0x19 | *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) & 0xfdffffff;
      iVar19 = 0;
      bVar8 = false;
      iVar22 = (uVar18 & 0xff) * 0x40;
      if ((local_1a8[iVar22] == '\x03') && (bVar8 = true, local_194[iVar22] == 4)) {
        bVar8 = false;
      }
      if ((bVar8) && (iVar19 = 1, local_194[iVar22] == 5)) {
        iVar19 = 0;
      }
      *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) =
           iVar19 << 0x1f | *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) & 0x7fffffff;
      *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) =
           ((uint)LZCOUNT(local_194[iVar5] - 3) & 0x20) << 0x15 |
           *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) & 0xfbffffff;
      *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) =
           ((uint)(byte)local_1a8[iVar5 + 3] - (uint)bVar2 |
           (uint)bVar2 - (uint)(byte)local_1a8[iVar5 + 3]) >> 2 & 0x20000000 |
           *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) & 0xdfffffff;
      if ((uVar18 & 0xff) == 0) {
        *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) =
             (DAT_4001dc78 & 1) << 0x1c | *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) & 0xefffffff;
        *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) =
             (DAT_4001dc79 & 1) << 0x1b | *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) & 0xf7ffffff;
        iVar19 = DAT_4001d7e0 + iVar17;
        if ((*(uint *)(iVar19 + 0x10) >> 0x1d & 1) == 0) {
          iVar20 = 0;
          if (((uVar3 >> 0x18 & 1) != 0) || (uVar23 != 0)) {
            iVar20 = 1;
          }
          *(uint *)(iVar19 + 0x10) = iVar20 << 0x18 | *(uint *)(iVar19 + 0x10) & 0xfeffffff;
        }
        else {
          *(uint *)(iVar19 + 0x10) = (int)uVar23 << 0x18 | *(uint *)(iVar19 + 0x10) & 0xfeffffff;
        }
      }
      else {
        *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) =
             ((uint)LZCOUNT(local_194[iVar5] - 1) & 0x20) << 0x17 |
             *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) & 0xefffffff;
        *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) =
             ((uint)LZCOUNT(local_194[iVar5] - 2) & 0x20) << 0x16 |
             *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) & 0xf7ffffff;
        *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) =
             *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) & 0xfeffffff;
      }
      iVar19 = 0;
      bVar8 = false;
      if ((local_1a8[iVar22] == '\x02') && (bVar8 = true, local_194[iVar5] == 4)) {
        bVar8 = false;
      }
      if ((bVar8) && (iVar19 = 1, local_194[iVar5] == 5)) {
        iVar19 = 0;
      }
      *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) =
           iVar19 << 0x1e | *(uint *)(DAT_4001d7e0 + iVar17 + 0x10) & 0xbfffffff;
      *(undefined1 *)(DAT_4001d7e0 + iVar17 + 0xc) = 0xff;
      fVar14 = local_1d0[uVar10 * 0x10 + 5] * 1000.0;
      if (fVar14 < 0.0) {
        uVar6 = (ulonglong)-fVar14;
        if (0x80000000 < uVar6) {
          uVar6 = 0;
        }
        sVar7 = -(short)uVar6;
      }
      else {
        uVar6 = (ulonglong)fVar14;
        if (0x7fffffff < uVar6) {
          uVar6 = 0x7fffffff;
        }
        sVar7 = (short)uVar6;
      }
      *(short *)(DAT_4001d7e0 + iVar17 + 10) = sVar7;
      fVar14 = local_1d0[uVar10 * 0x10 + 3] * 100.0;
      if (fVar14 < 0.0) {
        uVar6 = (ulonglong)-fVar14;
        if (0x80000000 < uVar6) {
          uVar6 = 0;
        }
        sVar7 = -(short)uVar6;
      }
      else {
        uVar6 = (ulonglong)fVar14;
        if (0x7fffffff < uVar6) {
          uVar6 = 0x7fffffff;
        }
        sVar7 = (short)uVar6;
      }
      *(short *)(DAT_4001d7e0 + iVar17 + 2) = sVar7;
      fVar14 = local_1d0[uVar10 * 0x10 + 4] * 1000.0;
      if (fVar14 < 0.0) {
        uVar6 = (ulonglong)-fVar14;
        if (0x80000000 < uVar6) {
          uVar6 = 0;
        }
        sVar7 = -(short)uVar6;
      }
      else {
        uVar6 = (ulonglong)fVar14;
        if (0x7fffffff < uVar6) {
          uVar6 = 0x7fffffff;
        }
        sVar7 = (short)uVar6;
      }
      *(short *)(DAT_4001d7e0 + iVar17 + 8) = sVar7;
      fVar14 = local_1d0[uVar10 * 0x10 + 2] * 100.0;
      if (fVar14 < 0.0) {
        uVar6 = (ulonglong)-fVar14;
        if (0x80000000 < uVar6) {
          uVar6 = 0;
        }
        sVar7 = -(short)uVar6;
      }
      else {
        uVar6 = (ulonglong)fVar14;
        if (0x7fffffff < uVar6) {
          uVar6 = 0x7fffffff;
        }
        sVar7 = (short)uVar6;
      }
      *(short *)(DAT_4001d7e0 + iVar17) = sVar7;
      fVar14 = local_1a0[uVar10 * 0x10] * 100.0;
      if (fVar14 < 0.0) {
        uVar6 = (ulonglong)-fVar14;
        if (0x80000000 < uVar6) {
          uVar6 = 0;
        }
        sVar7 = -(short)uVar6;
      }
      else {
        uVar6 = (ulonglong)fVar14;
        if (0x7fffffff < uVar6) {
          uVar6 = 0x7fffffff;
        }
        sVar7 = (short)uVar6;
      }
      *(short *)(DAT_4001d7e0 + iVar17 + 0x14) = sVar7;
      uVar6 = (ulonglong)local_1d0[uVar10 * 0x10 + 8];
      if (0x7fffffff < uVar6) {
        uVar6 = 0x7fffffff;
      }
      *(char *)(DAT_4001d7e0 + iVar17 + 0x2a) = (char)uVar6;
      cVar16 = local_1a8[iVar5 + 1];
      if (cVar16 == '\x01') {
        *(undefined1 *)(DAT_4001d7e0 + iVar17 + 0x1e) = 0;
      }
      else if (cVar16 == '\x02') {
        *(undefined1 *)(DAT_4001d7e0 + iVar17 + 0x1e) = 0xff;
      }
      else if (cVar16 == '\x03') {
        *(undefined1 *)(DAT_4001d7e0 + iVar17 + 0x1e) = 1;
      }
      else {
        *(undefined1 *)(DAT_4001d7e0 + iVar17 + 0x1e) = 0;
      }
      fVar14 = local_1d0[uVar10 * 0x10 + 9] * 100.0;
      if (fVar14 < 0.0) {
        uVar6 = (ulonglong)-fVar14;
        if (0x80000000 < uVar6) {
          uVar6 = 0;
        }
        sVar7 = -(short)uVar6;
      }
      else {
        uVar6 = (ulonglong)fVar14;
        if (0x7fffffff < uVar6) {
          uVar6 = 0x7fffffff;
        }
        sVar7 = (short)uVar6;
      }
      *(short *)(DAT_4001d7e0 + iVar17 + 0x1c) = sVar7;
      fVar14 = local_1d0[uVar10 * 0x10 + 4] * 1000.0;
      if (fVar14 < 0.0) {
        uVar6 = (ulonglong)-fVar14;
        if (0x80000000 < uVar6) {
          uVar6 = 0;
        }
        sVar7 = -(short)uVar6;
      }
      else {
        uVar6 = (ulonglong)fVar14;
        if (0x7fffffff < uVar6) {
          uVar6 = 0x7fffffff;
        }
        sVar7 = (short)uVar6;
      }
      *(short *)(DAT_4001d7e0 + iVar17 + 0x1a) = DAT_4001d8e6 + sVar7;
      fVar14 = local_1d0[uVar10 * 0x10 + 6] * 100.0;
      if (fVar14 < 0.0) {
        uVar6 = (ulonglong)-fVar14;
        if (0x80000000 < uVar6) {
          uVar6 = 0;
        }
        sVar7 = -(short)uVar6;
      }
      else {
        uVar6 = (ulonglong)fVar14;
        if (0x7fffffff < uVar6) {
          uVar6 = 0x7fffffff;
        }
        sVar7 = (short)uVar6;
      }
      *(short *)(DAT_4001d7e0 + iVar17 + 0x18) = sVar7;
      *(uint *)(DAT_4001d7e0 + iVar17 + 0x2c) = *(uint *)(DAT_4001d7e0 + iVar17 + 0x2c) & 0x7fffffff
      ;
      *(uint *)(DAT_4001d7e0 + iVar17 + 0x2c) = *(uint *)(DAT_4001d7e0 + iVar17 + 0x2c) & 0xefffffff
      ;
      *(uint *)(DAT_4001d7e0 + iVar17 + 0x2c) = *(uint *)(DAT_4001d7e0 + iVar17 + 0x2c) & 0xdfffffff
      ;
      *(uint *)(DAT_4001d7e0 + iVar17 + 0x2c) = *(uint *)(DAT_4001d7e0 + iVar17 + 0x2c) & 0xbfffffff
      ;
      *(undefined2 *)(DAT_4001d7e0 + iVar17 + 0x28) = *(undefined2 *)(DAT_40037a40 + 0x55c);
      *(undefined2 *)(DAT_4001d7e0 + iVar17 + 0x26) = 0;
      *(undefined2 *)(DAT_4001d7e0 + iVar17 + 0x24) = *(undefined2 *)(DAT_40037a40 + 0x5a0);
      *(undefined2 *)(DAT_4001d7e0 + iVar17 + 0x22) = *(undefined2 *)(DAT_40037a40 + 0x5a0);
      *(undefined2 *)(DAT_4001d7e0 + iVar17 + 0x20) = *(undefined2 *)(DAT_40037a40 + 0x5a2);
    }
    uVar18 = uVar18 + 1;
  } while (uVar18 < 6);
  if (*(char *)(DAT_40037a40 + 0x6b0) == '\x01') {
    FUN_00134660(param_1);
  }
  lVar24 = 8;
  puVar11 = (undefined4 *)0x4001db84;
  puVar12 = &local_218;
  do {
    puVar21 = puVar12;
    puVar15 = puVar11;
    uVar4 = puVar15[2];
    puVar21[1] = puVar15[1];
    puVar21[2] = uVar4;
    lVar24 = lVar24 + -1;
    puVar11 = puVar15 + 2;
    puVar12 = puVar21 + 2;
  } while (lVar24 != 0);
  puVar21[3] = puVar15[3];
  local_230 = DAT_4001d978;
  local_22c = DAT_4001d97c;
  local_228 = DAT_4001d980;
  local_224 = DAT_4001d984;
  local_220 = DAT_4001d988;
  local_21c = DAT_4001d98c;
  local_218 = _DAT_4001d990;
  FUN_001361c0(param_1,&DAT_4001dc10,DAT_4001d7e0,&local_230,&DAT_4001dbcc,local_214,&DAT_4001db08);
  lVar24 = 8;
  puVar11 = (undefined4 *)0x4001db84;
  puVar12 = &local_218;
  do {
    puVar21 = puVar12;
    puVar15 = puVar11;
    uVar4 = puVar21[2];
    puVar15[1] = puVar21[1];
    puVar15[2] = uVar4;
    lVar24 = lVar24 + -1;
    puVar11 = puVar15 + 2;
    puVar12 = puVar21 + 2;
  } while (lVar24 != 0);
  puVar15[3] = puVar21[3];
  DAT_4001d978 = local_230;
  DAT_4001d97c = local_22c;
  DAT_4001d980 = local_228;
  DAT_4001d984 = local_224;
  DAT_4001d988 = local_220;
  DAT_4001d98c = local_21c;
  _DAT_4001d990 = local_218;
  return;
}

