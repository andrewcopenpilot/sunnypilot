
void FUN_000b36a0(void)

{
  if (DAT_4000a168 == 1) {
    FUN_000429d0(0x132,0);
    DAT_4000a164 = DAT_4000a164 + 1;
    FUN_000b3300(*(undefined4 *)
                  ((&PTR_DAT_0014d6c0)[(uint)DAT_4000a162 * 2] + (DAT_4000a164 - 1) * 0xc + 8),
                 *(undefined4 *)
                  ((&PTR_DAT_0014d6c0)[(uint)DAT_4000a162 * 2] + (DAT_4000a164 - 1) * 0xc + 4),
                 FUN_000b3710);
  }
  return;
}

