
void FUN_0004e550(void)

{
  ulonglong uVar1;
  byte bVar2;
  
  FUN_00081b80(&DAT_400047d8);
  bVar2 = FUN_00079250(&DAT_400047d8);
  uVar1 = (ulonglong)(float)bVar2;
  if (0x7fffffff < uVar1) {
    uVar1 = 0x7fffffff;
  }
  FUN_000bb5c0(0x22);
  FUN_000c61c0(uVar1 & 0xff);
  FUN_000bb8d0(0x22);
  return;
}

