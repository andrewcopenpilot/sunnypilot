
undefined2 FUN_0013a570(int param_1,int param_2,int param_3,short param_4,longlong param_5)

{
  short sVar1;
  short sVar3;
  uint uVar2;
  
  sVar1 = (short)(param_1 / param_2);
  if (sVar1 < 0) {
    sVar3 = 0;
  }
  else {
    sVar3 = (short)param_5 + -1;
    if ((int)sVar1 < (int)param_5) {
      sVar3 = sVar1;
    }
  }
  param_4 = param_4 - sVar3;
  if (param_4 < 0) {
    param_4 = param_4 + (short)param_5;
  }
  uVar2 = FUN_0012e5a0(param_4,0,param_5 + -1);
  return *(undefined2 *)(param_3 + (uVar2 & 0xff) * 2);
}

