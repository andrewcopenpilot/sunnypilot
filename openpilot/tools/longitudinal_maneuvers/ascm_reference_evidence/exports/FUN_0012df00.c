
void FUN_0012df00(int param_1,short param_2,short *param_3,int param_4)

{
  if (param_1 == 1) {
    if (param_4 == 0) {
      *param_3 = 0;
    }
    if (*param_3 != 0) {
      *param_3 = *param_3 + -1;
    }
  }
  else {
    *param_3 = param_2;
  }
  return;
}

