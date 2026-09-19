
void FUN_00133960(int param_1)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  bool bVar5;
  bool bVar6;
  bool bVar7;
  undefined4 uVar8;
  char *pcVar9;
  int iVar10;
  int iVar11;
  int iVar12;
  char cVar13;
  char cVar14;
  undefined1 uVar15;
  int iVar16;
  int iVar17;
  int iVar18;
  uint uVar19;
  uint uVar20;
  uint uVar21;
  uint uVar22;
  uint uVar23;
  uint uVar24;
  int iVar25;
  undefined8 uVar26;
  longlong lVar27;
  
  uVar26 = 0;
  DAT_4001d8b4 = '\0';
  FUN_00045520(0x19);
  DAT_4001d970 = FUN_000c0d10();
  FUN_00045560(0x19);
  FUN_00045520(0x21);
  DAT_4001d974 = FUN_000c5f80();
  FUN_00045560(0x21);
  FUN_0012df00((uint)LZCOUNT(DAT_4001d94b - 1) >> 5,
               (short)((int)(uint)*(ushort *)(DAT_40037a40 + 0x5c4) / param_1),&DAT_4001d8f8,
               DAT_4001d9e4 >> 0x1a & 1);
  FUN_0012df00((uint)LZCOUNT(DAT_4001d94a - 1) >> 5,
               (short)((int)(uint)*(ushort *)(DAT_40037a40 + 0x5c2) / param_1),&DAT_4001d914,
               DAT_4001d9e4 >> 0x1a & 1);
  if ((DAT_4001d94c == '\x01') && (DAT_4001d95c == '\x01')) {
    uVar26 = 1;
  }
  FUN_0012df00(uVar26,(short)((int)(uint)*(ushort *)(DAT_40037a40 + 0x5ce) / param_1),&DAT_4001d8fe,
               DAT_4001d9e4 >> 0x1a & 1);
  uVar8 = 0;
  bVar5 = true;
  if ((DAT_4001d938 <= *(short *)(DAT_40037a40 + 0x5ca)) &&
     (bVar5 = false, DAT_4001d938 < *(short *)(DAT_40037a40 + 0x5cc))) {
    bVar5 = true;
  }
  if ((bVar5) && (uVar8 = 0, DAT_4001d93f == '\0')) {
    uVar8 = 1;
  }
  FUN_0012df00(uVar8,(short)((int)(uint)*(ushort *)(DAT_40037a40 + 0x5c8) / param_1),&DAT_4001d8fc,
               DAT_4001d9e4 >> 0x1a & 1);
  FUN_0012df00((uint)LZCOUNT(DAT_4001d963 - 2) >> 5,
               (short)((int)(uint)*(ushort *)(DAT_40037a40 + 0x5c6) / param_1),&DAT_4001d8fa,
               DAT_4001d9e4 >> 0x1a & 1);
  DAT_4001d8e2 = 0;
  bVar7 = false;
  bVar5 = false;
  if (DAT_4001d934 < *(short *)(DAT_40037a40 + 0x5e4)) {
    bVar6 = true;
    bVar5 = true;
    if ((1 < DAT_4001d959) && (bVar5 = false, DAT_4001d95a == '\x01')) {
      bVar5 = true;
    }
    if ((!bVar5) && (bVar6 = false, DAT_4001d95a == '\0')) {
      bVar6 = true;
    }
    bVar5 = true;
    if (!bVar6) {
      bVar5 = false;
    }
  }
  if (bVar5) {
    bVar5 = true;
    if ((DAT_4001d95b != '\x02') && (bVar5 = false, DAT_4001d95b == '\0')) {
      bVar5 = true;
    }
    bVar7 = true;
    if (!bVar5) {
      bVar7 = false;
    }
  }
  if ((bVar7) && (DAT_4001d8e2 = 0, *(char *)(DAT_40037a40 + 0x5de) == '\x01')) {
    DAT_4001d8e2 = 1;
  }
  FUN_0012df00((uint)LZCOUNT(DAT_4001d8e2 - 1) >> 5,
               (short)((int)(uint)*(ushort *)(DAT_40037a40 + 0x5c0) / param_1),&DAT_4001d912,
               DAT_4001d9e4 >> 0x1a & 1);
  uVar26 = 0;
  if ((DAT_4001d951 == '\x01') && (*(char *)(DAT_40037a40 + 0x5df) == '\x01')) {
    uVar26 = 1;
  }
  FUN_0012df00(uVar26,(short)((int)(uint)*(ushort *)(DAT_40037a40 + 0x686) / param_1),&DAT_4001d91e,
               DAT_4001d9e4 >> 0x1a & 1);
  uVar26 = 0;
  if ((DAT_4001d950 == '\x01') && (*(char *)(DAT_40037a40 + 0x5df) == '\x01')) {
    uVar26 = 1;
  }
  FUN_0012df00(uVar26,(short)((int)(uint)*(ushort *)(DAT_40037a40 + 0x684) / param_1),&DAT_4001d920,
               DAT_4001d9e4 >> 0x1a & 1);
  uVar1 = ((uint)LZCOUNT(DAT_4001d949 - 3) & 0x20) << 0x18;
  uVar2 = ((uint)LZCOUNT((uint)DAT_4001d912) & 0x20) << 0x17;
  uVar21 = ((uint)LZCOUNT(DAT_4001d956 - 1) & 0x20) << 0xd;
  uVar19 = ((uint)LZCOUNT(DAT_4001d957 - 1) & 0x20) << 0xc;
  uVar20 = uVar19 | uVar21 | uVar2 | uVar1 | DAT_4001daf8 & 0xcff9ffff;
  if (*(char *)(DAT_40037a40 + 0x5df) == '\0') {
    uVar20 = ((uint)LZCOUNT((uint)DAT_4001d94f) & 0x20) << 8 |
             uVar19 | uVar21 | uVar2 | uVar1 | DAT_4001daf8 & 0xcff9dfff;
  }
  DAT_4001daf8 = uVar20;
  if ((*(char *)(DAT_40037a40 + 0x5df) == '\x01') &&
     ((((DAT_4001d91e == 0 && (*(char *)(DAT_40037a40 + 0x688) == '\x01')) ||
       ((DAT_4001d951 == '\x01' && (*(char *)(DAT_40037a40 + 0x688) == '\0')))) ||
      (((((DAT_4001d950 == '\0' || (DAT_4001d920 == 0)) ||
         ((DAT_4001d950 == '\r' && (DAT_4001d951 == '\0')))) || ((byte)(DAT_4001d950 - 0xeU) < 2))
       && (DAT_4001d926 == 0)))))) {
    DAT_4001daf8 = DAT_4001daf8 | 0x1000;
  }
  else {
    DAT_4001daf8 = DAT_4001daf8 & 0xffffefff;
  }
  uVar2 = ((uint)LZCOUNT((uint)DAT_4001d914) & 0x20) << 4;
  uVar21 = ((uint)LZCOUNT((uint)DAT_4001d8f8) & 0x20) << 3;
  uVar19 = ((uint)LZCOUNT((uint)DAT_4001d8fe) & 0x20) << 2;
  uVar20 = ((uint)LZCOUNT(DAT_4001d940 - 1) & 0x20) << 1;
  uVar22 = (uint)LZCOUNT(DAT_4001d93c - 1) & 0x20;
  uVar23 = (uint)LZCOUNT(DAT_4001d932 - 1) >> 1 & 0x10;
  uVar24 = (uint)LZCOUNT((uint)DAT_4001d953) >> 2 & 8;
  uVar3 = (uint)LZCOUNT((uint)DAT_4001d952) >> 3 & 4;
  uVar4 = (uint)LZCOUNT(DAT_4001d936 - 1) >> 4 & 2;
  uVar1 = (uint)LZCOUNT(DAT_4001d95d - 1) >> 5;
  iVar25 = 0;
  if ((DAT_4001d8fc == 0) && (iVar25 = 0, *(short *)(DAT_40037a40 + 0x5ca) < DAT_4001d938)) {
    iVar25 = 1;
  }
  iVar10 = 0;
  if ((DAT_4001d8fc == 0) && (DAT_4001d938 < *(short *)(DAT_40037a40 + 0x5cc))) {
    iVar10 = 1;
  }
  iVar11 = 0;
  if ((DAT_4001d929 == '\x01') && (DAT_4001d92a == '\x01')) {
    iVar11 = 1;
  }
  iVar16 = 0;
  bVar5 = false;
  if ((*(char *)(DAT_40037a40 + 0x5de) == '\x01') &&
     (bVar5 = false, DAT_4001d934 < *(short *)(DAT_40037a40 + 0x5e4))) {
    bVar5 = true;
  }
  if ((bVar5) && (iVar16 = 0, DAT_4001d96b == '\x01')) {
    iVar16 = 1;
  }
  iVar12 = 0;
  if ((*(char *)(DAT_40037a40 + 0x5de) == '\x01') && (DAT_4001d971 == '\0')) {
    iVar12 = 1;
  }
  pcVar9 = (char *)&DAT_4001daf8;
  lVar27 = 2;
  do {
    cVar14 = '\x01';
    if (*pcVar9 == '\0') {
      cVar14 = DAT_4001d8b4;
    }
    cVar13 = '\x01';
    if (pcVar9[1] == '\0') {
      cVar13 = cVar14;
    }
    cVar14 = '\x01';
    if (pcVar9[2] == '\0') {
      cVar14 = cVar13;
    }
    cVar13 = '\x01';
    if (pcVar9[3] == '\0') {
      cVar13 = cVar14;
    }
    cVar14 = '\x01';
    if (pcVar9[4] == '\0') {
      cVar14 = cVar13;
    }
    DAT_4001d8b4 = '\x01';
    if (pcVar9[5] == '\0') {
      DAT_4001d8b4 = cVar14;
    }
    pcVar9 = pcVar9 + 6;
    lVar27 = lVar27 + -1;
  } while (lVar27 != 0);
  if (DAT_4001d8b4 == '\0') {
    DAT_4001d8dc = '\0';
  }
  if (((DAT_4001d8b4 == '\x01') && (DAT_4001d8dc == '\0')) || (DAT_4001d922 != 0)) {
    if ((DAT_4001daee == '\x02') && (DAT_4001d990 == '\x02')) {
      if ((DAT_4001d922 == 0) && (DAT_4001d8b4 == '\x01')) {
        DAT_4001d922 = (short)((int)(uint)*(ushort *)(DAT_40037a40 + 0x5d0) / param_1);
        DAT_4001d8e5 = 0;
      }
      else {
        DAT_4001d922 = DAT_4001d922 + -1;
        DAT_4001d8e5 = 1;
        if (DAT_4001d922 == 0) {
          DAT_4001d8dc = '\x01';
        }
      }
    }
    else {
      DAT_4001d8dc = '\x01';
      DAT_4001d922 = 0;
      DAT_4001d8e5 = 0;
    }
  }
  else {
    DAT_4001d8e5 = 0;
    DAT_4001d8dc = DAT_4001d8b4;
  }
  iVar17 = 0;
  if (((*(char *)(DAT_40037a40 + 0x5de) == '\0') &&
      (DAT_4001d934 < *(short *)(DAT_40037a40 + 0x5e0))) && (DAT_4001daee != '\0')) {
    iVar17 = 1;
  }
  if (DAT_4001d931 == '\x01') {
    iVar18 = 0;
    if ((*(short *)(DAT_40037a40 + 0x674) < DAT_4001d934) && (DAT_4001d936 == 0)) {
      iVar18 = 1;
    }
    DAT_4001daf8 = iVar18 << 0x1e |
                   iVar17 << 0x1f |
                   uVar1 | uVar4 | uVar3 | uVar24 | uVar23 | uVar22 | uVar20 | uVar19 | uVar21 | 
                                                  uVar2 | DAT_4001daf8 & 0x3ffffc00;
  }
  else {
    iVar18 = 0;
    if ((*(short *)(DAT_40037a40 + 0x5e2) < DAT_4001d934) && (DAT_4001d936 == 0)) {
      iVar18 = 1;
    }
    DAT_4001daf8 = iVar18 << 0x1e |
                   iVar17 << 0x1f |
                   uVar1 | uVar4 | uVar3 | uVar24 | uVar23 | uVar22 | uVar20 | uVar19 | uVar21 | 
                                                  uVar2 | DAT_4001daf8 & 0x3ffffc00;
  }
  uVar19 = (uint)LZCOUNT(DAT_4001d94f - 0xe);
  uVar1 = (uVar19 & 0x20) << 10;
  uVar20 = (uint)LZCOUNT(DAT_4001d94f - 0xd);
  uVar2 = (uVar20 & 0x20) << 9;
  uVar21 = uVar1 | DAT_4001daf8 & 0xffff3fff;
  if (((((int)uVar21 < 0) || ((DAT_4001daf8 >> 0x1e & 1) != 0)) || (uVar19 >> 5 != 0)) ||
     (uVar20 >> 5 != 0)) {
    bVar5 = true;
    DAT_4001d8b3 = 1;
  }
  else {
    bVar5 = false;
    DAT_4001d8b3 = 0;
  }
  uVar21 = uVar2 | uVar21;
  if (*(char *)(DAT_40037a40 + 0x5df) == '\0') {
    uVar21 = ((uint)LZCOUNT(DAT_4001d94f - 0xf) & 0x20) << 0xb |
             uVar2 | uVar1 | DAT_4001daf8 & 0xfffe3fff;
  }
  DAT_4001daf8 = uVar21;
  uVar2 = DAT_4001daf8;
  uVar21 = (uint)LZCOUNT(DAT_4001d93d - 1);
  uVar19 = (uint)LZCOUNT(DAT_4001d93e - 1);
  DAT_4001daf8 = (uVar19 & 0x20) << 5 | (uVar21 & 0x20) << 6 | DAT_4001daf8 & 0xfffff3ff;
  uVar20 = (uint)LZCOUNT(DAT_4001d95e - 1);
  uVar22 = (uint)LZCOUNT(DAT_4001d95e - 3);
  uVar23 = (uint)LZCOUNT(DAT_4001d96f - 2);
  uVar24 = (uint)LZCOUNT(DAT_4001d974 - 1);
  uVar1 = (uVar23 & 0x20) << 2 |
          ((uint)LZCOUNT((uint)DAT_4001d96f) & 0x20) << 3 |
          (uVar22 & 0x20) << 0x18 |
          (uVar20 & 0x20) << 0x19 |
          ((uint)LZCOUNT((uint)DAT_4001d95e) & 0x20) << 0x1a |
          (uint)LZCOUNT(DAT_4001d973 - 1) >> 1 & 0x10 |
          (uint)LZCOUNT((uint)DAT_4001d96a) & 0x20 |
          iVar12 << 6 |
          ((uint)LZCOUNT(DAT_4001d966 - 2) & 0x20) << 4 |
          ((uint)LZCOUNT(DAT_4001d964 - 1) & 0x20) << 5 |
          ((uint)LZCOUNT((uint)DAT_4001d965) & 0x20) << 6 |
          iVar16 << 0xc |
          ((uint)LZCOUNT((uint)DAT_4001d8fa) & 0x20) << 8 |
          ((uint)LZCOUNT(DAT_4001d963 - 3) & 0x20) << 9 |
          ((uint)LZCOUNT(DAT_4001d970 - 3) & 0x20) << 0xb |
          ((uint)LZCOUNT(DAT_4001d94e - 2) & 0x20) << 0xe |
          ((uint)LZCOUNT(DAT_4001d94d - 2) & 0x20) << 0xf |
          ((uint)LZCOUNT((uint)DAT_4001d972) & 0x20) << 0x10 |
          ((uint)LZCOUNT(DAT_4001d972 - 2) & 0x20) << 0x11 |
          ((uint)LZCOUNT((uint)DAT_4001d969) & 0x20) << 0x12 |
          ((uint)LZCOUNT((uint)DAT_4001d968) & 0x20) << 0x13 |
          iVar11 << 0x19 | iVar10 << 0x1a | iVar25 << 0x1b | DAT_4001dafc & 0x10060007;
  DAT_4001dafc = uVar24 >> 2 & 8 | uVar1;
  if ((((((uVar2 >> 0x10 & 1) == 0) && (uVar21 >> 5 == 0)) &&
       ((uVar19 >> 5 == 0 && ((-1 < (int)uVar1 && (uVar20 >> 5 == 0)))))) && (uVar22 >> 5 == 0)) &&
     ((((uint)LZCOUNT((uint)DAT_4001d96f) >> 5 == 0 && (uVar23 >> 5 == 0)) && (uVar24 >> 5 == 0))))
  {
    bVar7 = false;
    DAT_4001d8b2 = 0;
  }
  else {
    bVar7 = true;
    DAT_4001d8b2 = 1;
    if ((DAT_4001d8b4 == '\0') && (!bVar5)) {
      DAT_4001d8e5 = 1;
    }
  }
  uVar15 = 0;
  if (((DAT_4001d8dc != '\0') || (bVar5)) || (bVar7)) {
    uVar15 = 1;
  }
  DAT_4001d8dc = uVar15;
  return;
}

