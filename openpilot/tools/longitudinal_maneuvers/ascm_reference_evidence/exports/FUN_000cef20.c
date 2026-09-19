
undefined8 FUN_000cef20(int param_1)

{
  undefined1 auStack_a0 [160];
  
  if (*(char *)(DAT_40037a30 + 0xa18) != '\0') {
    DAT_4000d830 = auStack_a0;
    *(undefined1 **)(param_1 + 0x6cc) = DAT_4000d830;
    FUN_000ce970();
    FUN_000cd920(param_1 + 8,param_1 + 0xc,param_1 + 0x2f4,param_1 + 0x6c8,
                 *(undefined4 *)(param_1 + 0x6cc),param_1 + 0x6d0);
    *(undefined1 *)(param_1 + 4) = 0;
    FUN_000cecd0(param_1);
  }
  return 0;
}

