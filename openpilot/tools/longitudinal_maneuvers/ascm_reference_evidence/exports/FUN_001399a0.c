
void FUN_001399a0(int param_1,int param_2,undefined2 *param_3,int param_4)

{
  short sVar1;
  int iVar2;
  int iVar3;
  undefined2 uVar4;
  
  if ((*(char *)(DAT_40037a40 + 0x5df) == '\x01') &&
     (((*(uint *)(param_3 + 4) >> 0x1c & 1) != 0 || (*(char *)(param_2 + 0xe) == '\0')))) {
    sVar1 = *(short *)(DAT_40037a40 + 0x68c);
  }
  else {
    sVar1 = *(short *)(param_2 + 2);
  }
  if (sVar1 < 0) {
    iVar2 = 1000000 / (int)*(short *)(param_1 + 0x16);
  }
  else {
    iVar2 = (int)DAT_4001e15e;
  }
  iVar2 = (iVar2 * sVar1) / 1000;
  iVar3 = (int)*(short *)(DAT_40037a40 + 0x690);
  if ((iVar2 <= iVar3) && (iVar3 = iVar2, iVar2 < *(short *)(DAT_40037a40 + 0x68e))) {
    iVar3 = (int)*(short *)(DAT_40037a40 + 0x68e);
  }
  uVar4 = FUN_0013bb20((short)iVar3,param_1,*param_3);
  *(undefined2 *)(param_4 + 4) = uVar4;
  return;
}

