
void FUN_000cc070(float param_1,float param_2,ulonglong param_3,ulonglong param_4,ulonglong param_5,
                 float param_6,float param_7,undefined4 param_8,undefined4 param_9,char param_10,
                 byte param_11,byte param_12,char param_13,float param_14,char param_15,
                 undefined4 param_16,undefined4 param_17,undefined4 param_18,undefined4 param_19,
                 float param_20,float param_21,float param_22,undefined4 *param_23,
                 undefined4 *param_24,undefined1 *param_25,byte *param_26,undefined4 *param_27,
                 undefined4 *param_28,undefined4 *param_29,undefined1 *param_30,byte *param_31,
                 undefined4 *param_32,float *param_33,char *param_34)

{
  char cVar1;
  uint uVar2;
  uint uVar3;
  bool bVar4;
  bool bVar5;
  int iVar6;
  undefined1 uVar7;
  float fVar10;
  ulonglong uVar8;
  undefined8 uVar9;
  float fVar11;
  float fVar12;
  float fVar13;
  float fVar14;
  ulonglong unaff_r14;
  ulonglong uVar15;
  ulonglong uVar16;
  ulonglong unaff_r27;
  byte bVar17;
  char local_a8;
  char local_a7;
  char local_a6;
  char local_a5;
  undefined4 local_a4;
  undefined4 local_a0;
  undefined4 local_9c;
  undefined4 local_98;
  undefined4 local_94;
  undefined4 local_90;
  undefined4 local_8c;
  undefined4 local_88;
  undefined4 local_80;
  undefined4 local_7c;
  undefined4 local_78;
  undefined4 local_74;
  undefined4 local_70;
  undefined4 local_6c;
  undefined4 local_68;
  undefined4 local_64;
  char local_60;
  float local_5c;
  undefined4 local_48;
  undefined4 uStack_14;
  
  local_48 = (undefined4)unaff_r14;
  uStack_14 = (undefined4)unaff_r27;
  cVar1 = *param_34;
  uVar8 = (ulonglong)(uint)param_21;
  fVar11 = param_22;
  if (cVar1 == '\0') {
    uVar8 = unaff_r27 & 0xffffffff00000000 |
            (ulonglong)
            (uint)(param_33[7] + *(float *)(DAT_40037a30 + 0x6a4) * (param_21 - param_33[7]));
    fVar11 = param_33[8] + *(float *)(DAT_40037a30 + 0x6a4) * (param_22 - param_33[8]);
  }
  param_33[7] = (float)uVar8;
  param_33[8] = fVar11;
  fVar12 = (float)param_3;
  fVar13 = (float)param_4;
  fVar14 = (float)param_5;
  fVar10 = (param_6 + fVar14 + fVar12 + fVar13) * 0.25;
  if (param_2 < *(float *)(DAT_40037a30 + 0x670)) {
    if (fVar10 < 1.0) {
      fVar10 = 1.0;
    }
    local_60 = param_7 / fVar10 < *(float *)(DAT_40037a30 + 0x6ac);
  }
  else {
    local_60 = false;
  }
  uVar7 = 0;
  fVar10 = (float)FUN_0012b750(uVar8 & 0xffffffff00000000 |
                               (ulonglong)(uint)((float)uVar8 - param_1));
  if ((fVar10 < *(float *)(DAT_40037a30 + 0x674)) || (local_60 != '\0')) {
    uVar7 = 1;
  }
  *(undefined1 *)(param_32 + 1) = uVar7;
  bVar17 = (byte)(*(byte *)(param_33 + 9) + 1);
  if (0xff < (ushort)(*(byte *)(param_33 + 9) + 1)) {
    bVar17 = 0xff;
  }
  if (0x95 < bVar17) {
    bVar17 = 1;
  }
  *(byte *)(param_33 + 9) = bVar17;
  uVar8 = param_3;
  uVar15 = param_5;
  uVar16 = param_4;
  local_5c = param_6;
  if (cVar1 == '\0') {
    fVar10 = *(float *)(DAT_40037a30 + 0x6a8);
    local_5c = param_33[6] + fVar10 * (param_6 - param_33[6]);
    uVar8 = (ulonglong)(uint)(param_33[3] + fVar10 * (fVar12 - param_33[3]));
    uVar15 = unaff_r14 & 0xffffffff00000000 |
             (ulonglong)(uint)(param_33[5] + fVar10 * (fVar14 - param_33[5]));
    uVar16 = (ulonglong)(uint)(param_33[4] + fVar10 * (fVar13 - param_33[4]));
  }
  param_33[3] = (float)uVar8;
  param_33[4] = (float)uVar16;
  param_33[5] = (float)uVar15;
  param_33[6] = local_5c;
  FUN_000cbe50(bVar17,uVar8,*(undefined4 *)(DAT_40037a30 + 0x6b4),&local_a8,param_32 + 0x18);
  FUN_000cbe50(bVar17,uVar16,*(undefined4 *)(DAT_40037a30 + 0x6b4),&local_a7,param_32 + 0x11);
  bVar4 = false;
  if ((local_a8 != '\0') && (local_a7 != '\0')) {
    bVar4 = true;
  }
  FUN_000cbe50(bVar17,uVar15,*(undefined4 *)(DAT_40037a30 + 0x6b4),&local_a6,param_32 + 10);
  FUN_000cbe50(bVar17,local_5c,*(undefined4 *)(DAT_40037a30 + 0x6b4),&local_a5,param_32 + 3);
  if (fVar12 <= fVar13) {
    param_4 = param_3;
  }
  if ((float)param_4 <= fVar14) {
    param_5 = param_4;
  }
  if ((float)param_5 <= param_6) {
    param_6 = (float)param_5;
  }
  uVar7 = 0;
  if ((((bVar4) && (local_a6 != '\0')) && (local_a5 != '\0')) &&
     (*(float *)(DAT_40037a30 + 0x6b0) < param_6)) {
    uVar7 = 1;
  }
  *(undefined1 *)((int)param_32 + 5) = uVar7;
  uVar2 = (uint)LZCOUNT((uint)param_11) >> 5;
  uVar3 = (uint)LZCOUNT((uint)param_12) >> 5;
  uVar7 = 0;
  fVar10 = (float)FUN_0012b750(param_8);
  if ((((fVar10 <= *(float *)(DAT_40037a30 + 0x6b8)) &&
       (fVar10 = (float)FUN_0012b750(param_9), fVar10 <= *(float *)(DAT_40037a30 + 0x68c))) &&
      ((param_10 == '\0' && ((param_13 != '\0' && (uVar2 != 0)))))) && (uVar3 != 0)) {
    uVar7 = 1;
  }
  *(undefined1 *)((int)param_32 + 6) = uVar7;
  bVar4 = false;
  if ((*(char *)((int)param_32 + 5) != '\0') && (*(char *)((int)param_32 + 6) != '\0')) {
    bVar4 = true;
  }
  uVar7 = 0;
  if ((*(char *)(param_32 + 1) != '\0') && (bVar4)) {
    uVar7 = 1;
  }
  *(undefined1 *)((int)param_32 + 7) = uVar7;
  fVar10 = param_14;
  if (param_15 == '\0') {
    fVar10 = *param_33;
  }
  fVar12 = fVar10;
  if ((cVar1 == '\0') && (*(char *)((int)param_33 + 0x25) == '\0')) {
    fVar12 = param_33[2] + *(float *)(DAT_40037a30 + 0x698) * (fVar10 - param_33[2]);
  }
  param_33[2] = fVar12;
  iVar6 = DAT_40037a30;
  fVar12 = *(float *)(DAT_40037a30 + 0x688);
  uVar8 = FUN_0012b750(param_14);
  uVar9 = FUN_0012bd30(uVar8 & 0xffffffff00000000 | (ulonglong)(uint)((float)uVar8 / fVar12),
                       iVar6 + 0x728,0x41000000);
  uVar8 = FUN_0012bed0(DAT_40037a30 + 0x74c,uVar9,0x41000000);
  if (param_15 == '\0') {
    uVar8 = (ulonglong)(uint)param_33[1];
  }
  local_70 = param_16;
  local_6c = param_17;
  local_68 = param_18;
  local_64 = param_19;
  FUN_000cbf30(param_16,param_17,*(undefined1 *)(DAT_40037a60 + 1),param_18,param_19,
               (ulonglong)(uint)param_21,uVar8,param_1);
  DAT_4000d7f8 = local_a0;
  bVar5 = false;
  fVar11 = (float)FUN_0012b750(fVar11 - param_20);
  if ((fVar11 < *(float *)(DAT_40037a30 + 0x674)) || (local_60 != '\0')) {
    bVar5 = true;
  }
  *(bool *)(param_32 + 2) = bVar5;
  uVar7 = 0;
  if ((bVar5) && (bVar4)) {
    uVar7 = 1;
  }
  *(undefined1 *)((int)param_32 + 9) = uVar7;
  local_80 = param_16;
  local_7c = param_17;
  local_78 = param_18;
  local_74 = param_19;
  FUN_000cbf30(param_16,param_17,*(undefined1 *)(DAT_40037a60 + 1),param_18,param_19,param_22,uVar8,
               param_20);
  DAT_4000d7f4 = local_90;
  *param_23 = local_9c;
  *param_24 = local_a4;
  *param_25 = (char)uVar3;
  *param_26 = param_12;
  *param_27 = local_98;
  *param_28 = local_8c;
  *param_29 = local_94;
  *param_32 = local_88;
  *param_30 = (char)uVar2;
  *param_31 = param_11;
  *param_33 = fVar10;
  *(char *)((int)param_33 + 0x25) = cVar1;
  param_33[1] = (float)uVar8;
  return;
}

