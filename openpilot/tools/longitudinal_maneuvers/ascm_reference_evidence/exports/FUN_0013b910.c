
void FUN_0013b910(int param_1,int param_2,int param_3)

{
  byte bVar1;
  short sVar5;
  short sVar6;
  int iVar3;
  undefined2 uVar7;
  undefined4 uVar4;
  undefined8 uVar2;
  undefined1 uVar8;
  ushort uVar9;
  uint uVar10;
  int iVar11;
  uint uVar12;
  longlong lVar13;
  int iVar14;
  longlong lVar15;
  
  uVar9 = *(short *)(param_3 + 0x280) + (short)param_1;
  *(ushort *)(param_3 + 0x280) = uVar9;
  *(int *)(param_3 + 0x284) = *(short *)(param_3 + 0xea) * param_1 + *(int *)(param_3 + 0x284);
  *(int *)(param_3 + 0x288) = *(short *)(param_2 + 4) * param_1 + *(int *)(param_3 + 0x288);
  if (99 < uVar9) {
    bVar1 = *(char *)(param_3 + 0x27e) + 1;
    *(byte *)(param_3 + 0x27e) = bVar1;
    if (99 < bVar1) {
      *(undefined1 *)(param_3 + 0x27e) = 0;
    }
    *(short *)((uint)*(byte *)(param_3 + 0x27e) * 2 + param_3 + 0xee) =
         (short)(*(int *)(param_3 + 0x284) / (int)(uint)*(ushort *)(param_3 + 0x280));
    *(short *)((uint)*(byte *)(param_3 + 0x27e) * 2 + param_3 + 0x1b6) =
         (short)(*(int *)(param_3 + 0x288) / (int)(uint)*(ushort *)(param_3 + 0x280));
    *(undefined4 *)(param_3 + 0x284) = 0;
    *(undefined4 *)(param_3 + 0x288) = 0;
    *(undefined2 *)(param_3 + 0x280) = 0;
  }
  sVar5 = FUN_0013a570(3000,100,param_3 + 0xee,*(undefined1 *)(param_3 + 0x27e),100);
  sVar6 = FUN_0013a570(0,100,param_3 + 0xee,*(undefined1 *)(param_3 + 0x27e),100);
  iVar11 = ((int)sVar6 - (int)sVar5) * 1000;
  lVar15 = 0;
  lVar13 = 0;
  uVar10 = 0;
  uVar12 = 0;
  do {
    uVar10 = uVar10 + 1;
    sVar5 = FUN_0013a570(uVar12 & 0xffff,100,param_3 + 0xee,*(undefined1 *)(param_3 + 0x27e),100);
    lVar15 = lVar15 + sVar5;
    sVar5 = FUN_0013a570(uVar12 & 0xffff,100,param_3 + 0x1b6,*(undefined1 *)(param_3 + 0x27e),100);
    lVar13 = lVar13 + sVar5;
    uVar12 = uVar12 + 100;
  } while (uVar12 < 3000);
  uVar10 = uVar10 & 0xff;
  if (uVar10 != 0) {
    lVar15 = (longlong)((int)lVar15 / (int)uVar10);
    lVar13 = (longlong)((int)lVar13 / (int)uVar10);
  }
  iVar14 = 0;
  uVar10 = 0;
  do {
    sVar5 = FUN_0013a570(uVar10 & 0xffff,100,param_3 + 0xee,*(undefined1 *)(param_3 + 0x27e),100);
    sVar6 = FUN_0013a570(uVar10 & 0xffff,100,param_3 + 0x1b6,*(undefined1 *)(param_3 + 0x27e),100);
    iVar3 = FUN_0012e610(((longlong)sVar5 - (longlong)sVar6) - (lVar15 - lVar13));
    iVar14 = iVar14 + iVar3;
    uVar10 = uVar10 + 100;
  } while (uVar10 < 3000);
  uVar10 = iVar14 * 100;
  uVar7 = FUN_0012e5a0((ulonglong)(uVar10 >> 0x1f) +
                       (longlong)((int)uVar10 / 3000 + ((int)uVar10 >> 0x1f)),0xffffffffffff8001,
                       0x7ffe);
  *(undefined2 *)(param_3 + 0x290) = uVar7;
  uVar10 = (short)(((short)(iVar11 / 3000) + (short)(iVar11 >> 0x1f)) -
                  (short)((longlong)iVar11 * 0x57619f1 >> 0x3f)) * 1000;
  uVar4 = FUN_0012e5a0((ulonglong)(uVar10 >> 0x1f) +
                       (longlong)((int)uVar10 / 3000 + ((int)uVar10 >> 0x1f)),0xffffffffffff8001,
                       0x7ffe);
  *(undefined4 *)(param_3 + 0x28c) = uVar4;
  iVar11 = FUN_0012e610();
  uVar2 = FUN_0012e5a0(((longlong)*(short *)(param_3 + 0x290) + -100) -
                       (ulonglong)(uint)(iVar11 << 1),0,100);
  uVar8 = FUN_0012e5e0(uVar2,*(undefined1 *)(param_3 + 0x292),200 / param_1);
  *(undefined1 *)(param_3 + 0x292) = uVar8;
  return;
}

