
void FUN_000cb860(int param_1,int param_2,undefined8 param_3,undefined8 param_4,undefined8 param_5,
                 undefined8 param_6,undefined8 param_7,undefined1 *param_8,undefined1 *param_9,
                 undefined1 *param_10,undefined1 *param_11,undefined1 *param_12,undefined1 *param_13
                 ,undefined1 *param_14,undefined1 *param_15,undefined1 *param_16,byte *param_17,
                 undefined4 *param_18,char *param_19)

{
  char cVar1;
  undefined4 uVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  bool bVar6;
  float fVar7;
  undefined8 uVar8;
  byte in_cr0;
  byte bVar9;
  undefined1 local_70;
  undefined1 local_6f;
  undefined1 local_6e;
  undefined1 local_6d;
  undefined1 local_6c;
  undefined1 local_6b;
  undefined1 local_6a;
  undefined1 local_69;
  undefined1 local_68;
  undefined1 local_67;
  undefined1 local_66;
  undefined1 local_65;
  undefined1 local_64;
  undefined1 local_63;
  undefined1 local_62;
  undefined1 local_61;
  undefined1 local_60;
  undefined1 local_5f;
  undefined1 local_5e;
  undefined1 local_5d;
  undefined4 local_5c;
  undefined4 local_58 [22];
  
  cVar1 = *param_19;
  uVar3 = (uint)LZCOUNT(param_1 + -0x42) >> 5;
  uVar4 = (uint)LZCOUNT(param_2 + -0x42) >> 5;
  uVar2 = *param_18;
  uVar8 = 0;
  bVar6 = true;
  if (((float)param_3 < *(float *)(DAT_40037a30 + 0xbc0)) &&
     (bVar6 = true,
     (byte)(in_cr0 & 0xb | (*(float *)(DAT_40037a30 + 0xbc4) < (float)param_3) << 2) >> 2 == 1)) {
    bVar6 = false;
  }
  if ((bVar6) && (uVar8 = 1, uVar3 == 0)) {
    uVar8 = 0;
  }
  FUN_000c91f0(param_6,*(undefined1 *)(DAT_40037a30 + 0xbd0),param_4,param_7,uVar8,
               *(undefined1 *)(DAT_40037a30 + 0xbb5),*(undefined1 *)(DAT_40037a30 + 0xbb4),
               *(undefined4 *)(DAT_40037a30 + 0xbe4));
  uVar5 = (uint)LZCOUNT((int)param_4) >> 5;
  bVar6 = false;
  if ((uVar5 == 0) && (param_17[3] != 0)) {
    bVar6 = true;
  }
  param_17[3] = (byte)uVar5;
  bVar9 = param_17[2];
  param_17[2] = (byte)uVar3;
  uVar8 = 0;
  if (((cVar1 != '\0') || (bVar6)) || ((uVar3 != 0 && ((uint)LZCOUNT((uint)bVar9) >> 5 != 0)))) {
    uVar8 = 1;
  }
  bVar9 = 0;
  FUN_000cb810(uVar8,param_3,uVar2,&local_5c,param_17 + 0x3c);
  uVar8 = 0;
  fVar7 = (float)FUN_0012b750(local_5c);
  bVar9 = bVar9 & 0xfb;
  if ((*(float *)(DAT_40037a60 + 0x58c) <= fVar7) && (bVar9 = 0, uVar3 != 0)) {
    uVar8 = 1;
  }
  FUN_000c91f0(param_6,*(undefined1 *)(DAT_40037a30 + 0xbd2),param_4,param_7,uVar8,
               *(undefined1 *)(DAT_40037a30 + 2999),*(undefined1 *)(DAT_40037a30 + 0xbb6),
               *(undefined4 *)(DAT_40037a30 + 0xbe8));
  uVar8 = 0;
  bVar6 = true;
  if (((float)param_5 < *(float *)(DAT_40037a30 + 0xbc0)) &&
     (bVar6 = true,
     (byte)(bVar9 & 0xb | (*(float *)(DAT_40037a30 + 0xbc4) < (float)param_5) << 2) >> 2 == 1)) {
    bVar6 = false;
  }
  if ((bVar6) && (uVar8 = 1, uVar4 == 0)) {
    uVar8 = 0;
  }
  FUN_000c91f0(param_6,*(undefined1 *)(DAT_40037a30 + 0xbd0),param_4,param_7,uVar8,
               *(undefined1 *)(DAT_40037a30 + 0xbb5),*(undefined1 *)(DAT_40037a30 + 0xbb4),
               *(undefined4 *)(DAT_40037a30 + 0xbe4));
  bVar6 = false;
  if ((uVar5 == 0) && (param_17[1] != 0)) {
    bVar6 = true;
  }
  param_17[1] = (byte)uVar5;
  bVar9 = *param_17;
  *param_17 = (byte)uVar4;
  uVar8 = 0;
  if (((cVar1 != '\0') || (bVar6)) || ((uVar4 != 0 && ((uint)LZCOUNT((uint)bVar9) >> 5 != 0)))) {
    uVar8 = 1;
  }
  FUN_000cb810(uVar8,param_5,uVar2,local_58,param_17 + 0x14);
  uVar8 = 0;
  fVar7 = (float)FUN_0012b750(local_58[0]);
  if ((*(float *)(DAT_40037a60 + 0x58c) <= fVar7) && (uVar4 != 0)) {
    uVar8 = 1;
  }
  FUN_000c91f0(param_6,*(undefined1 *)(DAT_40037a30 + 0xbd2),param_4,param_7,uVar8,
               *(undefined1 *)(DAT_40037a30 + 2999),*(undefined1 *)(DAT_40037a30 + 0xbb6),
               *(undefined4 *)(DAT_40037a30 + 0xbe8));
  *param_8 = local_70;
  *param_16 = local_6d;
  *param_9 = local_66;
  param_16[1] = local_63;
  param_16[2] = local_64;
  param_16[3] = local_65;
  *param_10 = local_62;
  *param_11 = local_61;
  param_16[4] = local_5e;
  param_16[5] = local_5f;
  param_16[6] = local_60;
  *param_12 = local_5d;
  param_16[7] = local_6e;
  param_16[8] = local_6f;
  *param_13 = local_6c;
  *param_14 = local_6b;
  param_16[9] = local_68;
  param_16[10] = local_69;
  param_16[0xb] = local_6a;
  *param_15 = local_67;
  return;
}

