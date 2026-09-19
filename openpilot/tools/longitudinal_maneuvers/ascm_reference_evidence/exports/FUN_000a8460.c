
void FUN_000a8460(uint param_1,uint param_2)

{
  undefined2 uVar1;
  int iVar2;
  int iVar3;
  int iVar4;
  int iVar5;
  uint uVar6;
  undefined8 uVar7;
  char cVar9;
  ushort uVar8;
  int iVar10;
  ushort *puVar11;
  
  iVar4 = (param_1 & 0xffff) * 4;
  iVar2 = *(int *)(&DAT_00143f80 + iVar4);
  uVar7 = FUN_000af230();
  FUN_000a1510(param_1,1);
  iVar10 = (param_2 & 0xffff) * 0x10;
  iVar3 = param_1 * 0x14;
  do {
    *(uint *)(&DAT_40009670 + iVar3) = (uint)*(ushort *)(iVar2 + iVar10 + 0x80);
    cVar9 = FUN_000a1560(param_1,1);
    if ((*(uint *)(&DAT_40009670 + iVar3) & 0x100) != 0x100) break;
  } while (cVar9 != '\0');
  FUN_000a1640(param_1,1);
  iVar10 = iVar2 + iVar10;
  *(undefined2 *)(&DAT_40009674 + iVar3) = *(undefined2 *)(iVar10 + 0x84);
  *(undefined2 *)(&DAT_40009676 + iVar3) = *(undefined2 *)(iVar10 + 0x86);
  *(undefined4 *)(&DAT_40009678 + iVar3) = *(undefined4 *)(iVar10 + 0x88);
  *(undefined4 *)(&DAT_4000967c + iVar3) = *(undefined4 *)(iVar10 + 0x8c);
  *(int *)(iVar2 + 0x30) = 1 << ((byte)param_2 & 0x3f);
  iVar10 = (param_1 & 0xffff) * 2;
  *(undefined2 *)(&DAT_40009680 + iVar3) =
       *(undefined2 *)((uint)*(ushort *)(&DAT_00143f98 + iVar10) * 0x10 + iVar2 + 0x82);
  FUN_000af240(uVar7);
  if (cVar9 != '\0') {
    iVar5 = (param_1 & 0xffff) * 0x10;
    puVar11 = &DAT_400095e8 + (param_1 & 0xffff) * 8;
    *(undefined **)(&DAT_400095ec + iVar5) = &DAT_40009670 + iVar3;
    *(undefined **)(&DAT_400095f0 + iVar5) = &DAT_40009678 + iVar3;
    *(undefined **)(&DAT_400096c0 + iVar4) = &DAT_40009678 + iVar3;
    *(undefined2 *)(&DAT_400095f4 + iVar5) = 0xffff;
    iVar2 = *(int *)(&DAT_400095ec + iVar5);
    if ((*(byte *)(iVar2 + 3) & 0x20) == 0x20) {
      uVar6 = *(uint *)(iVar2 + 4) & 0x3ffff00;
    }
    else {
      uVar6 = *(uint *)(iVar2 + 4) & 0x1ffc0000;
    }
    iVar3 = param_1 * 0x4c;
    uVar8 = *(ushort *)(&DAT_00143ce4 + iVar3);
    if ((((((uVar8 & 1) == 0) || ((*(byte *)(iVar2 + 3) & 0x20) != (&DAT_00143ce6)[iVar3])) ||
         ((uVar6 & ~*(uint *)(&DAT_00143cc4 + iVar3)) != *(uint *)(&DAT_00143cd4 + iVar3))) ||
        (cVar9 = (*(code *)((uint)(&PTR_LAB_00143ca8)[(uint)*puVar11 * 0x13] & 0xfffffffe))(puVar11)
        , cVar9 != '\0')) &&
       ((((uVar8 >> 3 & 1) == 0 ||
         ((*(byte *)(*(int *)(&DAT_400095ec + iVar5) + 3) & 0x20) != (&DAT_00143ce9)[iVar3])) ||
        (((uVar6 & ~*(uint *)(&DAT_00143cd0 + iVar3)) != *(uint *)(&DAT_00143ce0 + iVar3) ||
         (cVar9 = (*(code *)((uint)(&PTR_LAB_00143cb4)[(uint)*puVar11 * 0x13] & 0xfffffffe))
                            (puVar11), cVar9 != '\0')))))) {
      uVar8 = *(ushort *)(&DAT_00143e90 + iVar10);
      while ((uVar8 < *(ushort *)(&DAT_00143e9c + iVar10) &&
             ((uVar6 != *(uint *)(&DAT_00142c50 + (uint)uVar8 * 4) ||
              ((*(byte *)(*(int *)(&DAT_400095ec + iVar5) + 3) & 0x20) !=
               (*(byte *)((int)u__00143eb0 + uVar8 + 8) & 0x20)))))) {
        uVar8 = uVar8 + 1;
      }
      if (uVar8 < *(ushort *)(&DAT_00143e9c + iVar10)) {
        uVar1 = *(undefined2 *)(&DAT_00142f54 + (uint)uVar8 * 2);
        *(undefined2 *)(&DAT_400095f4 + iVar5) = uVar1;
        cVar9 = FUN_000a87e0(param_1);
        if (cVar9 == '\x01') {
          FUN_000a88c0(uVar1);
        }
      }
    }
  }
  return;
}

