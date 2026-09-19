
void FUN_000b3710(void)

{
  if (DAT_4000a168 == 1) {
    DAT_4000a160 = DAT_4000a160 ^ 1;
    if (DAT_4000a164 < *(ushort *)(&DAT_0014d6c4 + (uint)DAT_4000a162 * 8)) {
      if (DAT_4000a160 == 1) {
        FUN_000b36a0();
      }
      else {
        FUN_000b3620();
      }
    }
    else {
      DAT_4000a164 = 0;
      DAT_4000a162 = DAT_4000a162 + 1;
      if ((DAT_4000a162 < 0xe) && ((&PTR_DAT_0014d6c0)[(uint)DAT_4000a162 * 2] != (undefined *)0x0))
      {
        FUN_000b3620();
      }
      else {
        FUN_000429d0(0x133,0);
        DAT_4000a166 = DAT_4000a166 + 1;
        DAT_4000a162 = 0;
      }
    }
  }
  return;
}

