
void FUN_000dfad0(undefined8 param_1,undefined8 param_2,int param_3,int param_4,float param_5,
                 float param_6,int param_7,int param_8,char param_9,float param_10,float param_11,
                 float param_12,float param_13,float param_14,float param_15,char *param_16,
                 undefined1 *param_17,float *param_18,float *param_19,float *param_20)

{
  bool bVar1;
  bool bVar2;
  bool bVar3;
  bool bVar4;
  bool bVar5;
  int iVar6;
  undefined1 uVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  int iVar11;
  uint uVar12;
  byte bVar13;
  
  uVar12 = 2U - param_3 | param_3 - 2U;
  fVar9 = param_19[6];
  param_19[6] = param_6;
  iVar11 = DAT_40037a30;
  bVar3 = false;
  if ((((param_7 == 0) && (param_8 == 0)) && (param_9 == '\0')) && (param_4 == 0)) {
    bVar3 = true;
  }
  bVar2 = false;
  bVar1 = false;
  if (param_10 <= *(float *)(DAT_40037a30 + 0x8c0)) {
    fVar8 = (float)FUN_0012b750();
    bVar1 = false;
    if (fVar8 <= *(float *)(iVar11 + 0x928)) {
      bVar1 = true;
    }
  }
  iVar6 = DAT_40037a30;
  bVar13 = 0;
  if (bVar1) {
    fVar8 = (float)FUN_0012b750(param_2);
    bVar13 = bVar13 & 0xfb;
    bVar2 = false;
    iVar11 = iVar6;
    if (fVar8 <= *(float *)(iVar6 + 0x8e4)) {
      bVar2 = true;
    }
  }
  bVar1 = false;
  if ((param_5 < *(float *)(iVar11 + 0x918)) ||
     ((*(float *)(iVar11 + 0x914) < param_5 && (param_6 <= *(float *)(iVar11 + 0x8c4))))) {
    bVar1 = true;
  }
  bVar13 = bVar13 & 0xb | (*(float *)(iVar11 + 0x8e0) < (param_6 - fVar9) / *param_20) << 2;
  bVar4 = false;
  if (((!bVar1) || (!bVar2)) || ((bVar13 >> 2 == 0 || ((-1 < (int)uVar12 || (!bVar3)))))) {
    bVar4 = true;
  }
  bVar5 = false;
  if ((!bVar4) && (*(char *)((int)param_19 + 0x1f) != '\0')) {
    bVar5 = true;
  }
  *(bool *)((int)param_19 + 0x1f) = bVar4;
  if (bVar5) {
    *param_19 = *(float *)(DAT_40037a30 + 0x908);
  }
  else {
    fVar9 = *param_19 - *param_20;
    if (fVar9 < 0.0) {
      fVar9 = 0.0;
    }
    *param_19 = fVar9;
  }
  fVar8 = *(float *)(DAT_40037a30 + 0x8cc) + param_11;
  fVar9 = param_11 + *(float *)(DAT_40037a30 + 0x8d0);
  if (*(char *)(DAT_40037a60 + 1) == '\x01') {
    fVar10 = (param_12 + param_13) * 0.5;
  }
  else if (*(char *)(DAT_40037a60 + 1) == '\0') {
    fVar10 = (param_14 + param_15) * 0.5;
  }
  else {
    fVar10 = (param_12 + param_13 + param_14 + param_15) * 0.25;
  }
  if (fVar10 <= fVar8) {
    fVar8 = fVar10;
  }
  if (fVar8 <= fVar9) {
    fVar8 = fVar9;
  }
  if (*(char *)(param_19 + 7) == '\0') {
    if ((bVar4) || (0.0 < *param_19)) {
      fVar9 = *(float *)(DAT_40037a30 + 0x8ec);
    }
    else {
      fVar9 = *(float *)(DAT_40037a30 + 0x8e8);
    }
    fVar8 = param_19[1] + fVar9 * (fVar8 - param_19[1]);
  }
  param_19[1] = fVar8;
  *param_18 = param_11 - fVar8;
  if (*(char *)((int)param_19 + 0x1d) == '\0') {
    *param_18 = param_19[3] + *(float *)(DAT_40037a30 + 0x8f4) * (*param_18 - param_19[3]);
  }
  param_19[3] = *param_18;
  if (*(float *)(DAT_40037a30 + 0x8cc) < *param_18) {
    *param_18 = *(float *)(DAT_40037a30 + 0x8cc);
  }
  if (*param_18 <= *(float *)(DAT_40037a30 + 0x8d0)) {
    *param_18 = *(float *)(DAT_40037a30 + 0x8d0);
  }
  fVar9 = (float)FUN_0012b750(*param_18);
  if (((((fVar9 <= *(float *)(DAT_40037a30 + 0x8c8)) || (!bVar1)) || (!bVar2)) ||
      ((bVar13 >> 2 == 0 || (-1 < (int)uVar12)))) || (!bVar3)) {
    param_19[5] = 0.0;
  }
  else {
    fVar8 = param_19[5];
    fVar10 = *param_20;
    param_19[5] = fVar10 + fVar8;
    if (*(float *)(DAT_40037a30 + 0x90c) < fVar10 + fVar8) {
      param_19[5] = *(float *)(DAT_40037a30 + 0x90c);
    }
    if (param_19[5] <= 0.0) {
      param_19[5] = 0.0;
    }
  }
  if (*(float *)(DAT_40037a30 + 0x8d4) <= fVar9) {
    param_19[4] = 0.0;
  }
  else {
    fVar9 = param_19[4];
    fVar8 = *param_20;
    param_19[4] = fVar8 + fVar9;
    if (*(float *)(DAT_40037a30 + 0x910) < fVar8 + fVar9) {
      param_19[4] = *(float *)(DAT_40037a30 + 0x910);
    }
    if (param_19[4] <= 0.0) {
      param_19[4] = 0.0;
    }
  }
  if (*(float *)(DAT_40037a30 + 0x90c) <= param_19[5]) {
    *param_16 = '\x01';
  }
  else if (*(float *)(DAT_40037a30 + 0x910) <= param_19[4]) {
    *param_16 = '\0';
  }
  else {
    *param_16 = *(char *)((int)param_19 + 0x1e);
  }
  uVar7 = 0;
  if ((((*param_16 != '\0') && (!bVar1)) && (bVar3)) ||
     ((((bVar1 && (bVar2)) && (bVar13 >> 2 != 0)) && (((int)uVar12 < 0 && (bVar3)))))) {
    uVar7 = 1;
  }
  *param_17 = uVar7;
  if (*(char *)((int)param_19 + 0x1d) == '\0') {
    *param_18 = param_19[2] + *(float *)(DAT_40037a30 + 0x8f0) * (*param_18 - param_19[2]);
  }
  param_19[2] = *param_18;
  *(undefined1 *)(param_19 + 7) = 0;
  *(undefined1 *)((int)param_19 + 0x1d) = 0;
  *(char *)((int)param_19 + 0x1e) = *param_16;
  return;
}

