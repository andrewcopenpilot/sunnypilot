
undefined8 FUN_000e3260(int param_1)

{
  undefined1 auStack_70 [112];
  
  if (*(char *)(DAT_40037a30 + 0xa1c) != '\0') {
    DAT_4000d830 = auStack_70;
    *(undefined1 **)(param_1 + 0x15c) = DAT_4000d830;
    FUN_000e3050();
    FUN_000dfe90(param_1 + 4,param_1 + 8,param_1 + 0x54,param_1 + 0x158,
                 *(undefined4 *)(param_1 + 0x15c),param_1 + 0x160);
    FUN_000e31f0(param_1);
  }
  return 0;
}

