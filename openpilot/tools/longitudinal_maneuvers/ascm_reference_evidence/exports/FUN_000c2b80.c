
void FUN_000c2b80(int param_1)

{
  uint uVar1;
  undefined4 *puVar2;
  uint uVar3;
  longlong lVar4;
  
  uVar3 = 0;
  lVar4 = 4;
  do {
    uVar1 = uVar3 & 0xffff;
    puVar2 = (undefined4 *)(param_1 + uVar1 * 4);
    (&DAT_400371a8)[uVar1] = *puVar2;
    (&DAT_400371ac)[uVar1] = puVar2[1];
    (&DAT_400371b0)[uVar1] = puVar2[2];
    (&DAT_400371b4)[uVar1] = puVar2[3];
    (&DAT_400371b8)[uVar1] = puVar2[4];
    (&DAT_400371bc)[uVar1] = puVar2[5];
    (&DAT_400371c0)[uVar1] = puVar2[6];
    (&DAT_400371c4)[uVar1] = puVar2[7];
    uVar1 = (uVar3 + 8) * 4 & 0x3fffc;
    puVar2 = (undefined4 *)(param_1 + uVar1);
    *(undefined4 *)((int)&DAT_400371a8 + uVar1) = *puVar2;
    *(undefined4 *)((int)&DAT_400371ac + uVar1) = puVar2[1];
    *(undefined4 *)((int)&DAT_400371b0 + uVar1) = puVar2[2];
    *(undefined4 *)((int)&DAT_400371b4 + uVar1) = puVar2[3];
    *(undefined4 *)((int)&DAT_400371b8 + uVar1) = puVar2[4];
    *(undefined4 *)((int)&DAT_400371bc + uVar1) = puVar2[5];
    *(undefined4 *)((int)&DAT_400371c0 + uVar1) = puVar2[6];
    *(undefined4 *)((int)&DAT_400371c4 + uVar1) = puVar2[7];
    uVar1 = (uVar3 + 0x10) * 4 & 0x3fffc;
    puVar2 = (undefined4 *)(param_1 + uVar1);
    *(undefined4 *)((int)&DAT_400371a8 + uVar1) = *puVar2;
    *(undefined4 *)((int)&DAT_400371ac + uVar1) = puVar2[1];
    *(undefined4 *)((int)&DAT_400371b0 + uVar1) = puVar2[2];
    *(undefined4 *)((int)&DAT_400371b4 + uVar1) = puVar2[3];
    *(undefined4 *)((int)&DAT_400371b8 + uVar1) = puVar2[4];
    *(undefined4 *)((int)&DAT_400371bc + uVar1) = puVar2[5];
    *(undefined4 *)((int)&DAT_400371c0 + uVar1) = puVar2[6];
    *(undefined4 *)((int)&DAT_400371c4 + uVar1) = puVar2[7];
    uVar3 = uVar3 + 0x18;
    lVar4 = lVar4 + -1;
  } while (lVar4 != 0);
  return;
}

