
void FUN_0013b6c0(int param_1,short *param_2,int param_3,int param_4)

{
  ushort uVar1;
  short sVar2;
  uint uVar3;
  longlong lVar4;
  
  uVar3 = *(uint *)(param_3 + 0xc);
  if ((((((uVar3 >> 0x19 & 1) == 0) && ((uVar3 >> 0x1a & 1) != 0)) && ((uVar3 >> 0x18 & 1) == 0)) &&
      (((uVar3 >> 0x1c & 1) == 0 && ((uVar3 >> 0x1b & 1) == 0)))) &&
     (*(short *)(DAT_40037a40 + 0x7cc) < *param_2)) {
    if ((byte)(*(char *)(param_4 + 0x293) - 1U) < 2) {
      sVar2 = (short)param_1;
      if (*(short *)(DAT_40037a40 + 0x7ce) < *(short *)(param_4 + 0xe)) {
        if ((uint)DAT_4001e19c < 0xffffU - param_1) {
          DAT_4001e19c = DAT_4001e19c + sVar2;
        }
      }
      else {
        DAT_4001e19c = 0;
      }
      if (*(short *)(param_4 + 0xe) < *(short *)(DAT_40037a40 + 2000)) {
        if ((uint)DAT_4001e19e < 0xffffU - param_1) {
          DAT_4001e19e = DAT_4001e19e + sVar2;
        }
      }
      else {
        DAT_4001e19e = 0;
      }
      uVar1 = *(ushort *)(DAT_40037a40 + 0x7d2);
      if ((uVar1 < DAT_4001e19c) || (uVar1 < DAT_4001e19e)) {
        if (((uVar1 < DAT_4001e19c) && (DAT_4001e19c < *(ushort *)(DAT_40037a40 + 0x7d4))) &&
           (DAT_4001e190 = FUN_0012e5e0((longlong)*(short *)(param_4 + 6) * 100 -
                                        (ulonglong)DAT_4001e198,DAT_4001e190,
                                        (int)(uint)*(ushort *)(DAT_40037a40 + 0x7d6) / param_1),
           (uint)DAT_4001e1a0 < 0xffffU - param_1)) {
          DAT_4001e1a0 = DAT_4001e1a0 + sVar2;
        }
        if (((*(ushort *)(DAT_40037a40 + 0x7d2) < DAT_4001e19e) &&
            (DAT_4001e19e < *(ushort *)(DAT_40037a40 + 0x7d4))) &&
           (DAT_4001e194 = FUN_0012e5e0((longlong)*(short *)(param_4 + 6) * 100 -
                                        (ulonglong)DAT_4001e198,DAT_4001e194,
                                        (int)(uint)*(ushort *)(DAT_40037a40 + 0x7d6) / param_1),
           (uint)DAT_4001e1a2 < 0xffffU - param_1)) {
          DAT_4001e1a2 = DAT_4001e1a2 + sVar2;
        }
      }
      else if ((*(short *)(param_4 + 0xe) <= *(short *)(DAT_40037a40 + 0x7ce)) &&
              (*(short *)(DAT_40037a40 + 2000) <= *(short *)(param_4 + 0xe))) {
        DAT_4001e198 = *(short *)(param_4 + 6) * 100;
      }
    }
    else {
      DAT_4001e198 = *(short *)(param_4 + 6) * 100;
    }
  }
  else {
    DAT_4001e198 = *(short *)(param_4 + 6) * 100;
  }
  if ((*(ushort *)(DAT_40037a40 + 0x7d8) < DAT_4001e1a0) &&
     (*(ushort *)(DAT_40037a40 + 0x7d8) < DAT_4001e1a2)) {
    uVar3 = (((DAT_4001e190 - DAT_4001e194) * param_1) / 1000) *
            (int)*(short *)(DAT_40037a40 + 0x7da);
    lVar4 = (longlong)((int)uVar3 / 1000000 + ((int)uVar3 >> 0x1f)) + (ulonglong)(uVar3 >> 0x1f);
    if (lVar4 != 0) {
      DAT_4001e194 = FUN_0012e5e0(0,DAT_4001e194,
                                  (int)(uint)*(ushort *)(DAT_40037a40 + 0x7d6) / param_1);
      DAT_4001e190 = FUN_0012e5e0(0,DAT_4001e190,
                                  (int)(uint)*(ushort *)(DAT_40037a40 + 0x7d6) / param_1);
      DAT_4001e158 = FUN_0012e5a0((ulonglong)DAT_4001e158 + lVar4,0,0xffff);
    }
  }
  return;
}

