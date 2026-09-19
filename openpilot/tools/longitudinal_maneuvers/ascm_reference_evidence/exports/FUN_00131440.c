
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_00131440(undefined8 param_1)

{
  short sVar1;
  undefined *puVar2;
  char cVar3;
  uint uVar4;
  uint uVar5;
  uint uVar6;
  uint uVar7;
  undefined4 *puVar8;
  undefined **ppuVar9;
  undefined4 *puVar12;
  char cVar18;
  uint uVar13;
  float fVar14;
  int iVar15;
  char cVar19;
  ushort uVar16;
  undefined2 uVar17;
  ulonglong uVar10;
  undefined8 uVar11;
  undefined **ppuVar20;
  bool bVar21;
  char unaff_r28;
  short sVar22;
  longlong lVar23;
  undefined *local_74;
  undefined1 local_70 [112];
  
  iVar15 = (int)param_1;
  if (DAT_4001d8b0 == '\0') {
    DAT_4001d8b0 = '\x01';
    FUN_00139e50();
    FUN_00139820();
    FUN_00139ef0(&DAT_4001deb4);
    DAT_4001d8b8 = (undefined2)((int)(uint)*(ushort *)(DAT_40037a40 + 0x1a) / iVar15);
    DAT_4001d8ba = (undefined2)((int)(uint)*(ushort *)(DAT_40037a40 + 0x2c2) / iVar15);
  }
  FUN_00139e50();
  lVar23 = 8;
  puVar8 = (undefined4 *)0x4001db84;
  ppuVar9 = &local_74;
  do {
    ppuVar20 = ppuVar9;
    puVar12 = puVar8;
    puVar2 = (undefined *)puVar12[2];
    ppuVar20[1] = (undefined *)puVar12[1];
    ppuVar20[2] = puVar2;
    lVar23 = lVar23 + -1;
    puVar8 = puVar12 + 2;
    ppuVar9 = ppuVar20 + 2;
  } while (lVar23 != 0);
  ppuVar20[3] = (undefined *)puVar12[3];
  FUN_0012dd80(&DAT_4001dac4,DAT_4001d92c == '\x01');
  FUN_0012dd80(&DAT_4001dacc,DAT_4001d92d == '\x01');
  FUN_0012dd80(&DAT_4001dac8,DAT_4001d92e == '\x01');
  FUN_0012dd80(&DAT_4001dad0,DAT_4001d92f == '\x01');
  FUN_0012dd80(&DAT_4001dabc,DAT_4001d92b == '\x01');
  FUN_0012dd80(&DAT_4001dab8,DAT_4001d92a == '\x01');
  FUN_0012dd80(&DAT_4001dadc,DAT_4001d930 == '\x02');
  FUN_0012dd80(&DAT_4001dad4,DAT_4001d928 == '\x01');
  FUN_0012dd80(&DAT_4001dac0,DAT_4001d929 == '\x01');
  FUN_0012dd80(&DAT_4001dae0,DAT_4001d959 == '\x01');
  if (*(char *)(DAT_40037a40 + 0x623) == '\0') {
    if ((*(char *)(DAT_40037a40 + 0x670) == '\x01') && (DAT_4001d931 == '\x01')) {
      DAT_4001dc2e = (*(char *)(DAT_40037a40 + 0x5f4) + -10) * '\n';
    }
    if ((*(char *)(DAT_40037a40 + 0x670) == '\x01') && (DAT_4001d931 == '\x01')) {
      DAT_4001dc2e = (*(char *)(DAT_40037a40 + 0x5f4) + -10) * '\n';
    }
    else {
      cVar18 = FUN_0012dde0(&DAT_4001dadc,DAT_4001da74 >> 0x1d & 1);
      if ((cVar18 == '\x01') ||
         (cVar18 = FUN_0012de40(&DAT_4001dadc,1,DAT_4001da74 >> 0x1d & 1,(short)(2000 / iVar15),
                                (short)(1000 / iVar15)), cVar18 == '\x01')) {
        cVar18 = (*(char *)(DAT_40037a40 + 0x5ee) + -10) * '\n';
        if (DAT_4001dc2e == cVar18) {
          cVar18 = (*(char *)(DAT_40037a40 + 0x5f4) + -10) * '\n';
        }
        else {
          cVar19 = (*(char *)(DAT_40037a40 + 0x5f1) + -10) * '\n';
          if ((DAT_4001dc2e != cVar19) &&
             (cVar3 = (*(char *)(DAT_40037a40 + 0x5f4) + -10) * '\n', cVar18 = cVar19,
             DAT_4001dc2e != cVar3)) {
            cVar18 = cVar3;
          }
        }
        DAT_4001dc2e = cVar18;
        DAT_4001dc38 = DAT_4001dc2e;
      }
    }
  }
  else {
    if ((*(char *)(DAT_40037a40 + 0x670) == '\x01') && (DAT_4001d931 == '\x01')) {
      DAT_4001dc2e = (*(char *)(DAT_40037a40 + 0x5f4) + -10) * '\n';
    }
    if ((*(char *)(DAT_40037a40 + 0x670) == '\x01') && (DAT_4001d931 == '\x01')) {
      DAT_4001dc2e = (*(char *)(DAT_40037a40 + 0x5f4) + -10) * '\n';
    }
    else {
      cVar18 = FUN_0012dde0(&DAT_4001dadc,DAT_4001da74 >> 0x1d & 1);
      if ((cVar18 == '\x01') ||
         (cVar18 = FUN_0012de40(&DAT_4001dadc,1,DAT_4001da74 >> 0x1d & 1,(short)(2000 / iVar15),
                                (short)(1000 / iVar15)), cVar18 == '\x01')) {
        cVar18 = (*(char *)(DAT_40037a40 + 0x5f4) + -10) * '\n';
        if (DAT_4001dc2e == cVar18) {
          DAT_4001dc2e = (*(char *)(DAT_40037a40 + 0x5f3) + -10) * '\n';
        }
        else if (DAT_4001dc2e == (char)((*(char *)(DAT_40037a40 + 0x5f3) + -10) * '\n')) {
          DAT_4001dc2e = (*(char *)(DAT_40037a40 + 0x5f2) + -10) * '\n';
        }
        else if (DAT_4001dc2e == (char)((*(char *)(DAT_40037a40 + 0x5f2) + -10) * '\n')) {
          DAT_4001dc2e = (*(char *)(DAT_40037a40 + 0x5f1) + -10) * '\n';
        }
        else if (DAT_4001dc2e == (char)((*(char *)(DAT_40037a40 + 0x5f1) + -10) * '\n')) {
          DAT_4001dc2e = (*(char *)(DAT_40037a40 + 0x5f0) + -10) * '\n';
        }
        else if (DAT_4001dc2e == (char)((*(char *)(DAT_40037a40 + 0x5f0) + -10) * '\n')) {
          DAT_4001dc2e = (*(char *)(DAT_40037a40 + 0x5ef) + -10) * '\n';
        }
        else if (DAT_4001dc2e == (char)((*(char *)(DAT_40037a40 + 0x5ef) + -10) * '\n')) {
          DAT_4001dc2e = (*(char *)(DAT_40037a40 + 0x5ee) + -10) * '\n';
        }
        else {
          cVar19 = (*(char *)(DAT_40037a40 + 0x5ee) + -10) * '\n';
          bVar21 = DAT_4001dc2e != cVar19;
          DAT_4001dc2e = cVar19;
          if (bVar21) {
            DAT_4001dc2e = cVar18;
          }
        }
        DAT_4001dc38 = DAT_4001dc2e;
      }
    }
  }
  DAT_4001da3c = 1;
  DAT_4001da3d = 1;
  DAT_4001d8d0 = DAT_4001d8d0 & 0xbfffffff;
  DAT_4001d8d6 = 0xff;
  DAT_4001d8d7 = 1;
  DAT_4001d8c0 = 0;
  FUN_00045520(0x14);
  uVar13 = FUN_000bfa90();
  DAT_4001d8c8 = ((uint)LZCOUNT(uVar13 & 0xff) & 0x20) << 0x1a | DAT_4001d8c8 & 0x7fffffff;
  FUN_00132910();
  fVar14 = (float)FUN_000bfa60();
  fVar14 = fVar14 * 1000.0;
  if (fVar14 < 0.0) {
    uVar10 = (ulonglong)-fVar14;
    if (0x80000000 < uVar10) {
      uVar10 = 0;
    }
    DAT_4001d8c4 = -(short)uVar10;
  }
  else {
    uVar10 = (ulonglong)fVar14;
    if (0x7fffffff < uVar10) {
      uVar10 = 0x7fffffff;
    }
    DAT_4001d8c4 = (short)uVar10;
  }
  FUN_00045560(0x14);
  if (*(char *)(DAT_40037a40 + 0x5df) == '\x01') {
    FUN_00132650(param_1);
  }
  else {
    FUN_00132480();
  }
  FUN_00045520(0x22);
  uVar13 = FUN_000c6260();
  DAT_4001d8d0 = ((uint)LZCOUNT(uVar13 & 0xff) & 0x20) << 0x1a | DAT_4001d8d0 & 0x7fffffff;
  uVar13 = FUN_000c60d0();
  sVar22 = (short)((int)((uVar13 & 0xffff) * 100) >> 6);
  FUN_00045560(0x22);
  if (DAT_4001d931 == '\x01') {
    if ((int)DAT_4001d8d0 < 0) {
      sVar1 = *(short *)(DAT_40037a40 + 0x672);
      DAT_4001d8d8 = ((char)((int)sVar1 / 100) + (char)(sVar1 >> 7)) -
                     (char)((longlong)(int)sVar1 * 0x51eb851f >> 0x3f);
    }
    else {
      sVar1 = *(short *)(DAT_40037a40 + 0x672);
      if (((longlong)sVar1 & 0x80000000U) == 0) {
        fVar14 = (float)(int)sVar1;
      }
      else {
        fVar14 = -(float)-(int)sVar1;
      }
      uVar10 = (ulonglong)((fVar14 / *(float *)(DAT_40037a40 + 0x8e4)) / 100.0);
      if (0x7fffffff < uVar10) {
        uVar10 = 0x7fffffff;
      }
      DAT_4001d8d8 = (char)uVar10;
    }
  }
  else {
    sVar1 = *(short *)(DAT_40037a40 + 0x5e2);
    DAT_4001d8d8 = ((char)((int)sVar1 / 100) + (char)(sVar1 >> 7)) -
                   (char)((longlong)(int)sVar1 * 0x51eb851f >> 0x3f);
  }
  DAT_4001d8f0 = FUN_0012e3e0(DAT_40037a40 + 0x636,6,(longlong)sVar22);
  DAT_4001d8d4 = sVar22;
  if (-1 < (int)DAT_4001d8d0) {
    if (((longlong)sVar22 & 0x80000000U) == 0) {
      fVar14 = (float)(int)sVar22;
    }
    else {
      fVar14 = -(float)-(int)sVar22;
    }
    fVar14 = fVar14 / *(float *)(DAT_40037a40 + 0x8e4);
    if (fVar14 < 0.0) {
      uVar10 = (ulonglong)-fVar14;
      if (0x80000000 < uVar10) {
        uVar10 = 0;
      }
      DAT_4001d8d4 = -(short)uVar10;
    }
    else {
      uVar10 = (ulonglong)fVar14;
      if (0x7fffffff < uVar10) {
        uVar10 = 0x7fffffff;
      }
      DAT_4001d8d4 = (short)uVar10;
    }
  }
  if (*(char *)(DAT_40037a40 + 0x634) == '\x01') {
    iVar15 = (int)DAT_4001d8f0 * (int)DAT_4001d8d4;
    sVar22 = (short)(iVar15 >> 0x1f);
    DAT_4001d8d4 = ((short)(iVar15 / 10000) + sVar22) -
                   ((short)((short)(iVar15 / 0x27100000) + sVar22) >> 0xf);
  }
  FUN_00045520(0x1f);
  uVar13 = FUN_000c2f20();
  DAT_4001d9a4 = ((uint)LZCOUNT((uVar13 & 0xff) - 3) & 0x20) << 0x1a | DAT_4001d9a4 & 0x7fffffff;
  FUN_00045560(0x1f);
  FUN_00045520(0x1a);
  uVar13 = FUN_000c1050();
  DAT_4001d9b0 = ((uint)LZCOUNT(uVar13 & 0xff) & 0x20) << 0x18 | DAT_4001d9b0 & 0xdfffffff;
  uVar13 = FUN_000c1050();
  DAT_4001d9b0 = ((uint)LZCOUNT(uVar13 & 0xff) & 0x20) << 0x19 | DAT_4001d9b0 & 0xbfffffff;
  uVar13 = FUN_000c0ff0();
  DAT_4001d9b0 = ((uint)LZCOUNT(uVar13 & 0xff) & 0x20) << 0x1a | DAT_4001d9b0 & 0x7fffffff;
  FUN_00045560(0x1a);
  if (*(char *)(DAT_40037a40 + 0x5df) == '\0') {
    FUN_00045520(0x21);
    unaff_r28 = FUN_000c5bc0();
    FUN_00045560(0x21);
  }
  DAT_4001d9a4 = (DAT_4001d957 & 1) << 0x1e | DAT_4001d9a4 & 0xbfffffff;
  uVar13 = ((uint)LZCOUNT(DAT_4001d949 - 3) & 0x20) << 0x15;
  uVar4 = ((uint)LZCOUNT(DAT_4001d949 - 4) & 0x20) << 0x14;
  uVar5 = ((uint)LZCOUNT(DAT_4001d949 - 1) & 0x20) << 0x13;
  uVar6 = ((uint)LZCOUNT(DAT_4001d949 - 2) & 0x20) << 0x12;
  uVar7 = ((uint)LZCOUNT((uint)DAT_4001d949) & 0x20) << 0x11;
  if (*(char *)(DAT_40037a40 + 0x5df) == '\0') {
    if (unaff_r28 == '\x01') {
      _DAT_4001d9b4 = CONCAT13(1,DAT_4001d9b4_1);
    }
    else if (unaff_r28 == '\x02') {
      _DAT_4001d9b4 = CONCAT13(2,DAT_4001d9b4_1);
    }
    else if (unaff_r28 == '\0') {
      _DAT_4001d9b4 = _DAT_4001d9b4 & 0xffffff;
    }
    else {
      _DAT_4001d9b4 = _DAT_4001d9b4 & 0xffffff;
    }
  }
  if (DAT_4001d9b4 == '\0') {
    DAT_4001d9a0 = uVar7 | uVar6 | uVar5 | uVar4 | uVar13 | DAT_4001d9a0 & 0xf03fffff;
  }
  else {
    DAT_4001d9a0 = uVar7 | uVar6 | uVar5 | uVar4 | uVar13 | DAT_4001d9a0 & 0xf83fffff | 0x8000000;
  }
  FUN_00045520(0x19);
  fVar14 = (float)FUN_000c0d50();
  fVar14 = fVar14 * 1000.0;
  if (fVar14 < 0.0) {
    uVar10 = (ulonglong)-fVar14;
    if (0x80000000 < uVar10) {
      uVar10 = 0;
    }
    sVar22 = -(short)uVar10;
  }
  else {
    uVar10 = (ulonglong)fVar14;
    if (0x7fffffff < uVar10) {
      uVar10 = 0x7fffffff;
    }
    sVar22 = (short)uVar10;
  }
  _DAT_4001d99c = CONCAT22(sVar22,DAT_4001d99c_2);
  FUN_00045560(0x19);
  if (*(char *)(DAT_40037a40 + 0x625) == '\x01') {
    DAT_4001d9a4 = ((uint)LZCOUNT(DAT_4001d966 - 1) & 0x20) << 0x18 | DAT_4001d9a4 & 0xdfffffff;
  }
  else {
    iVar15 = 0;
    if ((DAT_4001d966 == 1) || (DAT_4001d93b == '\x01')) {
      iVar15 = 1;
    }
    DAT_4001d9a4 = iVar15 << 0x1d | DAT_4001d9a4 & 0xdfffffff;
  }
  DAT_4001d9a8 = ((uint)LZCOUNT((uint)DAT_4001d971) & 0x20) << 0x17 | DAT_4001d9a8 & 0xefffffff;
  DAT_4001d9ac = (DAT_4001d93f & 1) << 0x1a | DAT_4001d9ac & 0xf9ffffff;
  FUN_00045520(0x14);
  iVar15 = FUN_000bfc80();
  DAT_4001d9a8 = iVar15 << 0x1f | DAT_4001d9a8 & 0x7fffffff;
  uVar13 = FUN_000bfca0();
  DAT_4001d9a8 = (uVar13 & 1) << 0x1e | DAT_4001d9a8 & 0xbfffffff;
  uVar13 = FUN_000bfcc0();
  DAT_4001d9a8 = (uVar13 & 1) << 0x1d | DAT_4001d9a8 & 0xdfffffff;
  uVar13 = FUN_000bfce0();
  DAT_4001d9a8 = ((uint)LZCOUNT((uVar13 & 0xff) - 2) & 0x20) << 0x16 | DAT_4001d9a8 & 0xf7ffffff;
  DAT_4001d9ac = DAT_4001d9ac & 0xff7fffff;
  FUN_00045560(0x14);
  FUN_00045520(0x18);
  cVar18 = FUN_000c0c10();
  FUN_00045560(0x18);
  FUN_00045520(0x1f);
  uVar13 = FUN_000c2f20();
  DAT_4001d9ac = ((uVar13 & 0xff) - 3 | 3 - (uVar13 & 0xff)) >> 1 & 0x40000000 |
                 DAT_4001d9ac & 0xbfffffff;
  cVar19 = FUN_000c34d0();
  if ((cVar19 == '\x01') && (cVar18 == '\x01')) {
    DAT_4001d9ac = DAT_4001d9ac | 0x1000000;
  }
  else {
    cVar19 = FUN_000c34d0();
    if ((cVar19 == '\0') && (cVar18 == '\0')) {
      DAT_4001d9ac = DAT_4001d9ac & 0xfeffffff;
    }
  }
  FUN_00045560(0x1f);
  DAT_4001d9ac = DAT_4001d9ac & 0x83ffffff;
  if (*(char *)(DAT_40037a40 + 0x5df) == '\0') {
    DAT_4001d9a0 = (DAT_4001d9a0 & 0x8000000) << 1 | DAT_4001d9a0 & 0xcfffffff;
  }
  else {
    DAT_4001d9a0 = (DAT_4001d951 & 1) << 0x1c | DAT_4001d9a0 & 0xcfffffff;
  }
  FUN_00045520(0x19);
  fVar14 = (float)FUN_000c0d50();
  fVar14 = fVar14 * 1000.0;
  if (fVar14 < 0.0) {
    uVar10 = (ulonglong)-fVar14;
    if (0x80000000 < uVar10) {
      uVar10 = 0;
    }
    sVar22 = -(short)uVar10;
  }
  else {
    uVar10 = (ulonglong)fVar14;
    if (0x7fffffff < uVar10) {
      uVar10 = 0x7fffffff;
    }
    sVar22 = (short)uVar10;
  }
  _DAT_4001d998 = CONCAT22(DAT_4001d998,sVar22);
  fVar14 = (float)FUN_000c0de0();
  fVar14 = fVar14 * 100.0;
  if (fVar14 < 0.0) {
    uVar10 = (ulonglong)-fVar14;
    if (0x80000000 < uVar10) {
      uVar10 = 0;
    }
    sVar22 = -(short)uVar10;
  }
  else {
    uVar10 = (ulonglong)fVar14;
    if (0x7fffffff < uVar10) {
      uVar10 = 0x7fffffff;
    }
    sVar22 = (short)uVar10;
  }
  _DAT_4001d998 = CONCAT22(sVar22,DAT_4001d99a);
  FUN_00045560(0x19);
  FUN_00045520(0x10);
  DAT_4001da94 = FUN_000be070();
  DAT_4001da95 = FUN_000be0b0();
  DAT_4001da96 = FUN_000be090();
  FUN_00045560(0x10);
  FUN_00045520(9);
  DAT_4001da97 = FUN_000bd730();
  FUN_00045560(9);
  FUN_0012f830(param_1);
  FUN_0012ed00(param_1,&DAT_4001d998,&DAT_4001d9ec,&DAT_4001d8c0,&DAT_4001da38,&DAT_4001da34,
               &DAT_4001d9b8,&DAT_4001d9b8);
  FUN_001397c0(param_1,&DAT_4001da38,&DAT_4001d8c0,&DAT_4001da34,&DAT_4001d998,&DAT_4001dc80,
               &DAT_4001d978,local_70);
  local_74 = &DAT_4001dab8;
  FUN_0012fbc0(param_1,&DAT_4001d9b8,&DAT_4001da38,&DAT_4001d978,&DAT_4001db88,&DAT_4001da60,
               &DAT_4001dc40,&DAT_4001dc80);
  FUN_001303a0(param_1,&DAT_4001d9b8,&DAT_4001d978,&DAT_4001da94,&DAT_4001db88,&DAT_4001da60,
               &DAT_4001dc40);
  FUN_00132380();
  FUN_00132230();
  DAT_4001dc40 = DAT_4001da60;
  DAT_4001dc44 = DAT_4001da64;
  DAT_4001dc48 = DAT_4001da68;
  DAT_4001dc4c = DAT_4001da6c;
  DAT_4001dc50 = _DAT_4001da70;
  DAT_4001dc54 = DAT_4001da74;
  DAT_4001dc58 = DAT_4001da78;
  DAT_4001dc5c = _DAT_4001da7c;
  DAT_4001dc60 = _DAT_4001da80;
  DAT_4001dc64 = DAT_4001da84;
  DAT_4001dc68 = _DAT_4001da88;
  DAT_4001dc6c = _DAT_4001da8c;
  DAT_4001dc70 = DAT_4001da90;
  DAT_4001da40 = _DAT_4001d998;
  DAT_4001da44 = _DAT_4001d99c;
  DAT_4001da48 = DAT_4001d9a0;
  DAT_4001da4c = DAT_4001d9a4;
  DAT_4001da50 = DAT_4001d9a8;
  DAT_4001da54 = DAT_4001d9ac;
  DAT_4001da58 = DAT_4001d9b0;
  DAT_4001da5c = _DAT_4001d9b4;
  FUN_00045520(0x21);
  DAT_4001dc90 = 0;
  fVar14 = (float)FUN_000c5480();
  if (fVar14 < 0.0) {
    uVar10 = (ulonglong)-fVar14;
    if (0x80000000 < uVar10) {
      uVar10 = 0;
    }
    DAT_4001dc92 = -(short)uVar10;
  }
  else {
    uVar10 = (ulonglong)fVar14;
    if (0x7fffffff < uVar10) {
      uVar10 = 0x7fffffff;
    }
    DAT_4001dc92 = (short)uVar10;
  }
  fVar14 = (float)FUN_000c5c10();
  if (fVar14 < 0.0) {
    uVar10 = (ulonglong)-fVar14;
    if (0x80000000 < uVar10) {
      uVar10 = 0;
    }
    DAT_4001dc94 = -(short)uVar10;
  }
  else {
    uVar10 = (ulonglong)fVar14;
    if (0x7fffffff < uVar10) {
      uVar10 = 0x7fffffff;
    }
    DAT_4001dc94 = (short)uVar10;
  }
  fVar14 = (float)FUN_000c5430();
  if (fVar14 < 0.0) {
    uVar10 = (ulonglong)-fVar14;
    if (0x80000000 < uVar10) {
      uVar10 = 0;
    }
    DAT_4001dc96 = -(short)uVar10;
  }
  else {
    uVar10 = (ulonglong)fVar14;
    if (0x7fffffff < uVar10) {
      uVar10 = 0x7fffffff;
    }
    DAT_4001dc96 = (short)uVar10;
  }
  fVar14 = (float)FUN_000c5430();
  if (fVar14 < 0.0) {
    uVar10 = (ulonglong)-fVar14;
    if (0x80000000 < uVar10) {
      uVar10 = 0;
    }
    DAT_4001dc98 = -(short)uVar10;
  }
  else {
    uVar10 = (ulonglong)fVar14;
    if (0x7fffffff < uVar10) {
      uVar10 = 0x7fffffff;
    }
    DAT_4001dc98 = (short)uVar10;
  }
  fVar14 = (float)FUN_000c5b90();
  fVar14 = (fVar14 / 60.0) * 100.0;
  if (fVar14 < 0.0) {
    uVar10 = (ulonglong)-fVar14;
    if (0x80000000 < uVar10) {
      uVar10 = 0;
    }
    DAT_4001dc9a = -(short)uVar10;
  }
  else {
    uVar10 = (ulonglong)fVar14;
    if (0x7fffffff < uVar10) {
      uVar10 = 0x7fffffff;
    }
    DAT_4001dc9a = (short)uVar10;
  }
  FUN_00045560(0x21);
  DAT_4001dc9c = FUN_00134390();
  DAT_4001dc9e = DAT_4001d8c6;
  if (DAT_4001d9b4 == '\x01') {
    if (DAT_4001d8c6 == '\x01') {
      DAT_4001dc9f = '\x02';
    }
    else if (DAT_4001d8c6 == '\x02') {
      DAT_4001dc9f = '\x03';
    }
    else if (DAT_4001d8c6 == '\x03') {
      DAT_4001dc9f = '\x04';
    }
    else if (DAT_4001d8c6 == '\x04') {
      DAT_4001dc9f = '\x05';
    }
    else if (DAT_4001d8c6 == '\x05') {
      DAT_4001dc9f = '\x06';
    }
    else if (DAT_4001d8c6 == '\x06') {
      DAT_4001dc9f = '\a';
    }
    else if (DAT_4001d8c6 == '\a') {
      DAT_4001dc9f = '\a';
    }
    else {
      DAT_4001dc9f = DAT_4001d8c6;
    }
  }
  else if (DAT_4001d9b4 == '\x02') {
    if (DAT_4001d8c6 == '\x01') {
      DAT_4001dc9f = '\x01';
    }
    else if (DAT_4001d8c6 == '\x02') {
      DAT_4001dc9f = '\x01';
    }
    else if (DAT_4001d8c6 == '\x03') {
      DAT_4001dc9e = '\x02';
    }
    else if (DAT_4001d8c6 == '\x04') {
      DAT_4001dc9e = '\x03';
    }
    else if (DAT_4001d8c6 == '\x05') {
      DAT_4001dc9f = '\x04';
    }
    else if (DAT_4001d8c6 == '\x06') {
      DAT_4001dc9f = '\x05';
    }
    else if (DAT_4001d8c6 == '\a') {
      DAT_4001dc9f = '\x06';
    }
    else {
      DAT_4001dc9f = DAT_4001d8c6;
    }
  }
  else {
    DAT_4001dc9f = DAT_4001d8c6;
  }
  if (*(char *)(DAT_40037a40 + 0x5df) == '\0') {
    DAT_4001dca0 = DAT_4001d9a0 & 0x8000000 |
                   (DAT_4001d9a0 & 0x8000000) << 1 | DAT_4001dca0 & 0x7ffffff;
  }
  else {
    DAT_4001dca0 = DAT_4001d9a0 & 0x10000000 | DAT_4001dca0 & 0xfffffff;
  }
  DAT_4001dc8c = DAT_4001dc8c | 0x400000;
  FUN_00139d80(param_1,&DAT_4001dc90,&DAT_4001d998,&DAT_4001dc80,&DAT_4001dae4,&DAT_4001e148);
  FUN_00045520(0x12);
  FUN_000c2780((undefined1)DAT_4001da68);
  FUN_000c2720(1);
  FUN_000c2740((uint)LZCOUNT(*(byte *)(DAT_40037a40 + 0x623) - 1) >> 5);
  FUN_000c25c0(DAT_4001da74 >> 0x1f);
  FUN_000c2760(DAT_4001da74 >> 0x1f);
  FUN_000c2500(DAT_4001da74 >> 0x1e & 1);
  FUN_000c2520(DAT_4001da74 >> 0x1d & 1);
  FUN_000c2540(DAT_4001da74 >> 0x1c & 1);
  FUN_000c2560(DAT_4001da74 >> 0x1b & 1);
  FUN_000c2580(DAT_4001da74 >> 0x1a & 1);
  FUN_000c25a0(DAT_4001da74 >> 0x19 & 1);
  FUN_000c25e0(DAT_4001da74 >> 0x18 & 1);
  FUN_000c2600(DAT_4001da74 >> 0x16 & 1);
  FUN_000c2800(DAT_4001da74 >> 0x17 & 1);
  FUN_000c27a0((undefined1)DAT_4001da6c);
  FUN_000c27c0(DAT_4001da70);
  if ((int)DAT_4001d8d0 < 0) {
    if (*(char *)(DAT_40037a40 + 0x634) == '\x01') {
      uVar10 = (ulonglong)(DAT_4001da64 * 100.0);
      if (0x7fffffff < uVar10) {
        uVar10 = 0x7fffffff;
      }
      uVar10 = FUN_0012e3e0(DAT_40037a40 + 0x636,6,(short)uVar10);
      FUN_000c2650(uVar10 & 0xffffffff00000000 |
                   (ulonglong)(uint)(DAT_4001da64 * (10000.0 / (float)((uint)uVar10 & 0xffff))));
    }
    else {
      FUN_000c2650(DAT_4001da64);
    }
  }
  else if (*(char *)(DAT_40037a40 + 0x634) == '\x01') {
    if (DAT_4001da64 < 0.0) {
      uVar10 = (ulonglong)-DAT_4001da64;
      if (0x80000000 < uVar10) {
        uVar10 = 0x80000000;
      }
      uVar10 = -uVar10;
    }
    else {
      uVar10 = (ulonglong)DAT_4001da64;
      if (0x7fffffff < uVar10) {
        uVar10 = 0x7fffffff;
      }
    }
    lVar23 = (uVar10 & 0xffffffff) * SUB168(SEXT216(0x649),0);
    iVar15 = (int)lVar23;
    sVar22 = (short)((ulonglong)lVar23 >> 0x10) >> 0xf;
    uVar16 = FUN_0012e3e0(DAT_40037a40 + 0x636,6,
                          ((short)(iVar15 / 10) + sVar22) -
                          ((short)((short)(iVar15 / 0xa0000) + sVar22) >> 0xf));
    FUN_000c2650((10000.0 / (float)uVar16) * DAT_4001da64 * *(float *)(DAT_40037a40 + 0x8e8));
  }
  else {
    FUN_000c2650(DAT_4001da64 * *(float *)(DAT_40037a40 + 0x8e8));
  }
  FUN_000c2680(DAT_4001da68._2_1_);
  FUN_000c2930(DAT_4001d9c9);
  FUN_000c2630(DAT_4001da72);
  FUN_000c2610(DAT_4001da71);
  FUN_000c27e0(DAT_4001da7c);
  FUN_000c2840(DAT_4001d96d);
  FUN_000c2820(DAT_4001d96e);
  if (*(char *)(DAT_40037a40 + 0x626) == '\x01') {
    FUN_000c2600(0);
    FUN_000c26a0(0);
    FUN_000c26b0(0);
    FUN_000c26d0(0);
    FUN_000c2700(0);
    FUN_000c2810(1);
  }
  else {
    uVar17 = FUN_0012e3e0(DAT_40037a40 + 0x5f6,8,DAT_4001d998);
    uVar17 = FUN_0012e5a0(DAT_4001dae6,uVar17,2000);
    uVar10 = FUN_0012e630(uVar17,DAT_4001dae6,-(longlong)*(short *)(DAT_40037a40 + 0x620),
                          (longlong)*(short *)(DAT_40037a40 + 0x620),param_1);
    DAT_4001dae6 = (short)uVar10;
    if (((longlong)DAT_4001dae6 & 0x80000000U) == 0) {
      fVar14 = (float)(int)DAT_4001dae6;
    }
    else {
      fVar14 = -(float)-(int)DAT_4001dae6;
    }
    FUN_000c26a0(uVar10 & 0xffffffff00000000 | (ulonglong)(uint)(fVar14 / 1000.0));
    bVar21 = DAT_4001dc30 == 0;
    DAT_4001dc30 = DAT_4001dc30 + -1;
    uVar11 = 0;
    if (bVar21) {
      DAT_4001dc30 = 0;
    }
    if ((DAT_4001daee == '\x02') || (DAT_4001dc30 != 0)) {
      uVar11 = 1;
    }
    uVar10 = FUN_000c26b0(uVar11);
    if (((longlong)DAT_4001dae8 & 0x80000000U) == 0) {
      fVar14 = (float)(int)DAT_4001dae8;
    }
    else {
      fVar14 = -(float)-(int)DAT_4001dae8;
    }
    FUN_000c26d0(uVar10 & 0xffffffff00000000 | (ulonglong)(uint)fVar14);
    uVar11 = 0;
    bVar21 = true;
    if ((DAT_4001daee != '\x02') && (bVar21 = false, DAT_4001daee == '\x01')) {
      bVar21 = true;
    }
    if ((bVar21) && (uVar11 = 1, 2 < (byte)(DAT_4001d9c6 - 2U))) {
      uVar11 = 0;
    }
    FUN_000c2700(uVar11);
    FUN_000c2810(DAT_4001daf2);
  }
  FUN_00045560(0x12);
  return;
}

