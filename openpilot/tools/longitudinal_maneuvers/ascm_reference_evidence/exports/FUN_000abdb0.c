
void FUN_000abdb0(int param_1)

{
  undefined1 uVar1;
  undefined1 uVar2;
  int iVar3;
  byte bVar4;
  int iVar5;
  uint uVar6;
  ushort uVar7;
  byte bVar8;
  
  (&DAT_40009888)[param_1] = 0;
  bVar4 = (&DAT_001462fd)[param_1];
  for (bVar8 = (&DAT_001462fc)[param_1]; bVar8 < bVar4; bVar8 = bVar8 + 1) {
    iVar3 = *(int *)(&DAT_0014319c + (uint)bVar8 * 4);
    if (iVar3 != 0) {
      if ((&PTR_DAT_00146008)[bVar8] == (undefined *)0x0) {
        FUN_000aeff0(iVar3,(&DAT_001430d8)[bVar8]);
      }
      else {
        FUN_000af120(iVar3,(&PTR_DAT_00146008)[bVar8],(&DAT_001430d8)[bVar8]);
      }
    }
  }
  FUN_000acc50(param_1);
  FUN_000aeff0(&DAT_4000988c + (byte)(&DAT_00146328)[param_1],
               (uint)(byte)(&DAT_00146329)[param_1] - (uint)(byte)(&DAT_00146328)[param_1] & 0xff);
  FUN_000aeff0(&DAT_40009898 + (byte)(&DAT_00146310)[param_1],
               (uint)(byte)(&DAT_00146311)[param_1] - (uint)(byte)(&DAT_00146310)[param_1] & 0xff);
  bVar4 = (&DAT_001462f5)[param_1];
  for (bVar8 = (&DAT_001462f4)[param_1]; bVar8 < bVar4; bVar8 = bVar8 + 1) {
    iVar5 = (uint)bVar8 * 2;
    uVar7 = *(ushort *)(&LAB_00146330 + iVar5);
    iVar3 = *(int *)(&DAT_00142770 + (uint)uVar7 * 4);
    if (iVar3 != 0) {
      if (*(int *)(&DAT_00145ed8 + (uint)bVar8 * 4) == 0) {
        FUN_000aeff0(iVar3,(&DAT_0014271c)[uVar7] & 0xf);
      }
      else {
        FUN_000af120(iVar3,*(int *)(&DAT_00145ed8 + (uint)bVar8 * 4),(&DAT_0014271c)[uVar7] & 0xf);
      }
    }
    (&DAT_400097a0)[bVar8] = 0;
    *(undefined2 *)(&DAT_400097f0 + iVar5) = 0;
    *(undefined2 *)(&DAT_400098a0 + iVar5) = 0;
  }
  bVar8 = (&DAT_00144ff0)[param_1];
  uVar7 = (ushort)(byte)(&DAT_00144ff1)[param_1] - (ushort)bVar8;
  FUN_000aeff0(&DAT_40009938 + bVar8,uVar7 & 0xff);
  FUN_000aeff0(&DAT_40009954 + bVar8,uVar7 & 0xff);
  uVar1 = (&DAT_00144fe9)[param_1];
  uVar2 = (&DAT_00144fe8)[param_1];
  FUN_000abd10(&DAT_40009970,uVar2,uVar1);
  FUN_000abd10(&DAT_40009974,uVar2,uVar1);
  FUN_000af120(&DAT_40009978 + bVar8,&UNK_0000c438 + bVar8,uVar7);
  (&DAT_40009994)[param_1] = 0;
  iVar3 = param_1 * 0x22;
  FUN_000aeff0(&DAT_40009998 + iVar3,0x20);
  (&DAT_400099b8)[iVar3] = 0xfe;
  (&DAT_400099b9)[iVar3] = 0xff;
  FUN_000aeff0(&DAT_40009a20 + iVar3,0x22);
  FUN_000aeff0(param_1 * 10 + 0x40009aa8,10);
  FUN_000aeff0(param_1 * 10 + 0x40009ad0,10);
  (&DAT_40009af8)[param_1] = 0;
  uVar6 = (uint)(byte)(&DAT_00144fe0)[param_1];
  FUN_000af120(&DAT_40009b00 + uVar6,uVar6 + 0x144fb8,
               (byte)(&DAT_00144fe1)[param_1] - uVar6 & 0xffff);
  FUN_000abd10(&DAT_40009b28,uVar2,uVar1);
  bVar8 = (&DAT_00144ff8)[param_1];
  bVar4 = (&DAT_00144ff9)[param_1];
  FUN_000aeff0(&DAT_40009b2c + bVar8,(ushort)bVar4 - (ushort)bVar8 & 0xff);
  FUN_000af120(&DAT_40009b38 + bVar8,&UNK_0000c454 + bVar8,(ushort)bVar4 - (ushort)bVar8);
  FUN_000a9ce0(param_1);
  return;
}

