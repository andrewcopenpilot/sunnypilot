
bool FUN_000bc380(int param_1)

{
  bool bVar1;
  byte bVar2;
  char cVar3;
  
  DAT_40037740 = 0;
  DAT_40037745 = 0;
  DAT_40037746 = 0;
  DAT_40037747 = 0;
  DAT_40037748 = 0;
  DAT_4000d82c = DAT_4000d830;
  FUN_00045690(0x9e,1);
  FUN_000b99b0();
  if (-1 < (char)DAT_40037744) {
    FUN_0012c090();
    DAT_40037744 = DAT_40037744 | 0x80;
  }
  bVar2 = DAT_40037744;
  if ((DAT_40037744 & 1) == 0) {
    cVar3 = FUN_00045410(DAT_00142388,&DAT_4003774c,0);
    if (cVar3 == '\0') {
      DAT_4000d7e5 = (undefined1)DAT_4003774c;
      DAT_4000d7e4 = (undefined1)DAT_4003774e;
      DAT_4000d7e3 = (undefined1)DAT_40037750;
      DAT_4000d7e2 = (undefined1)DAT_40037754;
      DAT_4000d7e1 = (undefined1)DAT_40037756;
      DAT_4000d7e0 = (undefined1)DAT_40037758;
      bVar2 = DAT_40037744 | 1;
    }
    else {
      bVar2 = DAT_40037744 | 1;
      if (param_1 == 0) {
        bVar2 = DAT_40037744;
      }
    }
  }
  DAT_40037744 = bVar2;
  bVar2 = DAT_40037744;
  if ((DAT_40037744 >> 1 & 1) == 0) {
    cVar3 = FUN_00045410(DAT_0014238a,&DAT_4003775c,0);
    if (cVar3 == '\0') {
      FUN_00045520(6);
      DAT_400376a2 = DAT_4003775c;
      DAT_400376a3 = 1;
      FUN_00045560(6);
      bVar2 = DAT_40037744 | 2;
    }
    else {
      bVar2 = DAT_40037744 | 2;
      if (param_1 == 0) {
        bVar2 = DAT_40037744;
      }
    }
  }
  DAT_40037744 = bVar2;
  bVar2 = DAT_40037744;
  if ((DAT_40037744 >> 2 & 1) == 0) {
    cVar3 = FUN_00045410(DAT_0014238c,&DAT_40037760,0);
    if (cVar3 == '\0') {
      FUN_00045520(6);
      DAT_400376a4 = (undefined1)DAT_40037760;
      DAT_400376a5 = 1;
      FUN_00045560(6);
      bVar2 = DAT_40037744 | 4;
    }
    else {
      bVar2 = DAT_40037744 | 4;
      if (param_1 == 0) {
        bVar2 = DAT_40037744;
      }
    }
  }
  DAT_40037744 = bVar2;
  bVar2 = DAT_40037744;
  if ((DAT_40037744 >> 3 & 1) == 0) {
    cVar3 = FUN_00045410(DAT_0014238e,&DAT_40037764,0);
    if (cVar3 == '\0') {
      DAT_4000d808 = DAT_40037764;
      DAT_4000d804 = DAT_40037768;
      DAT_4000d800 = DAT_4003776c;
      DAT_4000d7fc = DAT_40037770;
      DAT_4000d7f8 = DAT_40037774;
      DAT_4000d7f4 = DAT_40037778;
      DAT_4000d7f0 = DAT_4003777c;
      DAT_4000d7ec = DAT_40037780;
      DAT_4000d7e8 = DAT_40037784;
      FUN_00045520(6);
      DAT_400376a8 = DAT_40037764;
      DAT_400376ac = 1;
      DAT_400376b0 = DAT_40037768;
      DAT_400376b4 = 1;
      DAT_400376b8 = DAT_4003776c;
      DAT_400376bc = 1;
      DAT_400376c0 = DAT_40037770;
      DAT_400376c4 = 1;
      DAT_400376c8 = DAT_40037774;
      DAT_400376cc = 1;
      DAT_400376d0 = DAT_40037778;
      DAT_400376d4 = 1;
      DAT_400376d8 = DAT_4003777c;
      DAT_400376dc = 1;
      DAT_400376e0 = DAT_40037780;
      DAT_400376e4 = 1;
      DAT_400376e8 = DAT_40037784;
      DAT_400376ec = 1;
      FUN_00045560(6);
      bVar2 = DAT_40037744 | 8;
    }
    else {
      bVar2 = DAT_40037744 | 8;
      if (param_1 == 0) {
        bVar2 = DAT_40037744;
      }
    }
  }
  DAT_40037744 = bVar2;
  bVar2 = DAT_40037744;
  if ((DAT_40037744 >> 4 & 1) == 0) {
    cVar3 = FUN_00045410(0x9a,&DAT_40037788,0);
    if (cVar3 == '\0') {
      FUN_00045520(6);
      DAT_400376a0 = DAT_40037788;
      DAT_400376a1 = 1;
      FUN_00045560(6);
      bVar2 = DAT_40037744 | 0x10;
    }
    else {
      bVar2 = DAT_40037744 | 0x10;
      if (param_1 == 0) {
        bVar2 = DAT_40037744;
      }
    }
  }
  DAT_40037744 = bVar2;
  bVar2 = DAT_40037744;
  if ((DAT_40037744 >> 5 & 1) == 0) {
    cVar3 = FUN_00045410(DAT_00142390,&DAT_40037790,0);
    if (cVar3 == '\0') {
      DAT_4000d810 = DAT_40037790;
      DAT_4000d811 = DAT_40037791;
      DAT_4000d812 = DAT_40037792;
      DAT_4000d813 = DAT_40037793;
      DAT_4000d814 = DAT_40037794;
      DAT_4000d815 = DAT_40037795;
      DAT_4000d816 = DAT_40037796;
      DAT_4000d817 = DAT_40037797;
      bVar2 = DAT_40037744 | 0x20;
    }
    else {
      bVar2 = DAT_40037744 | 0x20;
      if (param_1 == 0) {
        bVar2 = DAT_40037744;
      }
    }
  }
  DAT_40037744 = bVar2;
  bVar1 = (DAT_40037744 & 0xbf) == 0xbf;
  if (bVar1) {
    FUN_0012c1d0();
    FUN_000c8dc0();
    FUN_000cf000();
    FUN_000dcfc0();
    FUN_000de470();
    FUN_000e3a80();
    FUN_000d87a0();
    (*(code *)((uint)PTR_FUN_00141024 & 0xfffffffe))(&DAT_4000fa28);
    (*(code *)((uint)PTR_FUN_0014107c & 0xfffffffe))(&DAT_40010df0);
    (*(code *)((uint)PTR_FUN_00141034 & 0xfffffffe))(&DAT_4000fac0);
    (*(code *)((uint)PTR_FUN_001410ac & 0xfffffffe))(&DAT_40011160);
    (*(code *)((uint)PTR_FUN_0014109c & 0xfffffffe))(&DAT_4001101c);
    (*(code *)((uint)PTR_FUN_0014108c & 0xfffffffe))(&DAT_40010e98);
    (*(code *)((uint)PTR_FUN_0014105c & 0xfffffffe))(&DAT_40010a28);
    (*(code *)((uint)PTR_FUN_0014106c & 0xfffffffe))(&DAT_40010bf0);
    (*(code *)((uint)PTR_FUN_0014104c & 0xfffffffe))(&DAT_40010238);
  }
  FUN_00045690(0x9e,0);
  DAT_4000d830 = DAT_4000d82c;
  return bVar1;
}

