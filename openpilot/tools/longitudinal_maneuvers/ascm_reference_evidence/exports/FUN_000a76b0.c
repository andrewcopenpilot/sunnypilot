
void FUN_000a76b0(uint param_1,short param_2)

{
  char cVar1;
  ushort uVar2;
  ushort uVar3;
  ushort uVar4;
  wchar_t wVar5;
  ushort uVar6;
  ushort *puVar7;
  uint uVar8;
  uint uVar9;
  uint uVar10;
  uint uVar11;
  uint uVar12;
  int iVar13;
  int iVar14;
  int iVar15;
  ushort uVar16;
  char cVar19;
  uint uVar17;
  ushort *puVar18;
  longlong lVar20;
  ulonglong uVar21;
  uint uVar22;
  uint uVar23;
  uint *puVar24;
  uint *puVar25;
  uint uVar26;
  uint uVar27;
  uint *puVar28;
  uint uVar29;
  uint uVar30;
  uint uVar31;
  
  uVar16 = (ushort)*(byte *)((int)&PTR_DAT_00143c30 + param_1) + param_2;
  iVar14 = (param_1 & 0xffff) * 4;
  puVar7 = *(ushort **)(&DAT_00143f80 + iVar14);
  uVar31 = 0;
  puVar28 = (uint *)(&DAT_40009540 + iVar14);
  *puVar28 = 0;
  puVar25 = (uint *)(&DAT_40009550 + iVar14);
  *puVar25 = 0;
  puVar24 = (uint *)(&DAT_40009560 + iVar14);
  *puVar24 = 0;
  *puVar7 = *puVar7 | 0x8000;
  puVar7[3] = puVar7[3] & 0xdfff;
  iVar13 = (uint)uVar16 * 4;
  cVar1 = (&DAT_00143c38)[iVar13];
  if (cVar1 != '\0') {
    puVar7[3] = puVar7[3] | 0x2000;
  }
  *puVar7 = *puVar7 & 0x7fff;
  *puVar7 = 0x200;
  FUN_000a1510(param_1,0);
  do {
    cVar19 = FUN_000a1560(param_1,0);
    if ((*puVar7 & 0x200) != 0x200) break;
  } while (cVar19 != '\0');
  FUN_000a1640(param_1,0);
  puVar7[0x40] = 0;
  puVar7[0x41] = 0;
  puVar7[0x48] = 0;
  puVar7[0x49] = 0;
  puVar7[0x50] = 0;
  puVar7[0x51] = 0;
  puVar7[0x58] = 0;
  puVar7[0x59] = 0;
  puVar7[0x60] = 0;
  puVar7[0x61] = 0;
  puVar7[0x68] = 0;
  puVar7[0x69] = 0;
  puVar7[0x70] = 0;
  puVar7[0x71] = 0;
  puVar7[0x78] = 0;
  puVar7[0x79] = 0;
  puVar7[0x80] = 0;
  puVar7[0x81] = 0;
  puVar7[0x88] = 0;
  puVar7[0x89] = 0;
  puVar7[0x90] = 0;
  puVar7[0x91] = 0;
  puVar7[0x98] = 0;
  puVar7[0x99] = 0;
  puVar7[0xa0] = 0;
  puVar7[0xa1] = 0;
  puVar7[0xa8] = 0;
  puVar7[0xa9] = 0;
  puVar7[0xb0] = 0;
  puVar7[0xb1] = 0;
  puVar7[0xb8] = 0;
  puVar7[0xb9] = 0;
  puVar7[0xc0] = 0;
  puVar7[0xc1] = 0;
  puVar7[200] = 0;
  puVar7[0xc9] = 0;
  puVar7[0xd0] = 0;
  puVar7[0xd1] = 0;
  puVar7[0xd8] = 0;
  puVar7[0xd9] = 0;
  puVar7[0xe0] = 0;
  puVar7[0xe1] = 0;
  puVar7[0xe8] = 0;
  puVar7[0xe9] = 0;
  puVar7[0xf0] = 0;
  puVar7[0xf1] = 0;
  puVar7[0xf8] = 0;
  puVar7[0xf9] = 0;
  puVar7[0x100] = 0;
  puVar7[0x101] = 0;
  puVar7[0x108] = 0;
  puVar7[0x109] = 0;
  puVar7[0x110] = 0;
  puVar7[0x111] = 0;
  puVar7[0x118] = 0;
  puVar7[0x119] = 0;
  puVar7[0x120] = 0;
  puVar7[0x121] = 0;
  puVar7[0x128] = 0;
  puVar7[0x129] = 0;
  puVar7[0x130] = 0;
  puVar7[0x131] = 0;
  puVar7[0x138] = 0;
  puVar7[0x139] = 0;
  iVar15 = (param_1 & 0xffff) * 2;
  uVar2 = *(ushort *)(&DAT_00143ea8 + iVar15);
  uVar27 = (uint)uVar2;
  uVar3 = *(ushort *)(&DAT_00143fc0 + iVar15);
  if (uVar2 < uVar3) {
    uVar23 = uVar27;
    if (((8 < (ushort)(uVar3 - uVar2)) && (uVar2 <= uVar3)) &&
       (uVar30 = uVar3 + 0xfff8 & 0xffff, uVar21 = (ulonglong)((uVar30 + 7) - (uint)uVar2 >> 3),
       uVar2 < uVar30)) {
      do {
        uVar30 = uVar23 & 0xffff;
        (puVar7 + uVar30 * 8 + 0x40)[0] = 0x400;
        (puVar7 + uVar30 * 8 + 0x40)[1] = 0;
        (puVar7 + uVar30 * 8 + 0x48)[0] = 0x400;
        (puVar7 + uVar30 * 8 + 0x48)[1] = 0;
        (puVar7 + uVar30 * 8 + 0x50)[0] = 0x400;
        (puVar7 + uVar30 * 8 + 0x50)[1] = 0;
        (puVar7 + uVar30 * 8 + 0x58)[0] = 0x400;
        (puVar7 + uVar30 * 8 + 0x58)[1] = 0;
        (puVar7 + uVar30 * 8 + 0x60)[0] = 0x400;
        (puVar7 + uVar30 * 8 + 0x60)[1] = 0;
        (puVar7 + uVar30 * 8 + 0x68)[0] = 0x400;
        (puVar7 + uVar30 * 8 + 0x68)[1] = 0;
        (puVar7 + uVar30 * 8 + 0x70)[0] = 0x400;
        (puVar7 + uVar30 * 8 + 0x70)[1] = 0;
        (puVar7 + uVar30 * 8 + 0x78)[0] = 0x400;
        (puVar7 + uVar30 * 8 + 0x78)[1] = 0;
        uVar23 = uVar23 + 8;
        uVar21 = uVar21 - 1;
      } while (uVar21 != 0);
    }
    for (; (uVar23 & 0xffff) < (uint)uVar3; uVar23 = uVar23 + 1) {
      (puVar7 + (uVar23 & 0xffff) * 8 + 0x40)[0] = 0x400;
      (puVar7 + (uVar23 & 0xffff) * 8 + 0x40)[1] = 0;
    }
  }
  uVar2 = *(ushort *)(&DAT_00143fb8 + iVar15);
  uVar29 = (uint)uVar2;
  uVar4 = *(ushort *)(&DAT_00143fa0 + iVar15);
  uVar23 = (uint)uVar4;
  uVar30 = (uint)uVar2;
  if (uVar2 < uVar4) {
    uVar26 = uVar29;
    if (((8 < (ushort)(uVar4 - uVar2)) && (uVar2 <= uVar4)) &&
       (uVar17 = uVar4 + 0xfff8 & 0xffff, uVar21 = (ulonglong)((uVar17 + 7) - (uint)uVar2 >> 3),
       uVar30 < uVar17)) {
      do {
        uVar17 = uVar26 & 0xffff;
        (puVar7 + uVar17 * 8 + 0x40)[0] = 0x400;
        (puVar7 + uVar17 * 8 + 0x40)[1] = 0;
        (puVar7 + uVar17 * 8 + 0x48)[0] = 0x400;
        (puVar7 + uVar17 * 8 + 0x48)[1] = 0;
        (puVar7 + uVar17 * 8 + 0x50)[0] = 0x400;
        (puVar7 + uVar17 * 8 + 0x50)[1] = 0;
        (puVar7 + uVar17 * 8 + 0x58)[0] = 0x400;
        (puVar7 + uVar17 * 8 + 0x58)[1] = 0;
        (puVar7 + uVar17 * 8 + 0x60)[0] = 0x400;
        (puVar7 + uVar17 * 8 + 0x60)[1] = 0;
        (puVar7 + uVar17 * 8 + 0x68)[0] = 0x400;
        (puVar7 + uVar17 * 8 + 0x68)[1] = 0;
        (puVar7 + uVar17 * 8 + 0x70)[0] = 0x400;
        (puVar7 + uVar17 * 8 + 0x70)[1] = 0;
        (puVar7 + uVar17 * 8 + 0x78)[0] = 0x400;
        (puVar7 + uVar17 * 8 + 0x78)[1] = 0;
        uVar26 = uVar26 + 8;
        uVar21 = uVar21 - 1;
      } while (uVar21 != 0);
    }
    for (; (uVar26 & 0xffff) < uVar23; uVar26 = uVar26 + 1) {
      (puVar7 + (uVar26 & 0xffff) * 8 + 0x40)[0] = 0x400;
      (puVar7 + (uVar26 & 0xffff) * 8 + 0x40)[1] = 0;
    }
  }
  uVar4 = *(ushort *)(&DAT_00143f90 + iVar15);
  uVar26 = (uint)uVar4;
  if (uVar4 < 0x20) {
    uVar17 = uVar26;
    if (((8 < (ushort)(0x20 - uVar4)) && (uVar4 < 0x21)) &&
       (uVar21 = (ulonglong)(0x1f - uVar4 >> 3), uVar4 < 0x18)) {
      do {
        uVar22 = uVar17 & 0xffff;
        (puVar7 + uVar22 * 8 + 0x40)[0] = 0x820;
        (puVar7 + uVar22 * 8 + 0x40)[1] = 0;
        (puVar7 + uVar22 * 8 + 0x48)[0] = 0x820;
        (puVar7 + uVar22 * 8 + 0x48)[1] = 0;
        (puVar7 + uVar22 * 8 + 0x50)[0] = 0x820;
        (puVar7 + uVar22 * 8 + 0x50)[1] = 0;
        (puVar7 + uVar22 * 8 + 0x58)[0] = 0x820;
        (puVar7 + uVar22 * 8 + 0x58)[1] = 0;
        (puVar7 + uVar22 * 8 + 0x60)[0] = 0x820;
        (puVar7 + uVar22 * 8 + 0x60)[1] = 0;
        (puVar7 + uVar22 * 8 + 0x68)[0] = 0x820;
        (puVar7 + uVar22 * 8 + 0x68)[1] = 0;
        (puVar7 + uVar22 * 8 + 0x70)[0] = 0x820;
        (puVar7 + uVar22 * 8 + 0x70)[1] = 0;
        (puVar7 + uVar22 * 8 + 0x78)[0] = 0x820;
        (puVar7 + uVar22 * 8 + 0x78)[1] = 0;
        uVar17 = uVar17 + 8;
        uVar21 = uVar21 - 1;
      } while (uVar21 != 0);
    }
    lVar20 = 0x20 - (ulonglong)(uVar17 & 0xffff);
    if ((ushort)uVar17 < 0x20) {
      do {
        (puVar7 + (uVar17 & 0xffff) * 8 + 0x40)[0] = 0x820;
        (puVar7 + (uVar17 & 0xffff) * 8 + 0x40)[1] = 0;
        uVar17 = uVar17 + 1;
        lVar20 = lVar20 + -1;
      } while (lVar20 != 0);
    }
  }
  puVar7[1] = 0x1f;
  *puVar7 = *puVar7 & 0xd910;
  *puVar7 = *puVar7 | 1;
  *puVar7 = *puVar7 | 2;
  puVar7[3] = CONCAT11(cVar1,(&DAT_00143c39)[iVar13]);
  puVar7[2] = CONCAT11((&DAT_00143c3b)[iVar13],(&DAT_00143c3a)[iVar13]);
  puVar7[3] = puVar7[3] | 0x40;
  wVar5 = u__00143eb0[param_1 & 0xffff];
  iVar13 = *(int *)(&DAT_00143fa8 + iVar14);
  for (; (uVar26 & 0xffff) < (uint)(ushort)wVar5; uVar26 = uVar26 + 1) {
    if ((((&DAT_40009570)[param_1] & 4) == 4) &&
       (*(ushort *)(&DAT_40009578 + (iVar13 + uVar26 & 0xffff) * 2) < 0x53)) {
      (*(code *)((uint)(&PTR_LAB_00143cbc)[param_1 * 0x13] & 0xfffffffe))();
    }
    *(undefined2 *)(&DAT_40009578 + (iVar13 + uVar26 & 0xffff) * 2) = 0xffff;
    uVar17 = 1 << ((byte)uVar26 & 0x3f);
    *puVar25 = *puVar25 | uVar17;
    uVar31 = uVar31 | uVar17;
    (puVar7 + (uVar26 & 0xffff) * 8 + 0x40)[0] = 0x820;
    (puVar7 + (uVar26 & 0xffff) * 8 + 0x40)[1] = 0;
  }
  uVar4 = *(ushort *)(&DAT_00143ea8 + iVar15);
  uVar6 = *(ushort *)(&DAT_00143e9c + iVar15);
  for (uVar26 = uVar27; (uVar26 & 0xffff) < (uint)uVar3; uVar26 = uVar26 + 1) {
    uVar22 = (uVar26 - uVar4) + (uint)uVar6;
    uVar17 = 1 << (uVar26 & 0x3f);
    *puVar24 = *puVar24 | uVar17;
    uVar31 = uVar31 | uVar17;
    *(undefined4 *)(puVar7 + (uVar26 & 0xffff) * 8 + 0x42) =
         *(undefined4 *)(&DAT_00142c50 + (uVar22 * 4 & 0x3fffc));
    *(uint *)(puVar7 + (uVar26 & 0xffff) * 8 + 0x40) =
         (*(byte *)((int)u__00143eb0 + (uVar22 & 0xffff) + 8) & 0x20) << 0x10 | 0x4000000;
  }
  if (uVar30 < uVar23) {
    uVar26 = uVar29;
    if (((8 < (ushort)(*(ushort *)(&DAT_00143fa0 + iVar15) - uVar2)) && (uVar30 <= uVar23)) &&
       (uVar17 = *(ushort *)(&DAT_00143fa0 + iVar15) + 0xfff8 & 0xffff,
       uVar21 = (ulonglong)((uVar17 + 7) - (uint)uVar2 >> 3), uVar30 < uVar17)) {
      do {
        uVar30 = 1 << (uVar26 & 0x3f);
        uVar17 = 1 << (uVar26 + 1 & 0x3f);
        uVar22 = 1 << (uVar26 + 2 & 0x3f);
        uVar8 = 1 << (uVar26 + 3 & 0x3f);
        uVar9 = 1 << (uVar26 + 4 & 0x3f);
        uVar10 = 1 << (uVar26 + 5 & 0x3f);
        uVar11 = 1 << (uVar26 + 6 & 0x3f);
        uVar12 = 1 << (uVar26 + 7 & 0x3f);
        *puVar28 = *puVar28 | uVar30 | uVar17 | uVar22 | uVar8 | uVar9 | uVar10 | uVar11 | uVar12;
        uVar31 = uVar31 | uVar30 | uVar17 | uVar22 | uVar8 | uVar9 | uVar10 | uVar11 | uVar12;
        uVar26 = uVar26 + 8;
        uVar21 = uVar21 - 1;
      } while (uVar21 != 0);
    }
    for (; (uVar26 & 0xffff) < uVar23; uVar26 = uVar26 + 1) {
      uVar30 = 1 << (uVar26 & 0x3f);
      *puVar28 = *puVar28 | uVar30;
      uVar31 = uVar31 | uVar30;
    }
  }
  uVar2 = *(ushort *)(&DAT_00143fa0 + iVar15);
  uVar3 = *(ushort *)(&DAT_00143fb8 + iVar15);
  for (; (uVar29 & 0xffff) < (uint)uVar2; uVar29 = uVar29 + 1) {
    puVar18 = (ushort *)(((uVar29 - uVar3) * 4 & 0x3f8) + (uint)uVar16 * 0x10 + 0x143c50);
    *(uint *)(puVar7 + (uVar29 & 0xffff) * 2 + 0x440) =
         (*puVar18 & 0x1fff) << 0x10 | (uint)puVar18[1];
    uVar23 = uVar29 & 0xffff;
    uVar4 = puVar18[2];
    *(uint *)(puVar7 + uVar23 * 8 + 0x42) = (uVar4 & 0x1fff) << 0x10;
    *(uint *)(puVar7 + uVar23 * 8 + 0x42) = (uint)puVar18[3] | *(uint *)(puVar7 + uVar23 * 8 + 0x42)
    ;
    *(uint *)(puVar7 + uVar23 * 8 + 0x40) = *(uint *)(puVar7 + uVar23 * 8 + 0x40) & 0xff000000;
    if ((short)uVar4 < 0) {
      *(uint *)(puVar7 + uVar23 * 8 + 0x40) = *(uint *)(puVar7 + uVar23 * 8 + 0x40) | 0x200000;
    }
  }
  uVar16 = *(ushort *)(&DAT_00143fc0 + iVar15);
  for (; (uVar27 & 0xffff) < (uint)uVar16; uVar27 = uVar27 + 1) {
    if ((*(uint *)(puVar7 + (uVar27 & 0xffff) * 8 + 0x40) & 0x200000) == 0) {
      (puVar7 + (uVar27 & 0xffff) * 2 + 0x440)[0] = 0x1ffc;
      (puVar7 + (uVar27 & 0xffff) * 2 + 0x440)[1] = 0;
    }
    else {
      (puVar7 + (uVar27 & 0xffff) * 2 + 0x440)[0] = 0x3ff;
      (puVar7 + (uVar27 & 0xffff) * 2 + 0x440)[1] = 0xff00;
    }
  }
  puVar7[0x18] = 0xffff;
  puVar7[0x19] = 0xffff;
  puVar7[0x10] = 0;
  puVar7[0x11] = 7;
  FUN_000af230();
  if ((&DAT_40009580)[param_1 & 0xffff] == 0) {
    puVar7[3] = puVar7[3] | 0x8000;
    *(uint *)(puVar7 + 0x14) = uVar31;
  }
  FUN_000af240();
  *puVar7 = *puVar7 & 0x7fff;
  *puVar7 = *puVar7 & 0xefff;
  *puVar7 = *puVar7 & 0xbfff;
  return;
}

