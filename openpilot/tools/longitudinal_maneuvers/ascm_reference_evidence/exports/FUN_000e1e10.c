
void FUN_000e1e10(undefined8 param_1,char param_2,char param_3,char param_4,char param_5,
                 float param_6,float param_7,float param_8,float param_9,undefined4 param_10,
                 char param_11,float param_12,float param_13,char param_14,float param_15,
                 float param_16,float param_17,float param_18,undefined4 param_19,float *param_20,
                 float *param_21,float *param_22)

{
  char cVar1;
  bool bVar2;
  bool bVar3;
  int iVar4;
  undefined1 uVar5;
  char cVar12;
  float fVar6;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float *pfVar11;
  float fVar13;
  float fVar14;
  float fVar15;
  float fVar16;
  ulonglong unaff_r15;
  ulonglong uVar17;
  float fVar18;
  ulonglong uVar19;
  float *pfVar20;
  float fVar21;
  byte *pbVar22;
  float fVar23;
  byte *pbVar24;
  int iVar25;
  short sVar26;
  byte bVar27;
  longlong lVar28;
  byte local_114 [4];
  byte local_110 [4];
  float local_10c;
  float local_108;
  float local_104;
  float local_100 [4];
  float local_f0 [4];
  float local_e0 [4];
  float local_d0 [4];
  float local_c0;
  float local_bc;
  float local_b8;
  float local_b4;
  byte local_b0;
  char local_af;
  int local_ac;
  int local_a8;
  int local_a4;
  float local_a0;
  float local_9c;
  float local_98;
  float local_94;
  
  local_d0[0] = param_6;
  local_d0[2] = param_7;
  cVar12 = FUN_00140694();
  if (*(char *)(param_21 + 0x26) == '\0') {
    local_a0 = param_21[0x11];
    local_98 = param_21[0x13];
    local_94 = param_21[0x14];
    local_9c = param_21[0x12];
  }
  else {
    local_94 = param_9;
    local_a0 = local_d0[0];
    local_9c = param_8;
    local_98 = local_d0[2];
  }
  if (*(char *)(param_21 + 0x26) == '\0') {
    fVar16 = *param_22;
    if (fVar16 <= *(float *)(DAT_40037a30 + 0x810)) {
      fVar16 = *(float *)(DAT_40037a30 + 0x810);
    }
    fVar8 = *param_22 * (1.0 / fVar16);
    fVar7 = fVar8 * fVar8;
    fVar16 = param_21[0x15];
    local_d0[0] = local_a0 * 2.0 +
                  ((fVar8 * (fVar16 - local_a0) * 2.0 + fVar7 * (local_d0[0] - fVar16)) - fVar16);
    fVar16 = param_21[0x16];
    unaff_r15 = 0;
    fVar6 = param_21[0x17];
    local_d0[2] = local_98 * 2.0 +
                  ((fVar8 * (fVar6 - local_98) * 2.0 + fVar7 * (local_d0[2] - fVar6)) - fVar6);
    fVar6 = param_21[0x18];
    local_d0[3] = local_94 * 2.0 +
                  ((fVar8 * (fVar6 - local_94) * 2.0 + fVar7 * (param_9 - fVar6)) - fVar6);
    local_d0[1] = local_9c * 2.0 +
                  ((fVar8 * (fVar16 - local_9c) * 2.0 + fVar7 * (param_8 - fVar16)) - fVar16);
  }
  else {
    local_d0[3] = param_9;
    local_d0[1] = param_8;
  }
  fVar16 = local_d0[1];
  if (local_d0[1] <= local_d0[0]) {
    fVar16 = local_d0[0];
  }
  fVar6 = local_d0[2];
  if (local_d0[2] <= fVar16) {
    fVar6 = fVar16;
  }
  bVar27 = 0;
  fVar16 = local_d0[3];
  if (local_d0[3] <= fVar6) {
    fVar16 = fVar6;
  }
  fVar16 = ((local_d0[0] + local_d0[1] + local_d0[2] + local_d0[3]) - fVar16) / 3.0;
  uVar17 = unaff_r15 & 0xffffffff00000000 | (ulonglong)(uint)fVar16;
  fVar6 = (float)FUN_0012b750(*(undefined4 *)(DAT_40037a30 + 0x83c));
  bVar27 = bVar27 & 0xfb;
  if (fVar6 < fVar16) {
    uVar19 = uVar17;
    if (*(float *)(DAT_40037a30 + 0x83c) < 0.0) {
      uVar19 = uVar17 ^ 0x80000000;
    }
  }
  else {
    uVar19 = (ulonglong)*(uint *)(DAT_40037a30 + 0x83c);
  }
  fVar6 = *(float *)(DAT_40037a30 + 0x83c);
  iVar25 = 0;
  pfVar11 = local_d0;
  pbVar24 = local_110;
  pbVar22 = local_114;
  pfVar20 = local_100;
  do {
    iVar4 = DAT_40037a30;
    fVar7 = (float)FUN_0012b750(*pfVar11);
    fVar8 = *(float *)(iVar4 + 0x83c);
    if (fVar7 < fVar8) {
      if (*pfVar11 < 0.0) {
        fVar8 = -fVar6;
      }
    }
    else {
      fVar8 = *pfVar11;
    }
    fVar8 = (float)uVar19 / fVar8;
    *pbVar24 = (byte)(((uint)(byte)(bVar27 & 0xb | (fVar8 < *(float *)(DAT_40037a60 + 0x430)) << 2)
                      << 0x1c) >> 0x1e) ^ 1;
    *pbVar22 = (byte)(((uint)(byte)(bVar27 & 0xb | (*(float *)(DAT_40037a60 + 0x434) < fVar8) << 2)
                      << 0x1c) >> 0x1e) ^ 1;
    *pfVar20 = fVar8;
    iVar25 = iVar25 + 1;
    bVar27 = (iVar25 < 4) << 3;
    pfVar11 = pfVar11 + 1;
    pbVar24 = pbVar24 + 1;
    pbVar22 = pbVar22 + 1;
    pfVar20 = pfVar20 + 1;
  } while (iVar25 < 4);
  cVar1 = *(char *)((int)param_21 + 0x99);
  if (cVar1 == '\0') {
    fVar6 = *(float *)(DAT_40037a30 + 0x828);
  }
  else {
    fVar6 = *(float *)(DAT_40037a30 + 0x824);
  }
  FUN_000e1d30(*(undefined1 *)((int)param_21 + 0x9a),*(undefined4 *)(DAT_40037a30 + 0x7a8),
               *(undefined4 *)(DAT_40037a30 + 0x7a4),param_19,*(undefined4 *)(DAT_40037a30 + 0x7a0),
               *(undefined4 *)(DAT_40037a30 + 0x7ac),*(undefined4 *)(DAT_40037a30 + 0x7b0),
               *(undefined4 *)(DAT_40037a30 + 0x7b4),&local_104,param_20 + 0x1a,param_21 + 0x2c);
  fVar8 = param_21[0xe];
  param_21[0xe] = local_104;
  if (cVar1 == '\0') {
    fVar7 = *(float *)(DAT_40037a30 + 0x7e8);
  }
  else {
    fVar7 = *(float *)(DAT_40037a30 + 0x7e4);
  }
  bVar27 = 0;
  if (cVar1 == '\0') {
    fVar18 = *(float *)(DAT_40037a30 + 0xa34);
  }
  else {
    fVar18 = *(float *)(DAT_40037a30 + 0xa30);
  }
  local_ac = 0;
  fVar8 = (float)FUN_0012b750((local_104 - fVar8) / *param_22);
  bVar27 = bVar27 & 0xfb;
  if (fVar8 < fVar7) {
    fVar8 = (float)FUN_0012b750(local_104);
    bVar27 = bVar27 & 0xfb;
    if ((fVar8 < fVar18) && (bVar27 = 0, cVar12 == '\0')) {
      local_ac = 1;
    }
  }
  fVar8 = *(float *)(DAT_40037a30 + 0x838);
  FUN_000e1d30(*(undefined1 *)((int)param_21 + 0x9b),*(undefined4 *)(DAT_40037a30 + 0x790),
               *(undefined4 *)(DAT_40037a30 + 0x78c),uVar17,*(undefined4 *)(DAT_40037a30 + 0x788),
               *(undefined4 *)(DAT_40037a30 + 0x794),*(undefined4 *)(DAT_40037a30 + 0x798),
               *(undefined4 *)(DAT_40037a30 + 0x79c),&local_108,param_20 + 0x1b,param_21 + 0x2e);
  fVar7 = param_21[0xf];
  param_21[0xf] = local_108;
  if (cVar1 == '\0') {
    fVar18 = *(float *)(DAT_40037a30 + 0x7d8);
  }
  else {
    fVar18 = *(float *)(DAT_40037a30 + 0x7d4);
  }
  local_a8 = 0;
  if ((((((byte)(bVar27 & 0xb | (fVar8 < fVar16) << 2) >> 2 != 0) &&
        (fVar8 = (float)FUN_0012b750((local_108 - fVar7) / *param_22), fVar8 < fVar18)) &&
       (param_2 == '\0')) && ((param_3 == '\0' && (param_4 == '\0')))) && (param_5 == '\0')) {
    local_a8 = 1;
  }
  fVar8 = param_15;
  fVar7 = param_16;
  fVar18 = param_18;
  fVar23 = param_17;
  if (*(char *)(param_21 + 0x27) == '\0') {
    fVar8 = param_21[0x1a];
    fVar7 = param_21[0x1b];
    fVar18 = param_21[0x19];
    fVar23 = param_21[0x1c];
  }
  if (*(char *)(param_21 + 0x27) == '\0') {
    fVar9 = *param_22;
    if (fVar9 <= *(float *)(DAT_40037a30 + 0x804)) {
      fVar9 = *(float *)(DAT_40037a30 + 0x804);
    }
    fVar21 = *param_22 * (1.0 / fVar9);
    fVar13 = fVar21 * fVar21;
    fVar9 = param_21[0x1d];
    local_e0[0] = fVar18 * 2.0 +
                  ((fVar21 * (fVar9 - fVar18) * 2.0 + fVar13 * (param_18 - fVar9)) - fVar9);
    fVar9 = param_21[0x1e];
    local_e0[1] = fVar8 * 2.0 +
                  ((fVar21 * (fVar9 - fVar8) * 2.0 + fVar13 * (param_15 - fVar9)) - fVar9);
    fVar9 = param_21[0x1f];
    local_e0[2] = fVar7 * 2.0 +
                  ((fVar21 * (fVar9 - fVar7) * 2.0 + fVar13 * (param_16 - fVar9)) - fVar9);
    fVar9 = param_21[0x20];
    local_e0[3] = fVar23 * 2.0 +
                  ((fVar21 * (fVar9 - fVar23) * 2.0 + fVar13 * (param_17 - fVar9)) - fVar9);
  }
  else {
    local_e0[0] = param_18;
    local_e0[1] = param_15;
    local_e0[2] = param_16;
    local_e0[3] = param_17;
  }
  iVar25 = 0;
  pfVar20 = local_e0;
  pfVar11 = local_f0;
  do {
    fVar9 = (float)FUN_0012b750(*pfVar20);
    *pfVar11 = fVar9;
    iVar25 = iVar25 + 1;
    pfVar20 = pfVar20 + 1;
    pfVar11 = pfVar11 + 1;
  } while (iVar25 < 4);
  if (local_f0[1] <= local_f0[0]) {
    local_f0[1] = local_f0[0];
  }
  if (local_f0[2] <= local_f0[1]) {
    local_f0[2] = local_f0[1];
  }
  fVar9 = local_f0[3];
  if (local_f0[3] <= local_f0[2]) {
    fVar9 = local_f0[2];
  }
  if (cVar1 == '\0') {
    fVar21 = *(float *)(DAT_40037a30 + 0x7e0);
  }
  else {
    fVar21 = *(float *)(DAT_40037a30 + 0x7dc);
  }
  local_b4 = param_15 - param_16;
  if (cVar1 == '\0') {
    fVar13 = *(float *)(DAT_40037a30 + 0x7f4);
  }
  else {
    fVar13 = *(float *)(DAT_40037a30 + 0x7f0);
  }
  fVar13 = fVar13 * fVar16;
  if (*(float *)(DAT_40037a30 + 0x840) <= fVar13) {
    fVar13 = *(float *)(DAT_40037a30 + 0x840);
  }
  local_b8 = param_8 - param_9;
  local_bc = param_15 - param_8;
  if (cVar1 == '\0') {
    fVar14 = *(float *)(DAT_40037a30 + 0x7fc);
  }
  else {
    fVar14 = *(float *)(DAT_40037a30 + 0x7f8);
  }
  fVar14 = fVar14 * fVar16;
  if (*(float *)(DAT_40037a30 + 0x844) <= fVar14) {
    fVar14 = *(float *)(DAT_40037a30 + 0x844);
  }
  local_c0 = param_16 - param_9;
  bVar27 = 0;
  if (cVar1 == '\0') {
    fVar15 = *(float *)(DAT_40037a30 + 0x818);
  }
  else {
    fVar15 = *(float *)(DAT_40037a30 + 0x814);
  }
  local_a4 = 0;
  fVar10 = (float)FUN_0012b750(param_10);
  bVar27 = bVar27 & 0xfb;
  if ((fVar10 < fVar15) && (bVar27 = 0, param_11 == '\0')) {
    local_a4 = 1;
  }
  local_b0 = (byte)(((uint)(byte)(bVar27 & 0xb | (param_12 < *(float *)(DAT_40037a30 + 2000)) << 2)
                    << 0x1c) >> 0x1e);
  if (cVar1 == '\0') {
    fVar15 = *(float *)(DAT_40037a30 + 0x7cc);
  }
  else {
    fVar15 = *(float *)(DAT_40037a30 + 0x7c8);
  }
  local_af = param_13 < fVar15;
  FUN_000e1d30(*(undefined1 *)((int)param_21 + 0x9d),*(undefined4 *)(DAT_40037a30 + 0x778),
               *(undefined4 *)(DAT_40037a30 + 0x774),param_13,*(undefined4 *)(DAT_40037a30 + 0x770),
               *(undefined4 *)(DAT_40037a30 + 0x77c),*(undefined4 *)(DAT_40037a30 + 0x780),
               *(undefined4 *)(DAT_40037a30 + 0x784),&local_10c,param_20 + 0x1c,param_21 + 0x30);
  fVar15 = param_21[0x10];
  param_21[0x10] = local_10c;
  fVar10 = *param_22;
  bVar2 = false;
  if (((((local_ac != 0) && (local_a8 != 0)) && (fVar9 < fVar21)) &&
      (((((fVar9 = (float)FUN_0012b750(local_b4), fVar9 < fVar13 ||
          (fVar9 = (float)FUN_0012b750(local_b8), fVar9 < fVar13)) &&
         ((fVar9 = (float)FUN_0012b750(local_bc), fVar9 < fVar14 ||
          (fVar9 = (float)FUN_0012b750(local_c0), fVar9 < fVar14)))) &&
        ((local_a4 != 0 && (local_b0 != 0)))) && (local_af != '\0')))) &&
     ((fVar9 = (float)FUN_0012b750((local_10c - fVar15) / fVar10),
      fVar9 < *(float *)(DAT_40037a30 + 0x7c4) && (param_14 == '\0')))) {
    bVar2 = true;
  }
  bVar3 = false;
  if ((bVar2) && (*(char *)((int)param_21 + 0xab) == '\0')) {
    bVar3 = true;
  }
  *(bool *)((int)param_21 + 0xab) = bVar2;
  if ((!bVar2) || (bVar3)) {
    param_21[0xd] = 0.0;
  }
  else {
    fVar9 = *param_22 + param_21[0xd];
    if (fVar6 <= fVar9) {
      fVar9 = fVar6;
    }
    param_21[0xd] = fVar9;
  }
  uVar5 = 0;
  if ((bVar2) && (fVar6 <= param_21[0xd])) {
    uVar5 = 1;
  }
  *(undefined1 *)(param_20 + 0x19) = uVar5;
  bVar2 = false;
  if (((((local_110[0] != 0) || (local_110[1] != '\0')) || (local_110[2] != '\0')) ||
      (((local_110[3] != '\0' || (local_114[0] != 0)) ||
       ((local_114[1] != '\0' || ((local_114[2] != '\0' || (local_114[3] != '\0')))))))) ||
     (*(char *)(param_20 + 0x19) == '\0')) {
    bVar2 = true;
  }
  bVar3 = false;
  if ((!bVar2) && (*(char *)(param_21 + 0x2b) != '\0')) {
    bVar3 = true;
  }
  *(bool *)(param_21 + 0x2b) = bVar2;
  if (bVar3) {
    param_21[0x21] = *(float *)(DAT_40037a30 + 0x820);
  }
  else {
    fVar6 = param_21[0x21] - *param_22;
    if (fVar6 < 0.0) {
      fVar6 = 0.0;
    }
    param_21[0x21] = fVar6;
  }
  if (*(char *)((int)param_21 + 0x9e) == '\0') {
    if ((!bVar2) && (param_21[0x21] <= 0.0)) {
      fVar6 = *param_22;
      if (fVar6 <= *(float *)(DAT_40037a30 + 0x808)) {
        fVar6 = *(float *)(DAT_40037a30 + 0x808);
      }
      pfVar11 = local_100;
      lVar28 = 4;
      pfVar20 = param_21;
      do {
        fVar9 = *(float *)(DAT_40037a60 + 0x430);
        if (*pfVar11 <= fVar9) {
          fVar9 = *pfVar11;
        }
        fVar21 = *(float *)(DAT_40037a60 + 0x434);
        if (fVar21 < fVar9) {
          fVar21 = fVar9;
        }
        pfVar20[0x22] = (1.0 / fVar6) * *param_22 * (fVar21 - pfVar20[0x22]) + pfVar20[0x22];
        pfVar11 = pfVar11 + 1;
        pfVar20 = pfVar20 + 1;
        lVar28 = lVar28 + -1;
      } while (lVar28 != 0);
    }
  }
  else {
    param_21[0x22] = 1.0;
    param_21[0x23] = 1.0;
    param_21[0x24] = 1.0;
    param_21[0x25] = 1.0;
  }
  if (*(char *)((int)param_21 + 0x9f) == '\0') {
    fVar6 = -*(float *)(DAT_40037a30 + 0xa2c);
    lVar28 = 2;
    pfVar20 = param_21;
    do {
      if (*(char *)(param_20 + 0x19) != '\0') {
        *pfVar20 = pfVar20[0x22];
      }
      fVar9 = *pfVar20;
      *pfVar20 = fVar9 - pfVar20[4];
      if (*(float *)(DAT_40037a30 + 0xa2c) < fVar9 - pfVar20[4]) {
        *pfVar20 = *(float *)(DAT_40037a30 + 0xa2c);
      }
      fVar9 = *pfVar20;
      if (fVar9 <= fVar6) {
        fVar9 = fVar6;
      }
      *pfVar20 = fVar9 + pfVar20[4];
      if (*(char *)(param_20 + 0x19) != '\0') {
        pfVar20[1] = pfVar20[0x23];
      }
      fVar9 = pfVar20[1];
      pfVar20[1] = fVar9 - pfVar20[5];
      if (*(float *)(DAT_40037a30 + 0xa2c) < fVar9 - pfVar20[5]) {
        pfVar20[1] = *(float *)(DAT_40037a30 + 0xa2c);
      }
      fVar9 = pfVar20[1];
      if (fVar9 <= fVar6) {
        fVar9 = fVar6;
      }
      pfVar20[1] = fVar9 + pfVar20[5];
      pfVar20 = pfVar20 + 2;
      lVar28 = lVar28 + -1;
    } while (lVar28 != 0);
  }
  else {
    *param_21 = 1.0;
    param_21[1] = 1.0;
    param_21[2] = 1.0;
    param_21[3] = 1.0;
  }
  *param_20 = param_15 * *param_21;
  param_20[1] = param_8 * param_21[1];
  param_20[2] = param_16 * param_21[2];
  param_20[3] = param_9 * param_21[3];
  fVar6 = DAT_0014171c;
  param_20[4] = *(float *)(DAT_40037a60 + 4) * *param_21 * DAT_0014171c;
  param_20[5] = *(float *)(DAT_40037a60 + 4) * param_21[1] * fVar6;
  param_20[6] = *(float *)(DAT_40037a60 + 8) * param_21[2] * fVar6;
  param_20[7] = *(float *)(DAT_40037a60 + 8) * param_21[3] * fVar6;
  iVar25 = 0;
  pfVar20 = param_21;
  do {
    bVar2 = false;
    fVar6 = (float)FUN_0012b750(*pfVar20 - pfVar20[0x22]);
    if ((fVar6 < *(float *)(DAT_40037a30 + 0x81c)) && (*(char *)(param_20 + 0x19) != '\0')) {
      bVar2 = true;
    }
    bVar3 = false;
    sVar26 = (short)iVar25;
    if ((bVar2) && (*(char *)((int)param_21 + sVar26 + 0xa2) == '\0')) {
      bVar3 = true;
    }
    *(bool *)((int)param_21 + sVar26 + 0xa2) = bVar2;
    pfVar20[8] = *param_22 + pfVar20[8];
    if ((!bVar2) || (bVar3)) {
      pfVar20[8] = 0.0;
    }
    else {
      fVar6 = pfVar20[8];
      if (*(float *)(DAT_40037a30 + 0x830) <= fVar6) {
        fVar6 = *(float *)(DAT_40037a30 + 0x830);
      }
      pfVar20[8] = fVar6;
    }
    uVar5 = 0;
    if (((bVar2) && (*(float *)(DAT_40037a30 + 0x830) <= pfVar20[8])) ||
       (*(char *)((int)param_21 + sVar26 + 0xa7) != '\0')) {
      uVar5 = 1;
    }
    *(undefined1 *)((int)param_21 + sVar26 + 0xa7) = uVar5;
    uVar5 = 0;
    if ((*(float *)(DAT_40037a60 + 0x438) < 1.0 - *pfVar20) &&
       (*(char *)((int)param_21 + sVar26 + 0xa7) != '\0')) {
      uVar5 = 1;
    }
    *(undefined1 *)((int)param_20 + sVar26 + 0x50) = uVar5;
    iVar25 = iVar25 + 1;
    pfVar20 = pfVar20 + 1;
  } while (iVar25 < 4);
  if (*(char *)((int)param_21 + 0xa1) == '\0') {
    if ((((*(char *)((int)param_21 + 0xa7) != '\0') && (*(char *)(param_21 + 0x2a) != '\0')) &&
        ((*(char *)((int)param_21 + 0xa9) != '\0' &&
         ((*(char *)((int)param_21 + 0xaa) != '\0' && (*(char *)(param_20 + 0x19) != '\0')))))) ||
       ((0.01 < fVar16 && (*(char *)(param_21 + 0x28) != '\0')))) {
      fVar16 = *param_22;
    }
    else {
      fVar16 = -*param_22;
    }
    fVar6 = param_21[0xc];
    param_21[0xc] = fVar16 + fVar6;
    if (600.0 < fVar16 + fVar6) {
      param_21[0xc] = 600.0;
    }
    if (param_21[0xc] <= 0.0) {
      param_21[0xc] = 0.0;
    }
  }
  else {
    param_21[0xc] = 0.0;
  }
  uVar5 = 0;
  if ((*(float *)(DAT_40037a30 + 0x834) <= param_21[0xc]) ||
     ((0.0 < param_21[0xc] && (*(char *)((int)param_21 + 0xa6) != '\0')))) {
    uVar5 = 1;
  }
  *(undefined1 *)((int)param_21 + 0xa6) = uVar5;
  *(char *)(param_20 + 0x15) = param_2;
  *(char *)((int)param_20 + 0x55) = param_3;
  param_20[8] = param_15;
  param_20[9] = param_16;
  param_20[10] = param_17;
  param_20[0xb] = *param_20;
  param_20[0xc] = param_20[1];
  param_20[0xd] = param_20[2];
  param_20[0xe] = param_20[3];
  param_20[0xf] = param_20[4];
  param_20[0x10] = param_20[5];
  param_20[0x11] = param_20[6];
  *(char *)((int)param_20 + 0x56) = param_4;
  param_20[0x12] = param_20[7];
  *(undefined1 *)((int)param_20 + 0x57) = *(undefined1 *)(param_20 + 0x14);
  *(undefined1 *)(param_20 + 0x16) = *(undefined1 *)((int)param_20 + 0x51);
  *(undefined1 *)((int)param_20 + 0x59) = *(undefined1 *)((int)param_20 + 0x52);
  *(undefined1 *)((int)param_20 + 0x5a) = *(undefined1 *)((int)param_20 + 0x53);
  *(undefined1 *)((int)param_20 + 0x5b) = *(undefined1 *)((int)param_21 + 0xa7);
  *(undefined1 *)(param_20 + 0x17) = *(undefined1 *)(param_21 + 0x2a);
  *(undefined1 *)((int)param_20 + 0x5d) = *(undefined1 *)((int)param_21 + 0xa9);
  *(undefined1 *)((int)param_20 + 0x5e) = *(undefined1 *)((int)param_21 + 0xaa);
  *(char *)((int)param_20 + 0x5f) = param_5;
  *(char *)(param_20 + 0x18) = param_2;
  *(char *)((int)param_20 + 0x61) = param_3;
  *(char *)((int)param_20 + 0x62) = param_4;
  *(char *)((int)param_20 + 99) = param_5;
  param_20[0x13] = param_18;
  *(undefined1 *)(param_21 + 0x26) = 0;
  *(undefined1 *)((int)param_21 + 0x99) = *(undefined1 *)((int)param_21 + 0xa6);
  *(undefined1 *)((int)param_21 + 0x9a) = 0;
  *(undefined1 *)((int)param_21 + 0x9b) = 0;
  *(undefined1 *)(param_21 + 0x27) = 0;
  *(undefined1 *)((int)param_21 + 0x9d) = 0;
  *(undefined1 *)((int)param_21 + 0x9e) = 0;
  *(undefined1 *)((int)param_21 + 0x9f) = 0;
  param_21[0x11] = local_d0[0];
  param_21[0x15] = local_a0;
  param_21[0x19] = local_e0[0];
  param_21[0x1d] = fVar18;
  param_21[4] = *param_21;
  param_21[0x12] = local_d0[1];
  param_21[0x16] = local_9c;
  param_21[0x1a] = local_e0[1];
  param_21[0x1e] = fVar8;
  param_21[5] = param_21[1];
  param_21[0x13] = local_d0[2];
  param_21[0x17] = local_98;
  param_21[0x1b] = local_e0[2];
  param_21[0x1f] = fVar7;
  param_21[6] = param_21[2];
  param_21[0x14] = local_d0[3];
  param_21[0x18] = local_94;
  param_21[0x1c] = local_e0[3];
  param_21[0x20] = fVar23;
  param_21[7] = param_21[3];
  *(undefined1 *)(param_21 + 0x28) = *(undefined1 *)((int)param_21 + 0xa6);
  *(undefined1 *)((int)param_21 + 0xa1) = 0;
  FUN_001406de();
  return;
}

