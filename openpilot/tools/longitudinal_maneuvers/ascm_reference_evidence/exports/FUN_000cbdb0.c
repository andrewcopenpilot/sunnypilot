
void FUN_000cbdb0(ulonglong param_1,float param_2,float param_3,int param_4,int param_5,int param_6,
                 undefined4 *param_7,undefined4 *param_8,undefined1 *param_9,undefined1 *param_10)

{
  undefined1 uVar1;
  ulonglong uVar2;
  undefined4 local_40;
  undefined4 local_3c;
  float local_38 [14];
  
  uVar2 = FUN_000cbd70(param_1 & 0xffffffff00000000 |
                       (ulonglong)(uint)((float)param_1 * *(float *)(DAT_40037a58 + 0x30)),local_38)
  ;
  uVar2 = FUN_000cbd70(uVar2 & 0xffffffff00000000 | (ulonglong)(uint)(param_2 + local_38[0]),
                       &local_40);
  FUN_000cbd70(uVar2 & 0xffffffff00000000 | (ulonglong)(uint)(local_38[0] + param_3),&local_3c);
  *param_7 = local_40;
  *param_8 = local_3c;
  uVar1 = 0;
  if ((param_4 != 0) || (param_5 != 0)) {
    uVar1 = 1;
  }
  *param_9 = uVar1;
  uVar1 = 0;
  if ((param_5 != 0) || (param_6 != 0)) {
    uVar1 = 1;
  }
  *param_10 = uVar1;
  return;
}

