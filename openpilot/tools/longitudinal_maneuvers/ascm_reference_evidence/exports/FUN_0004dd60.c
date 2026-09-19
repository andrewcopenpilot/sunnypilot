
void FUN_0004dd60(void)

{
  ulonglong uVar1;
  undefined1 uVar2;
  byte bVar3;
  
  FUN_00081c10(&DAT_400047cc);
  uVar2 = FUN_00079370(&DAT_400047cc);
  bVar3 = FUN_00079340(&DAT_400047cc);
  uVar1 = (ulonglong)(float)bVar3;
  if (0x7fffffff < uVar1) {
    uVar1 = 0x7fffffff;
  }
  FUN_000bb5c0(0x22);
  FUN_000c61f0(uVar1 & 0xff);
  FUN_000c6210(uVar2);
  FUN_000bb8d0(0x22);
  return;
}

