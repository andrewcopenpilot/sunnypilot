
void FUN_0013a180(undefined8 param_1,undefined2 *param_2,undefined2 *param_3,undefined8 param_4,
                 int param_5,int param_6,int param_7)

{
  uint uVar1;
  bool bVar2;
  undefined2 uVar3;
  
  DAT_4001e176 = *(undefined2 *)(param_5 + 8);
  bVar2 = DAT_4001e178 == 0;
  DAT_4001e178 = DAT_4001e178 + -1;
  if (bVar2) {
    DAT_4001e178 = 0;
  }
  if ((((((DAT_4001d9b8 >> 0x10 & 1) != 0) && (0 < *(short *)(param_7 + 0xe))) ||
       ((*(uint *)(param_6 + 0xc) >> 0x1a & 1) == 0)) ||
      (((*(uint *)(param_3 + 4) >> 0x19 & 1) == 0 && (DAT_4001d994 == 0)))) ||
     ((*(uint *)(param_3 + 10) >> 0x1a & 1) != 0)) {
    *(undefined1 *)(param_7 + 0xe8) = 0;
  }
  if (((*(uint *)(param_6 + 0xc) >> 0x1a & 1) == 0) ||
     (((((*(uint *)(param_6 + 0xc) >> 0x1c & 1) == 0 && (0 < *(short *)(param_7 + 0xe))) ||
       (((*(uint *)(param_3 + 10) >> 0x18 & 1) == 0 &&
        ((DAT_4001e1a4 == 0 && (*(char *)(param_7 + 0xe8) != '\x01')))))) &&
      ((*(uint *)(param_3 + 4) >> 0x19 & 1) == 0)))) {
    if (*(char *)(param_5 + 10) == '\x02') {
      uVar1 = *(uint *)(param_3 + 10);
      if ((uVar1 >> 0x17 & 1) == 0) {
        if (*(short *)(param_7 + 0x10) < *(short *)(DAT_40037a40 + 0x730)) {
          DAT_4001e178 = (short)((int)(uint)*(ushort *)(DAT_40037a40 + 0x734) / (int)param_1);
          *(uint *)(param_3 + 10) = uVar1 | 0x800000;
        }
      }
      else if ((*(short *)(DAT_40037a40 + 0x732) < *(short *)(param_7 + 0x10)) &&
              (DAT_4001e178 == 0)) {
        *(uint *)(param_3 + 10) = uVar1 & 0xfe3fffff;
      }
      uVar3 = FUN_0013bbc0(*(undefined2 *)(param_5 + 2),param_4,*param_3);
      *(undefined2 *)(param_5 + 8) = uVar3;
      uVar3 = FUN_0012e580(uVar3,*(undefined2 *)(DAT_40037a40 + 0x83a));
      *(undefined2 *)(param_5 + 8) = uVar3;
      if (DAT_4001e171 == '\x02') {
        if ((*(uint *)(param_6 + 0xc) >> 0x16 & 1) != 0) {
          uVar3 = FUN_0012e630(uVar3,DAT_4001e176,*(undefined4 *)(DAT_40037a40 + 0x704),
                               *(undefined4 *)(DAT_40037a40 + 0x700),param_1);
          *(undefined2 *)(param_5 + 8) = uVar3;
        }
      }
      else {
        DAT_4001e176 = *param_2;
        *(undefined2 *)(param_5 + 8) = DAT_4001e176;
      }
    }
    else {
      *(undefined2 *)(param_5 + 8) = *(undefined2 *)(DAT_40037a40 + 0x838);
      if (DAT_4001e178 == 0) {
        *(uint *)(param_3 + 10) = *(uint *)(param_3 + 10) & 0xff7fffff;
      }
    }
  }
  else {
    *(undefined1 *)(param_7 + 0xe8) = 1;
    uVar3 = FUN_0013bbc0(*(short *)(param_7 + 10) + *(short *)(param_7 + 6) +
                         *(short *)(param_7 + 4) + *(short *)(DAT_40037a40 + 0x7f8),param_4,*param_3
                        );
    uVar3 = FUN_0012e630(uVar3,DAT_4001e176,*(undefined4 *)(DAT_40037a40 + 0x704),
                         *(undefined4 *)(DAT_40037a40 + 0x700),param_1);
    *(undefined2 *)(param_5 + 8) = uVar3;
  }
  return;
}

