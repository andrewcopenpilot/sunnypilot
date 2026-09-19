
longlong FUN_0012e5e0(int param_1,int param_2,int param_3)

{
  int iVar1;
  longlong lVar2;
  
  iVar1 = (param_2 * param_3 + param_1) / (param_3 + 1);
  lVar2 = (longlong)iVar1;
  if (iVar1 == param_2) {
    if (param_2 != param_1) {
      if (param_2 < param_1) {
        lVar2 = lVar2 + 1;
      }
      else if (param_1 < param_2) {
        lVar2 = lVar2 + -1;
      }
    }
  }
  return lVar2;
}

