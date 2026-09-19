
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void FUN_000b3380(void)

{
  int iVar1;
  uint uVar2;
  char cVar4;
  uint uVar3;
  longlong lVar5;
  char local_20 [32];
  
  cVar4 = FUN_000b5770(8,local_20,1);
  if ((cVar4 == '\0') && (local_20[0] == 'Z')) {
    DAT_4000a168 = 1;
    DAT_400377b4 = 1;
    uVar3 = 0x116;
    lVar5 = 10;
    do {
      iVar1 = (uVar3 & 0xffff) * 2;
      *(ushort *)(iVar1 + -0x3c06ffc0) = *(ushort *)(iVar1 + -0x3c06ffc0) & 0xe3ff | 0x400;
      *(ushort *)(iVar1 + -0x3c06ffc0) = *(ushort *)(iVar1 + -0x3c06ffc0) | 0x200;
      *(ushort *)(iVar1 + -0x3c06ffc0) = *(ushort *)(iVar1 + -0x3c06ffc0) & 0xfc7f;
      *(ushort *)(iVar1 + -0x3c06ffc0) = *(ushort *)(iVar1 + -0x3c06ffc0) | 0xc0;
      *(ushort *)(iVar1 + -0x3c06ffc0) = *(ushort *)(iVar1 + -0x3c06ffc0) & 0xff8f;
      *(ushort *)(iVar1 + -0x3c06ffc0) = *(ushort *)(iVar1 + -0x3c06ffc0) & 0xffc7;
      *(ushort *)(iVar1 + -0x3c06ffc0) = *(ushort *)(iVar1 + -0x3c06ffc0) & 0xffe1;
      *(ushort *)(iVar1 + -0x3c06ffc0) = *(ushort *)(iVar1 + -0x3c06ffc0) & 0xfff8;
      *(ushort *)(iVar1 + -0x3c06ffc0) = *(ushort *)(iVar1 + -0x3c06ffc0) & 0xfffe;
      uVar2 = (uVar3 + 1) * 2 & 0x1fffe;
      *(ushort *)(uVar2 + 0xc3f90040) = *(ushort *)(uVar2 + 0xc3f90040) & 0xe3ff | 0x400;
      *(ushort *)(uVar2 + 0xc3f90040) = *(ushort *)(uVar2 + 0xc3f90040) | 0x200;
      *(ushort *)(uVar2 + 0xc3f90040) = *(ushort *)(uVar2 + 0xc3f90040) & 0xfc7f;
      *(ushort *)(uVar2 + 0xc3f90040) = *(ushort *)(uVar2 + 0xc3f90040) | 0xc0;
      *(ushort *)(uVar2 + 0xc3f90040) = *(ushort *)(uVar2 + 0xc3f90040) & 0xff8f;
      *(ushort *)(uVar2 + 0xc3f90040) = *(ushort *)(uVar2 + 0xc3f90040) & 0xffc7;
      *(ushort *)(uVar2 + 0xc3f90040) = *(ushort *)(uVar2 + 0xc3f90040) & 0xffe1;
      *(ushort *)(uVar2 + 0xc3f90040) = *(ushort *)(uVar2 + 0xc3f90040) & 0xfff8;
      *(ushort *)(uVar2 + 0xc3f90040) = *(ushort *)(uVar2 + 0xc3f90040) & 0xfffe;
      uVar3 = uVar3 + 2;
      lVar5 = lVar5 + -1;
    } while (lVar5 != 0);
    _DAT_c3f9020a = (_DAT_c3f9020a & 0xc07f | 0xc0) & 0xff80;
    DAT_4000a174 = 0x14;
    DAT_4000a178 = 0;
    DAT_4000a17a = 0;
    DAT_4000a17b = 4;
    DAT_4000a180 = 200;
    DAT_4000a182 = 0x11;
    DAT_4000a1ae = 0;
    DAT_4000a1ad = 0;
    DAT_4000a161 = 0;
  }
  return;
}

