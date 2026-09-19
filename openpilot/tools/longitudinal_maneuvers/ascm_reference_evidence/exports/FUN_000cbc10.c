
void FUN_000cbc10(int param_1,int param_2,int param_3,int param_4,int param_5,int param_6,
                 float param_7,int param_8,char param_9,char param_10,char param_11,float param_12,
                 float *param_13,undefined1 *param_14,float *param_15,undefined1 *param_16,
                 float *param_17,char *param_18)

{
  byte bVar1;
  uint uVar2;
  bool bVar3;
  undefined1 uVar4;
  uint uVar5;
  
  uVar5 = 0x42U - param_2 | param_2 - 0x42U;
  uVar2 = (uint)LZCOUNT((uint)LZCOUNT(param_1 + -0x42) >> 5) >> 5;
  bVar3 = false;
  if ((((uVar2 == 0) && (param_3 == 0)) && (param_4 == 0)) && ((param_5 == 0 && (param_6 == 0)))) {
    bVar3 = true;
  }
  bVar1 = *(byte *)((int)param_17 + 0x11);
  *(bool *)((int)param_17 + 0x11) = bVar3;
  if (((bVar3) && ((uint)LZCOUNT((uint)bVar1) >> 5 == 0)) && (*param_18 == '\0')) {
    param_17[2] = param_17[3] + *(float *)(DAT_40037a30 + 0x69c) * (param_7 - param_17[3]);
  }
  else if (bVar3) {
    param_17[2] = param_7;
  }
  param_17[3] = param_17[2];
  *param_13 = param_17[2];
  uVar4 = 0;
  if (((uVar2 != 0) || (param_5 != 0)) || (param_6 != 0)) {
    uVar4 = 1;
  }
  *param_14 = uVar4;
  bVar3 = false;
  if (((-1 < (int)uVar5) && (param_8 == 0)) &&
     ((param_9 == '\0' && ((param_10 == '\0' && (param_11 == '\0')))))) {
    bVar3 = true;
  }
  bVar1 = *(byte *)(param_17 + 4);
  *(bool *)(param_17 + 4) = bVar3;
  if (((bVar3) && ((uint)LZCOUNT((uint)bVar1) >> 5 == 0)) && (*param_18 == '\0')) {
    *param_17 = param_17[1] + *(float *)(DAT_40037a30 + 0x6a0) * (param_12 - param_17[1]);
  }
  else if (bVar3) {
    *param_17 = param_12;
  }
  param_17[1] = *param_17;
  *param_15 = *param_17;
  uVar4 = 0;
  if ((((int)uVar5 < 0) || (param_10 != '\0')) || (param_11 != '\0')) {
    uVar4 = 1;
  }
  *param_16 = uVar4;
  return;
}

