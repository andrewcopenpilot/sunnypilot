
void FUN_0013d3c0(undefined4 *param_1,undefined4 *param_2)

{
  undefined4 uVar1;
  float fVar2;
  float fVar3;
  undefined4 uVar4;
  undefined1 uVar5;
  
  uVar4 = *param_2;
  *param_1 = uVar4;
  uVar1 = param_2[3];
  param_1[1] = uVar1;
  fVar2 = (float)param_2[1];
  param_1[2] = fVar2;
  param_1[3] = param_2[4];
  fVar3 = (float)param_2[2];
  param_1[4] = fVar3;
  param_1[5] = 0;
  param_1[6] = fVar2 + DAT_4001e478;
  param_1[7] = fVar3 + DAT_4001e47c;
  param_1[8] = (float)*(byte *)(param_2 + 9);
  uVar4 = FUN_0013d5e0(uVar4,uVar1,DAT_4001e470);
  param_1[9] = uVar4;
  uVar5 = FUN_0013d4b0(*(undefined1 *)((int)param_2 + 0x19));
  *(undefined1 *)(param_1 + 10) = uVar5;
  uVar5 = FUN_0013d4e0(*(undefined1 *)(param_2 + 7));
  *(undefined1 *)((int)param_1 + 0x29) = uVar5;
  uVar5 = FUN_0013d510(*(undefined1 *)((int)param_2 + 0x1e));
  *(undefined1 *)((int)param_1 + 0x2a) = uVar5;
  *(undefined1 *)((int)param_1 + 0x2b) = *(undefined1 *)((int)param_2 + 0x1f);
  param_1[0xc] = param_2[5];
  param_1[0xd] = 0;
  uVar4 = FUN_0013d530(*(undefined1 *)(param_2 + 6));
  param_1[0xe] = uVar4;
  uVar5 = FUN_0013d570(*(undefined1 *)((int)param_2 + 0x1b));
  *(undefined1 *)(param_1 + 0xf) = uVar5;
  uVar5 = FUN_0013d5a0(*(undefined1 *)((int)param_2 + 0x1a));
  *(undefined1 *)((int)param_1 + 0x3d) = uVar5;
  *(undefined1 *)((int)param_1 + 0x3e) = 0;
  if (*(char *)(param_2 + 8) == '\x01') {
    *(undefined1 *)(param_1 + 0xb) = 1;
  }
  else {
    *(undefined1 *)(param_1 + 0xb) = 0;
  }
  if (*(char *)((int)param_2 + 0x2a) == '\0') {
    *(undefined1 *)((int)param_1 + 0x3f) = 0;
  }
  else {
    *(undefined1 *)((int)param_1 + 0x3f) = 1;
  }
  return;
}

