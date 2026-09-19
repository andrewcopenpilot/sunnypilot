
undefined8 FUN_000a87e0(uint param_1)

{
  uint uVar1;
  int iVar2;
  char cVar4;
  undefined8 uVar3;
  
  iVar2 = (param_1 & 0xffff) * 0x10;
  if ((*(byte *)(*(int *)(&DAT_400095ec + iVar2) + 3) & 0xf) <
      (byte)(&DAT_001430d8)[*(ushort *)(&DAT_400095f4 + iVar2)]) {
    uVar3 = 0;
  }
  else {
    cVar4 = FUN_000acb70(&DAT_400095e8 + (param_1 & 0xffff) * 8);
    if (cVar4 == '\x01') {
      uVar1 = *(uint *)(&DAT_001434a0 + (uint)*(ushort *)(&DAT_400095f4 + iVar2) * 4);
      if (uVar1 != 0) {
        (&DAT_40009640)[param_1 & 0xffff] = *(ushort *)(&DAT_400095f4 + iVar2);
        cVar4 = (*(code *)(uVar1 & 0xfffffffe))(&DAT_400095e8 + (param_1 & 0xffff) * 8);
        if (cVar4 == '\0') {
          return 0;
        }
      }
      if (*(int *)(&DAT_0014319c + (uint)*(ushort *)(&DAT_400095f4 + iVar2) * 4) != 0) {
        uVar3 = FUN_000af230();
        FUN_000a7420(*(undefined4 *)(&DAT_0014319c + (uint)*(ushort *)(&DAT_400095f4 + iVar2) * 4),
                     *(undefined4 *)(&DAT_400095f0 + iVar2),
                     (&DAT_001430d8)[*(ushort *)(&DAT_400095f4 + iVar2)]);
        FUN_000af240(uVar3);
      }
      uVar3 = 1;
    }
    else {
      uVar3 = 0;
    }
  }
  return uVar3;
}

