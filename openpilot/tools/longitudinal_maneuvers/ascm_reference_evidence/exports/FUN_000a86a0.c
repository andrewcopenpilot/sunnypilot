
void FUN_000a86a0(uint param_1,uint param_2)

{
  undefined2 uVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  undefined8 uVar5;
  char cVar6;
  int iVar7;
  
  iVar4 = (param_1 & 0xffff) * 4;
  iVar2 = *(int *)(&DAT_00143f80 + iVar4);
  uVar5 = FUN_000af230();
  FUN_000a1510(param_1,2);
  iVar7 = (param_2 & 0xffff) * 0x10;
  iVar3 = param_1 * 0x14;
  do {
    *(uint *)(&DAT_40009670 + iVar3) = (uint)*(ushort *)(iVar2 + iVar7 + 0x80);
    cVar6 = FUN_000a1560(param_1,2);
    if ((*(uint *)(&DAT_40009670 + iVar3) & 0x100) != 0x100) break;
  } while (cVar6 != '\0');
  FUN_000a1640(param_1,2);
  *(int *)(iVar2 + 0x30) = 1 << ((byte)param_2 & 0x3f);
  iVar7 = iVar2 + iVar7;
  *(undefined2 *)(&DAT_40009674 + iVar3) = *(undefined2 *)(iVar7 + 0x84);
  *(undefined2 *)(&DAT_40009676 + iVar3) = *(undefined2 *)(iVar7 + 0x86);
  *(undefined4 *)(&DAT_40009678 + iVar3) = *(undefined4 *)(iVar7 + 0x88);
  *(undefined4 *)(&DAT_4000967c + iVar3) = *(undefined4 *)(iVar7 + 0x8c);
  iVar7 = (param_1 & 0xffff) * 2;
  *(undefined2 *)(&DAT_40009680 + iVar3) =
       *(undefined2 *)((uint)*(ushort *)(&DAT_00143f98 + iVar7) * 0x10 + iVar2 + 0x82);
  FUN_000af240(uVar5);
  if (cVar6 != '\0') {
    iVar2 = (param_1 & 0xffff) * 0x10;
    *(undefined **)(&DAT_400095ec + iVar2) = &DAT_40009670 + iVar3;
    *(undefined **)(&DAT_400095f0 + iVar2) = &DAT_40009678 + iVar3;
    *(undefined **)(&DAT_400096c0 + iVar4) = &DAT_40009678 + iVar3;
    uVar1 = *(undefined2 *)
             (&DAT_00142f54 +
             (((param_2 - *(ushort *)(&DAT_00143ea8 + iVar7)) +
              (uint)*(ushort *)(&DAT_00143e9c + iVar7)) * 2 & 0x1fffe));
    *(undefined2 *)(&DAT_400095f4 + iVar2) = uVar1;
    cVar6 = FUN_000a87e0(param_1);
    if (cVar6 == '\x01') {
      FUN_000a88c0(uVar1);
    }
  }
  return;
}

