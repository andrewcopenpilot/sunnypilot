
undefined8 FUN_000bc9d0(void)

{
  char cVar1;
  undefined8 uVar2;
  
  DAT_40037744 = 0;
  DAT_40037798 = 0;
  DAT_40037799 = 0;
  DAT_4003779a = 0;
  FUN_000b99b0();
  DAT_4000d81c = DAT_4000d830;
  if ((DAT_40037745 & 1) == 0) {
    DAT_4003774c = (ushort)DAT_4000d7e5;
    DAT_4003774e = (ushort)DAT_4000d7e4;
    DAT_40037750 = (ushort)DAT_4000d7e3;
    DAT_40037754 = (ushort)DAT_4000d7e2;
    DAT_40037756 = (ushort)DAT_4000d7e1;
    DAT_40037758 = (ushort)DAT_4000d7e0;
    cVar1 = FUN_00045460(DAT_00142388,&DAT_4003774c,0);
    if (cVar1 == '\0') {
      DAT_40037745 = DAT_40037745 | 1;
    }
  }
  if ((DAT_40037745 >> 3 & 1) == 0) {
    DAT_40037764 = DAT_4000d808;
    DAT_40037768 = DAT_4000d804;
    DAT_4003776c = DAT_4000d800;
    DAT_40037770 = DAT_4000d7fc;
    DAT_40037774 = DAT_4000d7f8;
    DAT_40037778 = DAT_4000d7f4;
    DAT_4003777c = DAT_4000d7f0;
    DAT_40037780 = DAT_4000d7ec;
    DAT_40037784 = DAT_4000d7e8;
    cVar1 = FUN_00045460(DAT_0014238e,&DAT_40037764,0);
    if (cVar1 == '\0') {
      DAT_40037745 = DAT_40037745 | 8;
    }
  }
  if ((DAT_40037745 >> 1 & 1) == 0) {
    FUN_00045520(6);
    if (DAT_400376f3 == '\x01') {
      DAT_4003775c = DAT_400376f2;
      cVar1 = FUN_00045460(DAT_0014238a,&DAT_4003775c,0);
      if (cVar1 == '\0') {
        DAT_40037745 = DAT_40037745 | 2;
      }
    }
    FUN_00045560(6);
  }
  if ((DAT_40037745 >> 2 & 1) == 0) {
    FUN_00045520(6);
    if (DAT_400376f5 == '\x01') {
      DAT_40037760 = (ushort)DAT_400376f4;
      cVar1 = FUN_00045460(DAT_0014238c,&DAT_40037760,0);
      if (cVar1 == '\0') {
        DAT_40037745 = DAT_40037745 | 4;
      }
    }
    FUN_00045560(6);
  }
  if ((DAT_40037745 >> 4 & 1) == 0) {
    FUN_00045520(6);
    if (DAT_400376f1 == '\x01') {
      DAT_40037788 = DAT_400376f0;
      cVar1 = FUN_00045460(0x9a,&DAT_40037788,0);
      if (cVar1 == '\0') {
        DAT_40037745 = DAT_40037745 | 0x10;
      }
    }
    FUN_00045560(6);
  }
  if ((DAT_40037745 >> 5 & 1) == 0) {
    DAT_40037790 = DAT_4000d810;
    DAT_40037791 = DAT_4000d811;
    DAT_40037792 = DAT_4000d812;
    DAT_40037793 = DAT_4000d813;
    DAT_40037794 = DAT_4000d814;
    DAT_40037795 = DAT_4000d815;
    DAT_40037796 = DAT_4000d816;
    DAT_40037797 = DAT_4000d817;
    cVar1 = FUN_00045460(DAT_00142390,&DAT_40037790,0);
    if (cVar1 == '\0') {
      DAT_40037745 = DAT_40037745 | 0x20;
    }
  }
  if ((DAT_40037745 & 0x3f) == 0x3f) {
    (*(code *)((uint)PTR_FUN_0014102c & 0xfffffffe))(&DAT_4000fa28);
    (*(code *)((uint)PTR_FUN_00141084 & 0xfffffffe))(&DAT_40010df0);
    (*(code *)((uint)PTR_FUN_0014103c & 0xfffffffe))(&DAT_4000fac0);
    (*(code *)((uint)PTR_FUN_001410b4 & 0xfffffffe))(&DAT_40011160);
    (*(code *)((uint)PTR_FUN_001410a4 & 0xfffffffe))(&DAT_4001101c);
    (*(code *)((uint)PTR_FUN_00141094 & 0xfffffffe))(&DAT_40010e98);
    (*(code *)((uint)PTR_FUN_00141064 & 0xfffffffe))(&DAT_40010a28);
    (*(code *)((uint)PTR_FUN_00141074 & 0xfffffffe))(&DAT_40010bf0);
    (*(code *)((uint)PTR_FUN_00141054 & 0xfffffffe))(&DAT_40010238);
    uVar2 = 1;
  }
  else if (DAT_40037746 < 3) {
    DAT_40037746 = DAT_40037746 + 1;
    uVar2 = 0;
  }
  else {
    DAT_40037746 = 0;
    uVar2 = 1;
    (*(code *)((uint)PTR_FUN_0014102c & 0xfffffffe))(&DAT_4000fa28);
    (*(code *)((uint)PTR_FUN_00141084 & 0xfffffffe))(&DAT_40010df0);
    (*(code *)((uint)PTR_FUN_0014103c & 0xfffffffe))(&DAT_4000fac0);
    (*(code *)((uint)PTR_FUN_001410b4 & 0xfffffffe))(&DAT_40011160);
    (*(code *)((uint)PTR_FUN_001410a4 & 0xfffffffe))(&DAT_4001101c);
    (*(code *)((uint)PTR_FUN_00141094 & 0xfffffffe))(&DAT_40010e98);
    (*(code *)((uint)PTR_FUN_00141064 & 0xfffffffe))(&DAT_40010a28);
    (*(code *)((uint)PTR_FUN_00141074 & 0xfffffffe))(&DAT_40010bf0);
    (*(code *)((uint)PTR_FUN_00141054 & 0xfffffffe))(&DAT_40010238);
  }
  DAT_4000d830 = DAT_4000d81c;
  return uVar2;
}

