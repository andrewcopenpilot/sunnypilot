
void FUN_0013afc0(undefined8 param_1,short *param_2,int param_3,int param_4,int param_5,int param_6)

{
  char cVar1;
  short sVar3;
  int iVar2;
  int iVar4;
  
  if (*(char *)(param_2 + 5) == '\x02') {
    sVar3 = FUN_0012e3e0(DAT_40037a40 + 0x708,3,DAT_4001d998);
    DAT_4001e1b0 = (short)((int)((1000 - (uint)*(ushort *)(DAT_40037a40 + 0x78c)) *
                                (int)*(short *)(param_5 + 0xc)) / 1000) + sVar3;
    if (*(char *)(DAT_40037a40 + 0x83c) == '\x01') {
      iVar2 = (int)*(short *)(param_4 + 4);
    }
    else {
      iVar2 = 0;
    }
  }
  else {
    if ((DAT_4001d8f2 == -1) && (*(char *)(param_6 + 0x18) == '\x01')) {
      sVar3 = FUN_0012e3e0(DAT_40037a40 + 0x720,3,DAT_4001d998);
      DAT_4001e1b0 = (short)((int)((1000 - (uint)*(ushort *)(DAT_40037a40 + 0x78e)) *
                                  (int)*(short *)(param_5 + 0xc)) / 1000) + sVar3;
    }
    else {
      sVar3 = FUN_0012e3e0(DAT_40037a40 + 0x714,3,DAT_4001d998);
      DAT_4001e1b0 = (short)((int)((1000 - (uint)*(ushort *)(DAT_40037a40 + 0x78e)) *
                                  (int)*(short *)(param_5 + 0xc)) / 1000) + sVar3;
    }
    iVar2 = (int)*(short *)(param_4 + 4);
  }
  param_2[8] = DAT_4001e1b0 + (short)iVar2;
  DAT_4001e171 = *(char *)(param_2 + 5);
  cVar1 = *(char *)(param_5 + 0x293);
  iVar4 = (int)param_1;
  if (cVar1 == '\0') {
    *(undefined1 *)(param_2 + 5) = 0;
    *param_2 = 0;
    param_2[1] = 0;
    if ((*(uint *)(param_3 + 0xc) >> 0x19 & 1) != 0) {
      *(char *)(param_2 + 5) = DAT_4001e171;
    }
  }
  else if (cVar1 == '\x02') {
    if ((((*(uint *)(param_3 + 0xc) >> 0x18 & 1) == 0) ||
        ((*(uint *)(param_3 + 0xc) >> 0x17 & 1) != 0)) || ((DAT_4001d9a0 >> 0x19 & 1) != 0)) {
      if ((int)*(short *)(param_5 + 0x10) <
          (int)*(short *)(DAT_40037a40 + 0x81c) + DAT_4001e1b0 + iVar2) {
        DAT_4001e184 = '\x01';
        param_2[8] = (short)(DAT_4001e1b0 + iVar2) + *(short *)(DAT_40037a40 + 0x81c);
        if (DAT_4001e171 == '\x02') {
          *(undefined1 *)(param_2 + 5) = 2;
          *param_2 = 0;
          if ((DAT_4001e1a6 == '\0') || (-1 < *(short *)(param_5 + 0x10))) {
            if (*(char *)(DAT_40037a40 + 0x80c) == '\x01') {
              sVar3 = FUN_0012e630((longlong)*(short *)(param_5 + 0x10) -
                                   (longlong)*(short *)(param_5 + 0xc),param_2[1],
                                   -(longlong)*(short *)(DAT_40037a40 + 0x80e),
                                   (longlong)*(short *)(DAT_40037a40 + 0x80e),param_1);
              param_2[1] = sVar3;
            }
            else {
              sVar3 = FUN_0012e3e0(DAT_40037a40 + 0x810,3,DAT_4001d998);
              sVar3 = FUN_0012e630((longlong)*(short *)(param_5 + 0x10) -
                                   (longlong)*(short *)(param_5 + 0xc),param_2[1],-(longlong)sVar3,
                                   (longlong)sVar3,param_1);
              param_2[1] = sVar3;
            }
          }
          else {
            DAT_4001e1a6 = DAT_4001e1a6 + -1;
            if (*(char *)(DAT_40037a40 + 0x80c) == '\x01') {
              sVar3 = FUN_0012e3e0(DAT_40037a40 + 0x810,3,DAT_4001d998);
              sVar3 = FUN_0012e630((longlong)*(short *)(param_5 + 0x10) -
                                   (longlong)*(short *)(param_5 + 0xc),param_2[1],-(longlong)sVar3,
                                   (longlong)sVar3,param_1);
              param_2[1] = sVar3;
              DAT_4001e188 = 0;
            }
            else {
              param_2[1] = *(short *)(DAT_40037a40 + 0x80a);
            }
          }
        }
        else {
          *(undefined1 *)(param_2 + 5) = 2;
          *param_2 = 0;
          if (*(char *)(DAT_40037a40 + 0x806) == '\x01') {
            DAT_4001e1a6 = (char)((int)(uint)*(ushort *)(DAT_40037a40 + 0x808) / iVar4);
            param_2[1] = *(short *)(DAT_40037a40 + 0x80a);
          }
          else {
            DAT_4001e1a6 = '\0';
            param_2[1] = *(short *)(param_5 + 0x10) - *(short *)(param_5 + 0xc);
          }
        }
      }
      else if (((DAT_4001d9a0 >> 0x19 & 1) == 0) && (DAT_4001d91c != 0)) {
        if ((*(char *)(param_5 + 0xe8) == '\0') && (*(char *)(param_2 + 7) != '\x03')) {
          if (DAT_4001e184 == '\0') {
            *param_2 = *(short *)(param_5 + 0x10);
          }
          else {
            *param_2 = *(short *)(param_4 + 4);
          }
          *(undefined1 *)(param_2 + 5) = 1;
          param_2[1] = 0;
        }
      }
      else {
        *(undefined1 *)(param_2 + 5) = 2;
        param_2[1] = *(short *)(param_5 + 0x10);
      }
    }
    else {
      *(undefined1 *)(param_2 + 5) = 1;
      *param_2 = *(short *)(param_5 + 0x10);
      param_2[1] = 0;
    }
  }
  else if (cVar1 == '\x01') {
    if ((((*(uint *)(param_3 + 0xc) >> 0x18 & 1) == 0) ||
        ((*(uint *)(param_3 + 0xc) >> 0x17 & 1) != 0)) || ((DAT_4001d9a0 >> 0x19 & 1) != 0)) {
      if ((int)*(short *)(param_5 + 0x10) <
          (int)*(short *)(DAT_40037a40 + 0x81e) + DAT_4001e1b0 + iVar2) {
        DAT_4001e184 = '\x01';
        param_2[8] = (short)(DAT_4001e1b0 + iVar2) + *(short *)(DAT_40037a40 + 0x81e);
        if (DAT_4001e171 == '\x02') {
          *(undefined1 *)(param_2 + 5) = 2;
          *param_2 = 0;
          if ((DAT_4001e1a6 == '\0') || (-1 < *(short *)(param_5 + 0x10))) {
            if (*(char *)(DAT_40037a40 + 0x80c) == '\x01') {
              sVar3 = FUN_0012e630((longlong)*(short *)(param_5 + 0x10) -
                                   (longlong)*(short *)(param_5 + 0xc),param_2[1],
                                   -(longlong)*(short *)(DAT_40037a40 + 0x80e),
                                   (longlong)*(short *)(DAT_40037a40 + 0x80e),param_1);
              param_2[1] = sVar3;
            }
            else {
              sVar3 = FUN_0012e3e0(DAT_40037a40 + 0x810,3,DAT_4001d998);
              sVar3 = FUN_0012e630((longlong)*(short *)(param_5 + 0x10) -
                                   (longlong)*(short *)(param_5 + 0xc),param_2[1],-(longlong)sVar3,
                                   (longlong)sVar3,param_1);
              param_2[1] = sVar3;
            }
          }
          else {
            DAT_4001e1a6 = DAT_4001e1a6 + -1;
            if (*(char *)(DAT_40037a40 + 0x80c) == '\x01') {
              sVar3 = FUN_0012e3e0(DAT_40037a40 + 0x810,3,DAT_4001d998);
              sVar3 = FUN_0012e630((longlong)*(short *)(param_5 + 0x10) -
                                   (longlong)*(short *)(param_5 + 0xc),param_2[1],-(longlong)sVar3,
                                   (longlong)sVar3,param_1);
              param_2[1] = sVar3;
              DAT_4001e188 = 0;
            }
            else {
              param_2[1] = *(short *)(DAT_40037a40 + 0x80a);
            }
          }
        }
        else {
          *(undefined1 *)(param_2 + 5) = 2;
          *param_2 = 0;
          if (*(char *)(DAT_40037a40 + 0x806) == '\x01') {
            DAT_4001e1a6 = (char)((int)(uint)*(ushort *)(DAT_40037a40 + 0x808) / iVar4);
            param_2[1] = *(short *)(DAT_40037a40 + 0x80a);
          }
          else {
            DAT_4001e1a6 = '\0';
            param_2[1] = *(short *)(param_5 + 0x10) - *(short *)(param_5 + 0xc);
          }
        }
      }
      else if (((DAT_4001d9a0 >> 0x19 & 1) == 0) && (DAT_4001d91c != 0)) {
        if ((*(char *)(param_5 + 0xe8) == '\0') && (*(char *)(param_2 + 7) != '\x03')) {
          if (DAT_4001e184 == '\0') {
            *param_2 = *(short *)(param_5 + 0x10);
          }
          else {
            *param_2 = *(short *)(param_4 + 4);
          }
          *(undefined1 *)(param_2 + 5) = 1;
          param_2[1] = 0;
        }
      }
      else {
        *(undefined1 *)(param_2 + 5) = 2;
        param_2[1] = *(short *)(param_5 + 0x10);
      }
    }
    else {
      *(undefined1 *)(param_2 + 5) = 1;
      *param_2 = *(short *)(param_5 + 0x10);
      param_2[1] = 0;
    }
  }
  else if (cVar1 == '\x03') {
    if (((*(uint *)(param_3 + 0xc) >> 0x18 & 1) == 0) || ((DAT_4001d9a0 >> 0x19 & 1) != 0)) {
      *(undefined1 *)(param_2 + 5) = 2;
      *param_2 = 0;
      param_2[1] = *(short *)(param_5 + 0x10) - *(short *)(param_5 + 0xc);
    }
    else {
      *(undefined1 *)(param_2 + 5) = 1;
      *param_2 = *(short *)(param_5 + 0x10);
      param_2[1] = 0;
    }
  }
  else if (cVar1 == '\x04') {
    *(undefined1 *)(param_2 + 5) = 1;
    *param_2 = *(short *)(param_5 + 0x10);
    param_2[1] = 0;
  }
  else {
    *(undefined1 *)(param_2 + 5) = 0;
    *param_2 = 0;
    param_2[1] = 0;
  }
  if (*(char *)(param_2 + 5) == '\x02') {
    if ((DAT_4001d928 == '\0') || (((DAT_4001da04 >> 0x1a & 1) != 0 && (DAT_4001d93f == '\x01')))) {
      *(undefined1 *)(param_2 + 7) = 1;
    }
    else if ((*(char *)(param_5 + 0xe8) == '\x01') &&
            (DAT_4001d998 < *(short *)(DAT_40037a40 + 0x820))) {
      if (DAT_4001d8e2 == '\x01') {
        *(undefined1 *)(param_2 + 7) = 4;
      }
      else {
        *(undefined1 *)(param_2 + 7) = 5;
        DAT_4001dc30 = (undefined2)((int)(uint)*(ushort *)(DAT_40037a40 + 0x832) / iVar4);
        DAT_4001e170 = '\x02';
      }
    }
    else if ((((DAT_4001d998 < *(short *)(DAT_40037a40 + 0x820)) &&
              ((DAT_4001dcc0 >> 0x1b & 1) != 0)) ||
             ((DAT_4001d998 < *(short *)(DAT_40037a40 + 0x822) && ((DAT_4001dcc0 >> 0x1c & 1) != 0))
             )) || (((DAT_4001d998 < *(short *)(DAT_40037a40 + 0x820) &&
                     ((DAT_4001d9a0 >> 0x19 & 1) != 0)) || (DAT_4001d91c == 0)))) {
      if ((DAT_4001e171 == '\x02') &&
         ((DAT_4001e170 == '\0' || (*(short *)(DAT_40037a40 + 0x824) == 0)))) {
        *(undefined1 *)(param_2 + 7) = 3;
      }
      else {
        *(undefined1 *)(param_2 + 7) = 2;
      }
    }
    else {
      *(undefined1 *)(param_2 + 7) = 2;
      if ((DAT_4001d998 < *(short *)(DAT_40037a40 + 0x824)) && ((byte)(DAT_4001e170 - 1U) < 2)) {
        DAT_4001e170 = '\x01';
      }
      else {
        DAT_4001e170 = '\0';
      }
    }
  }
  else {
    *(undefined1 *)(param_2 + 7) = 1;
  }
  return;
}

