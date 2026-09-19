
void FUN_00139b50(undefined8 param_1,int param_2,undefined2 *param_3,int param_4)

{
  short sVar1;
  int iVar2;
  undefined2 uVar3;
  
  if (*(short *)(param_2 + 8) < 0) {
    iVar2 = 1000000 / (int)DAT_4001e15e;
  }
  else {
    iVar2 = (int)DAT_4001e15e;
  }
  iVar2 = iVar2 * *(short *)(param_2 + 8);
  sVar1 = (short)(iVar2 >> 0x1f);
  uVar3 = FUN_0013bb20(((short)(iVar2 / 1000) + sVar1) -
                       ((short)((short)(iVar2 / 0x3e80000) + sVar1) >> 0xf),param_1,*param_3);
  *(undefined2 *)(param_4 + 2) = uVar3;
  return;
}

