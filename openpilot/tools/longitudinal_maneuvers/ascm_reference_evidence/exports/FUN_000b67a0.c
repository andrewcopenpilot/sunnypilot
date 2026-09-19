
undefined8 FUN_000b67a0(undefined8 param_1,undefined8 param_2,int param_3)

{
  int iVar1;
  char cVar4;
  undefined8 uVar2;
  uint uVar3;
  short local_a0 [5];
  undefined2 local_96;
  undefined2 local_94;
  undefined2 local_92;
  undefined1 auStack_90 [144];
  
  DAT_4000ac78 = DAT_4000ac78 + 1;
  local_96 = (undefined2)param_1;
  local_94 = 0;
  local_92 = 0;
  FUN_000bc320(auStack_90,0,99);
  cVar4 = FUN_000b4ef0();
  if (cVar4 == '\x01') {
    if ((uint)param_1 < 0xa8) {
      if ((int)param_2 == 0) {
        uVar2 = 4;
      }
      else {
        iVar1 = ((uint)param_1 & 0xffff) * 0x10;
        if ((*(ushort *)(&DAT_0014df7c + iVar1) >> 4 & 1) == 0) {
          cVar4 = FUN_000b6700(param_1);
          if ((cVar4 == '\0') ||
             ((*(short *)(&DAT_0014df70 + iVar1) != *(short *)(&DAT_0014df72 + iVar1) &&
              (cVar4 = FUN_000b6720(param_1), cVar4 == '\0')))) {
            local_92 = *(undefined2 *)(&DAT_0014df74 + iVar1);
            FUN_000bc1a0(auStack_90,param_2);
            do {
              uVar2 = FUN_000b4680(param_1,param_2,1);
              uVar3 = (uint)uVar2;
              if ((uVar3 & 0xff) == 7) {
                FUN_000b3a60(7,param_1,1);
              }
              else {
                FUN_000b3a60(7,param_1,0);
              }
              if (((uVar3 & 0xff) == 2) && (param_3 == 1)) {
                FUN_000bbf50(local_a0);
                if (local_a0[0] == 4) {
                  FUN_000ba2d0(&DAT_40002948);
                  FUN_000b4bb0();
                  FUN_000ba1f0(&DAT_40002948);
                }
                else {
                  FUN_000ba2d0(&DAT_40002948);
                  DAT_4000294c = 4;
                  FUN_000ba2d0(&DAT_40002948);
                  FUN_000ba1f0(&DAT_40002948);
                }
              }
            } while (((uVar3 & 0xff) == 2) && (param_3 == 1));
          }
          else {
            uVar2 = 0x12;
          }
        }
        else {
          uVar2 = 0x1f;
        }
      }
    }
    else {
      uVar2 = 3;
    }
  }
  else {
    uVar2 = 6;
  }
  return uVar2;
}

