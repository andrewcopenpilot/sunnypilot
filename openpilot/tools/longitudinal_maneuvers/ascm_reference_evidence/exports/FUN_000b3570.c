
void FUN_000b3570(void)

{
  char cVar1;
  undefined1 local_20 [32];
  
  if (DAT_4000a168 == 1) {
    if ((DAT_4000a161 & 1) == 0) {
      FUN_000b37c0();
      FUN_000429d0(0x133,1);
      FUN_000b3620();
    }
    DAT_4000a161 = DAT_4000a161 + 1;
  }
  else if (DAT_4000a168 == 0x5a) {
    local_20[0] = 0x5a;
    cVar1 = FUN_000b67a0(8,local_20,1);
    if (cVar1 == '\0') {
      DAT_4000a168 = 0xa5;
    }
  }
  else if (DAT_4000a168 == 0xf) {
    local_20[0] = 0;
    cVar1 = FUN_000b67a0(8,local_20,1);
    if (cVar1 == '\0') {
      DAT_4000a168 = 0xf0;
    }
  }
  return;
}

