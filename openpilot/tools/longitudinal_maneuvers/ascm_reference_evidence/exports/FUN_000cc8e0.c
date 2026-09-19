
void FUN_000cc8e0(int param_1,int param_2,undefined1 param_3,undefined8 param_4,undefined8 param_5,
                 undefined8 param_6,undefined8 param_7,undefined8 param_8,undefined4 param_9,
                 undefined4 *param_10,undefined4 *param_11,undefined1 *param_12,undefined4 *param_13
                 ,uint param_14)

{
  undefined8 uVar1;
  undefined1 local_40;
  undefined1 local_3f [63];
  
  uVar1 = 0;
  if ((param_1 != 0) || (param_2 != 0)) {
    uVar1 = 1;
  }
  FUN_000ca5c0(uVar1,param_4,param_5,param_6,param_7,param_8,param_13 + 1,&local_40);
  *param_10 = param_13[1];
  FUN_000ca5c0(uVar1,param_4,param_5,param_6,param_7,param_9,param_13,local_3f);
  *param_11 = *param_13;
  *param_12 = local_40;
  *(undefined1 *)(param_13 + 2) = local_3f[0];
  *(undefined1 *)((int)param_13 + 9) = param_3;
  FUN_000ca610(param_13 + 1,(ulonglong)param_14 + 4);
  FUN_000ca610(param_13,(ulonglong)param_14);
  return;
}

