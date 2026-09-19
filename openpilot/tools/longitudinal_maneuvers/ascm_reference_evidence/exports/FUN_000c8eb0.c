
void FUN_000c8eb0(undefined4 param_1,undefined4 param_2,undefined1 param_3,undefined1 param_4,
                 undefined1 param_5,undefined1 param_6,undefined1 param_7,undefined1 param_8,
                 undefined1 param_9,undefined4 param_10,undefined4 param_11,char param_12,
                 char param_13,undefined4 param_14,undefined4 param_15,char param_16,char param_17,
                 undefined4 param_18,undefined4 param_19,char param_20,char param_21,
                 undefined4 param_22,char param_23,undefined4 param_24,char param_25,byte param_26,
                 undefined1 param_27,undefined1 param_28,char param_29,undefined1 param_30,
                 undefined1 param_31,undefined1 param_32,undefined4 param_33,byte param_34,
                 undefined4 *param_35)

{
  uint uVar1;
  
  *param_35 = param_1;
  param_35[1] = param_1;
  param_35[2] = param_2;
  param_35[3] = param_2;
  *(undefined1 *)((int)param_35 + 0x4b) = param_3;
  *(undefined1 *)(param_35 + 0x13) = param_4;
  *(undefined1 *)((int)param_35 + 0x4d) = param_5;
  *(undefined1 *)((int)param_35 + 0x4e) = param_6;
  *(undefined1 *)((int)param_35 + 0x37) = param_7;
  *(undefined1 *)((int)param_35 + 0x36) = param_8;
  *(undefined1 *)((int)param_35 + 0x4f) = param_9;
  param_35[4] = param_10;
  param_35[5] = param_11;
  if (param_12 == '\0') {
    *(undefined1 *)(param_35 + 0xe) = 0x42;
  }
  else {
    *(undefined1 *)(param_35 + 0xe) = 0x24;
  }
  *(undefined1 *)((int)param_35 + 0x39) = *(undefined1 *)(param_35 + 0xe);
  if (param_13 == '\0') {
    *(undefined1 *)((int)param_35 + 0x3a) = 0x42;
  }
  else {
    *(undefined1 *)((int)param_35 + 0x3a) = 0x24;
  }
  *(undefined1 *)((int)param_35 + 0x3b) = *(undefined1 *)((int)param_35 + 0x3a);
  param_35[6] = param_14;
  param_35[7] = param_15;
  if (param_16 == '\0') {
    *(undefined1 *)(param_35 + 0xf) = 0x42;
  }
  else {
    *(undefined1 *)(param_35 + 0xf) = 0x24;
  }
  *(undefined1 *)((int)param_35 + 0x3d) = *(undefined1 *)(param_35 + 0xf);
  if (param_17 == '\0') {
    *(undefined1 *)((int)param_35 + 0x3e) = 0x42;
  }
  else {
    *(undefined1 *)((int)param_35 + 0x3e) = 0x24;
  }
  *(undefined1 *)((int)param_35 + 0x3f) = *(undefined1 *)((int)param_35 + 0x3e);
  param_35[8] = param_18;
  param_35[9] = param_19;
  if (param_20 == '\0') {
    *(undefined1 *)(param_35 + 0x10) = 0x42;
  }
  else {
    *(undefined1 *)(param_35 + 0x10) = 0x24;
  }
  *(undefined1 *)((int)param_35 + 0x41) = *(undefined1 *)(param_35 + 0x10);
  if (param_21 == '\0') {
    *(undefined1 *)((int)param_35 + 0x42) = 0x42;
  }
  else {
    *(undefined1 *)((int)param_35 + 0x42) = 0x24;
  }
  *(undefined1 *)((int)param_35 + 0x43) = *(undefined1 *)((int)param_35 + 0x42);
  param_35[10] = param_22;
  if (param_23 == '\0') {
    *(undefined1 *)(param_35 + 0x11) = 0x42;
  }
  else {
    *(undefined1 *)(param_35 + 0x11) = 0x24;
  }
  *(undefined1 *)((int)param_35 + 0x45) = *(undefined1 *)(param_35 + 0x11);
  param_35[0xb] = param_24;
  if (param_25 == '\0') {
    *(undefined1 *)((int)param_35 + 0x46) = 0x42;
  }
  else {
    *(undefined1 *)((int)param_35 + 0x46) = 0x24;
  }
  *(char *)(param_35 + 0x14) = (char)((uint)LZCOUNT(param_26 - 2) >> 5);
  *(undefined1 *)(param_35 + 0xd) = param_27;
  *(undefined1 *)((int)param_35 + 0x4a) = param_28;
  *(undefined1 *)((int)param_35 + 0x35) = param_28;
  if (param_29 == '\0') {
    *(undefined1 *)((int)param_35 + 0x47) = 0x42;
  }
  else {
    *(undefined1 *)((int)param_35 + 0x47) = 0x24;
  }
  *(char *)((int)param_35 + 0x51) = param_29;
  *(undefined1 *)((int)param_35 + 0x52) = param_30;
  *(undefined1 *)((int)param_35 + 0x53) = param_30;
  *(undefined1 *)(param_35 + 0x15) = param_30;
  *(undefined1 *)((int)param_35 + 0x55) = param_30;
  *(undefined1 *)((int)param_35 + 0x56) = param_30;
  *(undefined1 *)((int)param_35 + 0x57) = param_31;
  *(undefined1 *)(param_35 + 0x16) = param_31;
  *(undefined1 *)((int)param_35 + 0x59) = param_31;
  *(undefined1 *)((int)param_35 + 0x5a) = param_31;
  *(undefined1 *)((int)param_35 + 0x5b) = param_31;
  *(undefined1 *)(param_35 + 0x17) = param_32;
  *(undefined1 *)((int)param_35 + 0x5d) = param_32;
  *(undefined1 *)((int)param_35 + 0x5e) = param_32;
  *(undefined1 *)((int)param_35 + 0x5f) = param_32;
  *(undefined1 *)(param_35 + 0x18) = param_32;
  if (*DAT_40037a60 == '\0') {
    uVar1 = 1;
  }
  else {
    uVar1 = (uint)LZCOUNT((uint)param_34) >> 5;
  }
  if (uVar1 == 0) {
    *(undefined1 *)(param_35 + 0x12) = 0x24;
  }
  else {
    *(undefined1 *)(param_35 + 0x12) = 0x42;
  }
  if (*DAT_40037a60 == '\0') {
    param_35[0xc] = 0;
  }
  else {
    param_35[0xc] = param_33;
  }
  *(undefined1 *)((int)param_35 + 0x49) = *(undefined1 *)(param_35 + 0x12);
  return;
}

