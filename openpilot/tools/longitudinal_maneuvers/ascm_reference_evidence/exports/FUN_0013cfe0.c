
void FUN_0013cfe0(void)

{
  float fVar1;
  int iVar2;
  uint uVar3;
  uint uVar4;
  uint uVar5;
  float fVar7;
  float fVar8;
  float fVar9;
  float fVar10;
  float fVar11;
  float fVar12;
  undefined4 uVar13;
  char cVar14;
  undefined8 uVar6;
  undefined1 uVar15;
  float *pfVar16;
  float *pfVar17;
  float *pfVar18;
  uint uVar19;
  undefined4 *puVar20;
  undefined1 local_290 [8];
  undefined1 local_288 [20];
  undefined1 local_274 [20];
  undefined1 local_260 [20];
  undefined1 local_24c [20];
  undefined4 local_238 [20];
  float local_1e8 [20];
  float local_198 [20];
  float local_148 [20];
  undefined4 local_f8 [20];
  float local_a8 [42];
  
  if (*(char *)(DAT_40037a40 + 0x8d8) == '\0') {
    FUN_00045520(0x20);
    uVar6 = FUN_000c43d0();
    FUN_000bc1a0(local_290,uVar6,6);
    FUN_00045560(0x20);
    DAT_4001e491 = '\0';
    uVar19 = 0;
    do {
      if ((&DAT_4001e492)[uVar19 & 0xff] == -1) {
        FUN_0013d370(&DAT_4001e498 + (uVar19 & 0xff) * 0x10);
        if ((uVar19 & 0xff) == 0) {
          uVar15 = FUN_0013d510(local_290[0]);
          (&DAT_4001e4c2)[(uVar19 & 0xff) * 0x40] = uVar15;
        }
      }
      else {
        FUN_0013d3c0(&DAT_4001e498 + (uVar19 & 0xff) * 0x10,
                     &DAT_4001e1d4 + (char)(&DAT_4001e492)[uVar19 & 0xff] * 0xb);
        DAT_4001e491 = DAT_4001e491 + '\x01';
      }
      uVar19 = uVar19 + 1;
    } while (uVar19 < 6);
  }
  else {
    FUN_00045520(0x20);
    uVar6 = FUN_000c5030();
    FUN_000bc1a0(local_24c,uVar6,0x14);
    uVar6 = FUN_000c3970();
    FUN_000bc1a0(local_260,uVar6,0x14);
    uVar6 = FUN_000c3b50();
    FUN_000bc1a0(local_a8,uVar6,0x50);
    uVar6 = FUN_000c50d0();
    FUN_000bc1a0(local_f8,uVar6,0x50);
    uVar6 = FUN_000c3bf0();
    FUN_000bc1a0(local_148,uVar6,0x50);
    uVar6 = FUN_000c4c10();
    FUN_000bc1a0(local_198,uVar6,0x50);
    uVar6 = FUN_000c3a10();
    FUN_000bc1a0(local_1e8,uVar6,0x50);
    uVar6 = FUN_000c3ab0();
    FUN_000bc1a0(local_274,uVar6,0x14);
    uVar6 = FUN_000c5210();
    FUN_000bc1a0(local_238,uVar6,0x50);
    uVar6 = FUN_000c5170();
    FUN_000bc1a0(local_288,uVar6,0x14);
    FUN_00045560(0x20);
    DAT_4001e491 = '\0';
    uVar19 = 0;
    do {
      uVar4 = uVar19 & 0xff;
      iVar2 = uVar4 * 0x40;
      (&DAT_4001e4c3)[iVar2] = local_260[uVar19 & 0xff];
      uVar15 = FUN_0013d570(local_24c[uVar19 & 0xff]);
      (&DAT_4001e4d4)[iVar2] = uVar15;
      uVar5 = uVar19 & 0xff;
      puVar20 = local_f8 + uVar5;
      pfVar18 = local_a8 + uVar5;
      fVar7 = (float)FUN_0013d8b0(*puVar20);
      (&DAT_4001e498)[uVar4 * 0x10] = *pfVar18 * fVar7;
      fVar7 = (float)FUN_0013da20(*puVar20);
      (&DAT_4001e49c)[uVar4 * 0x10] = *(float *)(DAT_40037a40 + 0x8dc) + *pfVar18 * fVar7;
      pfVar17 = local_198 + uVar5;
      pfVar16 = local_148 + uVar5;
      fVar8 = (float)FUN_0013da20(*puVar20);
      fVar7 = *pfVar17;
      fVar1 = *pfVar18;
      fVar9 = (float)FUN_0013d8b0(*puVar20);
      (&DAT_4001e4a0)[uVar4 * 0x10] = *pfVar16 * fVar9 - fVar1 * fVar7 * fVar8;
      fVar8 = (float)FUN_0013d8b0(*puVar20);
      fVar7 = *pfVar17;
      fVar1 = *pfVar18;
      fVar9 = (float)FUN_0013da20(*puVar20);
      (&DAT_4001e4a4)[uVar4 * 0x10] = *pfVar16 * fVar9 + fVar1 * fVar7 * fVar8;
      fVar10 = (float)FUN_0013d8b0(*puVar20);
      fVar7 = *pfVar18;
      fVar1 = *pfVar17;
      fVar11 = (float)FUN_0013da20(*puVar20);
      fVar8 = *pfVar17;
      fVar9 = *pfVar16;
      fVar12 = (float)FUN_0013d8b0(*puVar20);
      fVar7 = (local_1e8[uVar5] * fVar12 - fVar9 * 2.0 * fVar8 * fVar11) -
              fVar1 * fVar1 * fVar7 * fVar10;
      (&DAT_4001e4a8)[uVar4 * 0x10] = fVar7;
      (&DAT_4001e4ac)[uVar4 * 0x10] = 0;
      (&DAT_4001e4b0)[uVar4 * 0x10] = DAT_4001e478 + (float)(&DAT_4001e4a0)[uVar4 * 0x10];
      (&DAT_4001e4b4)[uVar4 * 0x10] = DAT_4001e47c + fVar7;
      (&DAT_4001e4b8)[uVar4 * 0x10] = 0;
      uVar13 = FUN_0013d5e0((&DAT_4001e498)[uVar4 * 0x10],(&DAT_4001e49c)[uVar4 * 0x10],DAT_4001e470
                           );
      (&DAT_4001e4bc)[uVar4 * 0x10] = uVar13;
      cVar14 = FUN_0013d4b0(local_274[uVar19 & 0xff]);
      (&DAT_4001e4c0)[iVar2] = cVar14;
      if (cVar14 != '\0') {
        DAT_4001e491 = DAT_4001e491 + '\x01';
      }
      uVar3 = uVar19 & 0xff;
      if (uVar3 < 2) {
        (&DAT_4001e4c1)[iVar2] = 1;
      }
      else if ((uVar3 == 2) || (uVar3 == 4)) {
        (&DAT_4001e4c1)[iVar2] = 3;
      }
      else {
        (&DAT_4001e4c1)[iVar2] = 2;
      }
      (&DAT_4001e4c2)[iVar2] = 0;
      (&DAT_4001e4c8)[uVar4 * 0x10] = local_238[uVar5];
      (&DAT_4001e4cc)[uVar4 * 0x10] = 0;
      uVar13 = FUN_0013d530(local_288[uVar19 & 0xff]);
      (&DAT_4001e4d0)[uVar4 * 0x10] = uVar13;
      (&DAT_4001e4d5)[iVar2] = 0;
      (&DAT_4001e4d6)[iVar2] = 0;
      (&DAT_4001e4c4)[iVar2] = 0;
      (&DAT_4001e4d7)[iVar2] = 0;
      uVar19 = uVar19 + 1;
    } while (uVar19 < 6);
  }
  FUN_00045520(0x17);
  FUN_000c2b80(&DAT_4001e498);
  FUN_000c2c30(DAT_4001e490);
  FUN_000c2c50(DAT_4001e491);
  FUN_000c2c60(DAT_4001e488);
  DAT_4001e488 = DAT_4001e488 + 1 & 3;
  FUN_00045560(0x17);
  return;
}

