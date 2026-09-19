
void FUN_00132fb0(void)

{
  char cVar1;
  char cVar2;
  char cVar3;
  char cVar4;
  char cVar5;
  undefined1 uVar6;
  
  FUN_00045520(0x22);
  cVar1 = FUN_000c61d0();
  cVar2 = FUN_000c62a0();
  cVar3 = FUN_000c62c0();
  cVar4 = FUN_000c6200();
  cVar5 = FUN_000c6220();
  DAT_4001d95d = FUN_000c6240();
  DAT_4001d973 = FUN_000c6280();
  if (*(char *)(DAT_40037a40 + 0x670) == '\x01') {
    uVar6 = FUN_000c6050();
  }
  else {
    uVar6 = 0;
  }
  FUN_00045560(0x22);
  if (cVar1 == '\x01') {
    DAT_4001d959 = 1;
  }
  else {
    DAT_4001d959 = 2;
  }
  if ((cVar4 == '\x01') && (cVar5 == '\0')) {
    DAT_4001d95b = 1;
  }
  else if ((cVar4 == '\0') && (cVar5 == '\0')) {
    DAT_4001d95b = 2;
  }
  else {
    DAT_4001d95b = 0;
  }
  if (cVar3 == '\0') {
    if (cVar2 == '\x01') {
      DAT_4001d95a = 1;
    }
    else {
      DAT_4001d95a = 2;
    }
  }
  else {
    DAT_4001d95a = 0;
  }
  DAT_4001d931 = uVar6;
  return;
}

