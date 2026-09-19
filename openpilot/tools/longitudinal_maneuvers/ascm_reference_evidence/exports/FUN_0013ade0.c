
void FUN_0013ade0(int param_1,int param_2,undefined2 *param_3,short *param_4,int param_5,
                 short *param_6)

{
  bool bVar1;
  int iVar2;
  short sVar3;
  
  bVar1 = DAT_4001e1a4 == 0;
  DAT_4001e1a4 = DAT_4001e1a4 + -1;
  if (bVar1) {
    DAT_4001e1a4 = 0;
  }
  if ((*(uint *)(param_4 + 6) >> 0x1a & 1) == 0) {
    *(undefined1 *)((int)param_6 + 0x293) = 0;
    *param_6 = 0;
    *(undefined1 *)((int)param_3 + 0x1d) = 3;
  }
  else {
    sVar3 = param_4[1];
    if ((sVar3 == *param_4) && (*(char *)(param_2 + 0xe) != '\0')) {
      *(undefined1 *)((int)param_6 + 0x293) = 2;
      *param_6 = *param_4;
      *(undefined1 *)((int)param_3 + 0x1d) = 0;
    }
    else if ((sVar3 == *(short *)(DAT_40037a40 + 0x7a6)) && (*(char *)(param_2 + 0xe) != '\0')) {
      *(undefined1 *)((int)param_6 + 0x293) = 4;
      *param_6 = *param_4;
      *(undefined1 *)((int)param_3 + 0x1d) = 0;
    }
    else if (*param_4 == *(short *)(DAT_40037a40 + 0x7a8)) {
      *(undefined1 *)((int)param_6 + 0x293) = 3;
      *param_6 = param_4[1];
      *(undefined1 *)((int)param_3 + 0x1d) = 1;
    }
    else if ((int)sVar3 + (int)param_6[3] < (int)*(short *)(param_5 + 4)) {
      *param_6 = sVar3;
      *(undefined1 *)((int)param_6 + 0x293) = 1;
      *(undefined1 *)((int)param_3 + 0x1d) = 1;
    }
    else {
      *(undefined1 *)((int)param_6 + 0x293) = 1;
      if ((int)*(short *)(param_5 + 4) < (int)*param_4 + (int)param_6[3]) {
        *param_6 = *param_4;
        *(undefined1 *)((int)param_3 + 0x1d) = 0;
      }
      else {
        sVar3 = FUN_0012e590();
        *param_6 = sVar3;
        if (sVar3 == *param_4) {
          *(undefined1 *)((int)param_3 + 0x1d) = 0;
        }
        else {
          *(undefined1 *)((int)param_3 + 0x1d) = 2;
        }
      }
    }
    if ((*(uint *)(param_4 + 6) >> 0x1c & 1) == 0) {
      if (((*(uint *)(param_4 + 6) >> 0x1b & 1) == 0) ||
         (param_6[7] <= *(short *)(DAT_40037a40 + 0x81e))) {
        iVar2 = 1000;
      }
      else {
        *(undefined1 *)((int)param_6 + 0x293) = 4;
        sVar3 = FUN_0012e3e0(DAT_40037a40 + 0x7ea,3,*param_3);
        iVar2 = (int)sVar3;
      }
    }
    else {
      sVar3 = FUN_0012e3e0(DAT_40037a40 + 0x7de,3,*(undefined2 *)(param_5 + 0xe));
      iVar2 = (int)sVar3;
      if (((*(uint *)(param_3 + 10) >> 0x18 & 1) != 0) || (DAT_4001e1a4 != 0)) {
        if ((*(uint *)(param_3 + 10) >> 0x18 & 1) == 1) {
          DAT_4001e1a4 = (short)((int)(uint)*(ushort *)(DAT_40037a40 + 0x7f6) / param_1);
        }
        *(undefined1 *)((int)param_6 + 0x293) = 3;
      }
    }
    iVar2 = iVar2 * *param_6;
    sVar3 = (short)(iVar2 >> 0x1f);
    *param_6 = ((short)(iVar2 / 1000) + sVar3) -
               ((short)((short)(iVar2 / 0x3e80000) + sVar3) >> 0xf);
  }
  return;
}

