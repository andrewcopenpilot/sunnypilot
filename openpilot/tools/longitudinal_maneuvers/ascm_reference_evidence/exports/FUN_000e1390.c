
void FUN_000e1390(float param_1,float param_2,float param_3,uint param_4,float param_5,float param_6
                 ,float param_7,float param_8,float param_9,float param_10,float param_11,
                 float *param_12,float *param_13,float *param_14)

{
  float fVar1;
  undefined1 uVar2;
  float fVar3;
  
  if (*(char *)((int)param_14 + 0x3e) == '\0') {
    param_14[0xe] = param_7 + param_14[0xe];
  }
  else {
    param_14[0xe] = 0.0;
  }
  uVar2 = 0;
  if ((param_1 != *param_14) && (param_2 != param_14[1])) {
    uVar2 = 1;
  }
  *(undefined1 *)((int)param_14 + 0x3e) = uVar2;
  if (*(char *)((int)param_14 + 0x3f) == '\0') {
    if (*(char *)((int)param_14 + 0x3e) != '\0') {
      param_14[4] = param_14[2];
      param_14[5] = param_14[3];
    }
  }
  else {
    param_14[4] = param_2;
    param_14[5] = param_1;
  }
  fVar1 = param_14[5];
  if (*(char *)(param_14 + 0x10) == '\0') {
    param_14[6] = param_3;
  }
  else if (fVar1 < param_1) {
    param_14[6] = param_1 - fVar1;
  }
  else if (param_1 < fVar1) {
    param_14[6] = (param_1 - fVar1) + param_3;
  }
  if ((*(char *)((int)param_14 + 0x3e) != '\0') &&
     (param_14[7] = param_7 + param_14[0xe],
     param_7 + param_14[0xe] <= *(float *)(DAT_40037a30 + 0x82c))) {
    param_14[7] = param_14[6] * param_8;
  }
  fVar1 = param_14[4];
  if (*(char *)((int)param_14 + 0x41) == '\0') {
    param_14[8] = 0.0;
  }
  else if (fVar1 < param_2) {
    param_14[8] = param_2 - fVar1;
  }
  else if (param_2 < fVar1) {
    param_14[8] = (param_2 - fVar1) + *(float *)(DAT_40037a30 + 0x7bc);
  }
  if (*(char *)((int)param_14 + 0x3e) == '\0') {
    *(short *)(param_14 + 0xf) = *(short *)(param_14 + 0xf) + 1;
  }
  else {
    *(undefined2 *)(param_14 + 0xf) = 0;
  }
  if (param_4 < *(ushort *)(param_14 + 0xf)) {
    param_14[9] = 0.0;
  }
  else if (*(char *)((int)param_14 + 0x3e) != '\0') {
    fVar1 = (param_14[8] / param_11) / param_14[7];
    param_14[9] = fVar1;
    if (*(float *)(DAT_40037a30 + 0x934) < fVar1) {
      param_14[9] = *(float *)(DAT_40037a30 + 0x934);
    }
    if (param_14[9] <= *(float *)(DAT_40037a30 + 0x938)) {
      param_14[9] = *(float *)(DAT_40037a30 + 0x938);
    }
  }
  if (*(char *)((int)param_14 + 0x3e) == '\0') {
    fVar1 = param_14[10];
  }
  else {
    fVar1 = param_14[9];
    if (*(char *)((int)param_14 + 0x42) != '\0') {
      param_14[0xc] = (param_14[7] + param_14[0xb]) * 0.5;
    }
  }
  if (*(char *)((int)param_14 + 0x3e) != '\0') {
    param_14[0xd] = (fVar1 - param_14[10]) / param_14[0xc];
  }
  if (param_5 < param_14[9]) {
    fVar3 = param_14[0xd];
  }
  else {
    fVar3 = 0.0;
  }
  if (fVar3 <= param_9) {
    param_9 = fVar3;
  }
  if (param_10 < param_9) {
    param_10 = param_9;
  }
  *param_12 = param_10 * param_6;
  *param_13 = param_6 * param_14[9];
  *param_14 = param_1;
  param_14[1] = param_2;
  *(undefined1 *)((int)param_14 + 0x3f) = 0;
  param_14[2] = param_2;
  param_14[3] = param_1;
  *(undefined1 *)(param_14 + 0x10) = 1;
  *(undefined1 *)((int)param_14 + 0x41) = 1;
  param_14[10] = fVar1;
  param_14[0xb] = param_14[7];
  *(undefined1 *)((int)param_14 + 0x42) = *(undefined1 *)((int)param_14 + 0x3e);
  return;
}

