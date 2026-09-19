
undefined8 FUN_000b5770(undefined8 param_1,undefined8 param_2,int param_3)

{
  uint uVar1;
  bool bVar2;
  char cVar3;
  undefined8 uVar4;
  undefined1 auStack_88 [100];
  undefined4 local_24;
  
  uVar4 = 0;
  bVar2 = false;
  DAT_4000ab28 = DAT_4000ab28 + 1;
  local_24 = 0;
  FUN_000bc320(auStack_88,0,99);
  cVar3 = FUN_000b4ef0();
  if (cVar3 == '\x01') {
    if (param_3 == 1) {
      cVar3 = FUN_000ba190(&DAT_40002948);
      if (cVar3 != '\0') {
        FUN_000ba2d0(&DAT_40002948);
      }
    }
    else {
      cVar3 = FUN_000ba190(&DAT_40002948);
      if (cVar3 != '\0') {
        uVar4 = 1;
        bVar2 = true;
      }
    }
    if (!bVar2) {
      uVar4 = FUN_000b5870(param_1,param_2);
      uVar1 = (uint)uVar4 & 0xff;
      if ((uVar1 != 3) && (uVar1 != 5)) {
        FUN_000bc1a0(auStack_88,param_2);
      }
    }
    FUN_000ba1f0(&DAT_40002948);
  }
  else {
    uVar4 = 6;
    uVar1 = (uint)param_1 & 0xffff;
    FUN_000bc1a0(param_2,(&PTR_s_ADCGmbH_0014df78)[uVar1 * 4],
                 *(undefined2 *)(&DAT_0014df74 + uVar1 * 0x10));
  }
  return uVar4;
}

