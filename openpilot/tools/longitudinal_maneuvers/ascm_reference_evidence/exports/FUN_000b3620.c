
void FUN_000b3620(void)

{
  if (DAT_4000a168 == 1) {
    DAT_4000a16c = *(undefined4 *)
                    ((&PTR_DAT_0014d6c0)[(uint)DAT_4000a162 * 2] + (uint)DAT_4000a164 * 0xc);
    DAT_4000a170 = *(undefined4 *)
                    ((&PTR_DAT_0014d6c0)[(uint)DAT_4000a162 * 2] + (uint)DAT_4000a164 * 0xc + 4);
    DAT_4000a176 = DAT_4000a166;
    FUN_000429d0(0x132,1);
    FUN_000b3300(&DAT_4000a16c,0x14,FUN_000b3710);
  }
  return;
}

