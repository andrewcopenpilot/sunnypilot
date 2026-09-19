
void FUN_000e1af0(int param_1,float param_2,float param_3,float *param_4,float *param_5,
                 float *param_6)

{
  bool bVar1;
  bool bVar2;
  
  if (*(char *)((int)param_6 + 0x12) == '\0') {
    if (*(short *)(param_6 + 4) != 0) {
      *(short *)(param_6 + 4) = *(short *)(param_6 + 4) + -1;
    }
  }
  else {
    *(undefined2 *)(param_6 + 4) = 10;
  }
  bVar1 = false;
  if ((param_1 != 0) && (*(char *)((int)param_6 + 0x13) == '\0')) {
    bVar1 = true;
  }
  *(char *)((int)param_6 + 0x13) = (char)param_1;
  bVar2 = false;
  if (((*(short *)(param_6 + 4) != 0) || (param_1 == 0)) || (bVar1)) {
    bVar2 = true;
  }
  if (bVar2) {
    if (param_1 == 0) {
      *param_4 = *param_6;
    }
    else {
      *param_4 = param_2;
    }
  }
  else if (param_1 == 0) {
    *param_4 = param_6[3];
  }
  else {
    *param_4 = param_6[3] + *(float *)(DAT_40037a30 + 0x80c) * (param_2 - param_6[3]);
  }
  param_6[3] = *param_4;
  if (bVar2) {
    if (param_1 == 0) {
      *param_5 = param_6[1];
    }
    else {
      *param_5 = param_3;
    }
  }
  else if (param_1 == 0) {
    *param_5 = param_6[2];
  }
  else {
    *param_5 = param_6[2] + *(float *)(DAT_40037a30 + 0x800) * (param_3 - param_6[2]);
  }
  param_6[2] = *param_5;
  *(undefined1 *)((int)param_6 + 0x12) = 0;
  *param_6 = *param_4;
  param_6[1] = *param_5;
  return;
}

