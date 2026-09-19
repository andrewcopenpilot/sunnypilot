
short FUN_0012e3e0(short *param_1,uint param_2,int param_3)

{
  short sVar1;
  short sVar2;
  short sVar3;
  ushort uVar4;
  
  uVar4 = 1;
  for (; (uVar4 < param_2 && (*param_1 < param_3)); param_1 = param_1 + 2) {
    uVar4 = uVar4 + 1;
  }
  if (uVar4 == 1) {
    sVar3 = param_1[1];
  }
  else {
    sVar1 = param_1[-2];
    sVar2 = *param_1;
    sVar3 = param_1[1];
    if ((param_3 < sVar2) && ((int)sVar1 < (int)sVar2)) {
      sVar3 = (short)((((int)sVar3 - (int)param_1[-1]) * (param_3 - sVar1)) /
                     ((int)sVar2 - (int)sVar1)) + param_1[-1];
    }
  }
  return sVar3;
}

