
void FUN_001333f0(void)

{
  byte bVar3;
  byte bVar4;
  byte bVar5;
  byte bVar6;
  uint uVar1;
  uint uVar2;
  byte bVar7;
  byte bVar8;
  byte bVar9;
  
  FUN_00045520(0x1f);
  bVar3 = FUN_000c2f00();
  bVar4 = FUN_000c3080();
  bVar5 = FUN_000c3060();
  bVar6 = FUN_000c30a0();
  uVar1 = FUN_000c31c0();
  uVar2 = FUN_000c3200();
  FUN_00045560(0x1f);
  FUN_00045520(0x1a);
  bVar7 = FUN_000c1160();
  FUN_00045560(0x1a);
  FUN_00045520(0x19);
  bVar8 = FUN_000c0cd0();
  FUN_00045560(0x19);
  FUN_00045520(0x11);
  bVar9 = FUN_000bf630();
  FUN_00045560(0x11);
  if ((((((bVar3 == 0x24) || (bVar4 == 0x24)) || (bVar5 == 0x24)) ||
       ((bVar6 == 0x24 || ((uVar1 & 0xff) == 1)))) ||
      (((uVar2 & 0xff) == 1 || ((bVar7 == 1 || (bVar8 == 0)))))) || (bVar9 == 1)) {
    DAT_4001d967 = 1;
  }
  else {
    DAT_4001d967 = 0;
  }
  DAT_4001daf8 = ((uint)LZCOUNT(bVar9 - 1) & 0x20) << 0xe |
                 ((uint)LZCOUNT((uint)bVar8) & 0x20) << 0xf |
                 ((uint)LZCOUNT(bVar7 - 1) & 0x20) << 0x10 |
                 ((uint)LZCOUNT((uVar2 & 0xff) - 1) & 0x20) << 0x11 |
                 ((uint)LZCOUNT((uVar1 & 0xff) - 1) & 0x20) << 0x12 |
                 ((uint)LZCOUNT(bVar5 - 0x24) & 0x20) << 0x13 |
                 ((uint)LZCOUNT(bVar6 - 0x24) & 0x20) << 0x14 |
                 ((uint)LZCOUNT(bVar4 - 0x24) & 0x20) << 0x15 |
                 ((uint)LZCOUNT(bVar3 - 0x24) & 0x20) << 0x16 | DAT_4001daf8 & 0xf007ffff;
  return;
}

