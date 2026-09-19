
void FUN_00139ce0(undefined8 param_1,undefined8 param_2,int param_3,undefined8 param_4,
                 undefined8 param_5,undefined8 param_6,undefined8 param_7,undefined8 param_8)

{
  short sVar1;
  
  sVar1 = *(short *)(param_3 + 6);
  if (sVar1 < *(short *)(param_3 + 2)) {
    *(short *)(param_3 + 8) = *(short *)(param_3 + 8) - (*(short *)(param_3 + 2) - sVar1);
    *(short *)(param_3 + 2) = sVar1;
  }
  FUN_00139bc0(param_4,param_6);
  FUN_00139c10(param_1,param_4,param_6,param_3,param_8,param_2);
  FUN_00139b50(param_2,param_3,param_4,param_6);
  FUN_00139950(param_2,param_3,param_4,param_6);
  FUN_001399a0(param_2,param_3,param_4,param_6);
  FUN_00139a40(param_1,param_2,param_3,param_4,param_6);
  FUN_00139850(param_4,param_6,param_5,param_7);
  return;
}

