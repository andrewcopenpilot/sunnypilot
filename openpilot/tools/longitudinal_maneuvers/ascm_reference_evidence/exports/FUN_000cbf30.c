
void FUN_000cbf30(float param_1,float param_2,int param_3,float param_4,float param_5,float param_6,
                 float param_7,ulonglong param_8,float param_9,char param_10,char param_11,
                 float param_12,float param_13,float param_14,float param_15,undefined4 param_16,
                 undefined4 param_17,undefined4 param_18,float *param_19,undefined4 param_20,
                 undefined4 param_21,undefined4 param_22,float *param_23)

{
  float fVar2;
  ulonglong uVar1;
  byte bVar3;
  
  if (param_3 == 1) {
    fVar2 = (param_1 + param_2) * 0.5;
  }
  else if (param_3 == 0) {
    fVar2 = (param_4 + param_5) * 0.5;
  }
  else {
    fVar2 = (param_1 + param_2 + param_4 + param_5) * 0.25;
  }
  if (param_10 == '\0') {
    *param_23 = *param_23 + param_15 * ((param_6 - fVar2) - *param_23);
    if (param_11 == '\0') {
      uVar1 = (ulonglong)(uint)param_23[1];
    }
    else {
      uVar1 = (ulonglong)(uint)(param_23[1] + param_12 * (*param_23 - param_23[1]));
    }
  }
  else {
    *param_23 = param_6 - fVar2;
    uVar1 = param_8;
  }
  bVar3 = 0;
  param_23[1] = (float)uVar1;
  FUN_000cbd70(uVar1,param_19);
  uVar1 = FUN_000c9b80(param_16,param_17,*param_19,param_8,param_18,param_13,param_14,param_20);
  fVar2 = param_6 - (float)param_8;
  if (*param_19 <= param_13) {
    param_13 = *param_19;
  }
  if ((byte)(bVar3 & 0xb | (param_14 < param_13) << 2) >> 2 != 0) {
    param_14 = param_13;
  }
  FUN_000cbd70(uVar1 & 0xffffffff00000000 |
               (ulonglong)
               (uint)((1.0 - param_7) * (fVar2 - param_9) + param_7 * (param_6 - param_14)),param_21
              );
  FUN_000cbd70(param_8 & 0xffffffff00000000 | (ulonglong)(uint)fVar2,param_22);
  return;
}

