
void FUN_0013a360(undefined8 param_1,int param_2,undefined2 *param_3,undefined2 *param_4,int param_5
                 ,int param_6)

{
  short sVar1;
  ushort uVar2;
  short sVar4;
  int iVar3;
  short sVar5;
  undefined2 uVar6;
  
  DAT_4001e172 = param_3[3];
  DAT_4001e174 = param_3[2];
  if (DAT_4001d8f2 == 1) {
    sVar4 = FUN_0012e3e0(DAT_40037a40 + 0x7fa,3,*param_4);
    *(short *)(param_5 + 0x1a) = *(short *)(param_5 + 0x1a) + sVar4;
  }
  sVar4 = FUN_0013bbc0(*param_3,param_5,*param_4);
  param_3[2] = sVar4;
  if (sVar4 < 0) {
    iVar3 = (int)DAT_4001e15e;
  }
  else {
    iVar3 = 1000000 / (int)DAT_4001e15e;
  }
  iVar3 = iVar3 * sVar4;
  sVar4 = (short)(iVar3 >> 0x1f);
  sVar4 = ((short)(iVar3 / 1000) + sVar4) - ((short)((short)(iVar3 / 0x3e80000) + sVar4) >> 0xf);
  param_3[2] = sVar4;
  if (*(short *)(param_6 + 10) == 0) {
    *(undefined2 *)(param_6 + 10) = 1;
  }
  uVar2 = *(ushort *)(param_6 + 10);
  sVar1 = *(short *)(param_6 + 0x10);
  sVar5 = FUN_0012e3e0(DAT_40037a40 + 0x790,3,*param_4);
  iVar3 = ((sVar4 * 100) / (int)(uint)uVar2) * (((int)sVar1 * (int)sVar5) / 1000 + (1000 - sVar5));
  sVar4 = (short)(iVar3 >> 0x1f);
  param_3[3] = ((short)(iVar3 / 1000) + sVar4) -
               ((short)((short)(iVar3 / 0x3e80000) + sVar4) >> 0xf);
  if (*(char *)(param_3 + 5) == '\x01') {
    if (DAT_4001e171 == '\x01') {
      DAT_4001e1a8 = FUN_0012e5e0(param_3[2],DAT_4001e1a8,
                                  (int)(uint)*(ushort *)(DAT_40037a40 + 0x72e) / (int)param_1);
      param_3[2] = DAT_4001e1a8;
      if ((DAT_4001d8f2 == -1) &&
         ((DAT_4001d990 == '\x02' ||
          ((DAT_4001d990 == '\x01' && (DAT_4001deb4 < *(short *)(DAT_40037a40 + 0x6fc))))))) {
        uVar6 = FUN_0012e3e0(DAT_40037a40 + 0x6f0,3,*param_4);
      }
      else {
        uVar6 = FUN_0012e3e0(DAT_40037a40 + 0x6e4,3,*param_4);
      }
      uVar6 = FUN_0012e630(param_3[2],DAT_4001e174,*(undefined4 *)(DAT_40037a40 + 0x6dc),uVar6,
                           param_1);
      param_3[2] = uVar6;
    }
    else {
      DAT_4001e174 = *(undefined2 *)(param_2 + 2);
      param_3[2] = DAT_4001e174;
      DAT_4001e1a8 = DAT_4001e174;
    }
  }
  else {
    param_3[2] = *(undefined2 *)(DAT_40037a40 + 0x834);
    param_3[3] = *(undefined2 *)(DAT_40037a40 + 0x836);
  }
  return;
}

