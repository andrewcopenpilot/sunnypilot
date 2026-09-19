// RAM seeded from descriptor at 0x40220; table 0x155070 -> 0x4001d860.

void FUN_00138c90(int param_1,int param_2,int param_3,uint *param_4,uint *param_5,int param_6)

{
  uint uVar1;
  uint uVar2;
  
  *(undefined1 *)((int)param_5 + 0xd) = *(undefined1 *)((int)param_5 + 0xe);
  *param_4 = *param_4 & 0xfff7ffff;
  switch(*(undefined1 *)((int)param_5 + 0xe)) {
  case 0:
    *(uint *)(param_6 + 0xc) = *(uint *)(param_6 + 0xc) & 0xf03fffff;
    *(undefined1 *)(param_5 + 3) = 0;
    if ((param_5[2] >> 0x14 & 1) == 0) {
      if (*(char *)(param_1 + 4) == '\x01') {
        if ((*param_4 >> 0x17 & 1) == 0) {
          *(undefined1 *)((int)param_5 + 0xe) = 1;
        }
      }
      else if ((*(char *)(param_1 + 4) == '\x03') && ((*param_4 >> 0x16 & 1) == 0)) {
        *(undefined1 *)((int)param_5 + 0xe) = 7;
      }
    }
    else if ((*param_4 >> 0x16 & 1) == 0) {
      *(undefined1 *)((int)param_5 + 0xf) = 0;
      *(undefined1 *)((int)param_5 + 0xe) = 0xb;
    }
    break;
  case 1:
    *(uint *)(param_6 + 0xc) = *(uint *)(param_6 + 0xc) & 0xf03fffff;
    *(undefined1 *)(param_5 + 3) = 1;
    if ((param_5[2] >> 0x14 & 1) == 0) {
      if (*(char *)(param_1 + 4) == '\x03') {
        *(undefined1 *)((int)param_5 + 0xe) = 7;
      }
      else if (*(char *)(param_1 + 4) == '\x01') {
        uVar1 = *param_5;
        if (((int)uVar1 < 0) || ((uVar1 >> 0x1d & 1) != 0)) {
          if ((int)param_5[2] < 0) {
            *(undefined1 *)((int)param_5 + 0xe) = 2;
            *(undefined1 *)(param_5 + 3) = 2;
          }
          else {
            *(undefined1 *)(param_5 + 3) = 4;
          }
        }
        else {
          if (((uVar1 >> 0x1a & 1) != 0) || ((uVar1 >> 0x19 & 1) != 0)) {
            *(undefined1 *)(param_5 + 3) = 4;
          }
          if ((*param_5 >> 0x11 & 1) != 0) {
            *(undefined1 *)(param_5 + 3) = 2;
          }
        }
      }
      else {
        *(undefined1 *)((int)param_5 + 0xe) = 0;
      }
    }
    else {
      *(undefined1 *)((int)param_5 + 0xf) = 1;
      *(undefined1 *)((int)param_5 + 0xe) = 0xb;
    }
    break;
  case 2:
    *(uint *)(param_6 + 0xc) = *(uint *)(param_6 + 0xc) & 0xf03fffff;
    *(undefined1 *)(param_5 + 3) = 1;
    if ((param_5[2] >> 0x1d & 1) == 0) {
      if ((*param_5 >> 0x11 & 1) != 0) {
        *(undefined1 *)(param_5 + 3) = 2;
      }
    }
    else {
      *(undefined1 *)((int)param_5 + 0xe) = 3;
    }
    break;
  case 3:
  case 4:
    if ((*param_5 >> 0x14 & 1) != 0) {
      *(uint *)(param_2 + 0x18) = *(uint *)(param_2 + 0x18) | 0x4000000;
    }
    uVar2 = *(uint *)(param_6 + 0xc) & 0xf83fffff;
    *(uint *)(param_6 + 0xc) = uVar2;
    uVar1 = param_5[2];
    if ((uVar1 >> 0x1b & 1) == 0) {
      if (*(char *)((int)param_5 + 0xe) == '\x03') {
        *(undefined1 *)(param_5 + 3) = 3;
        if ((uVar1 >> 0x19 & 1) == 0) {
          if ((uVar1 >> 0x1a & 1) == 0) {
            uVar2 = *param_5;
            if ((uVar2 >> 0x14 & 1) == 0) {
              if ((uVar1 >> 0x1c & 1) == 0) {
                if ((((((uVar2 >> 0x1a & 1) == 0) && ((uVar2 >> 0x19 & 1) == 0)) &&
                     ((uVar2 >> 0x1b & 1) == 0)) &&
                    (((uVar2 >> 0x18 & 1) == 0 && (-1 < (int)uVar2)))) && ((uVar2 >> 0x11 & 1) == 0)
                   ) {
                  if ((int)(uint)*(byte *)((int)param_5 + 0x25) <
                      (int)((uint)*(byte *)((int)param_5 + 0x1a) -
                           (uint)*(byte *)((int)param_5 + 0x19))) {
                    *(undefined1 *)(param_5 + 3) = 7;
                  }
                  else if ((uVar2 >> 0x1d & 1) == 0) {
                    *(undefined1 *)(param_5 + 3) = 3;
                  }
                  else {
                    *(undefined1 *)(param_5 + 3) = 2;
                  }
                }
                else {
                  *(undefined1 *)(param_5 + 3) = 2;
                }
              }
              else if ((uVar1 >> 0x14 & 1) == 0) {
                *(undefined1 *)((int)param_5 + 0xe) = 4;
              }
              else {
                *(undefined1 *)((int)param_5 + 0xf) = 3;
                *(undefined1 *)((int)param_5 + 0xe) = 0xb;
              }
            }
            else if ((uVar1 >> 0x14 & 1) == 0) {
              *(undefined1 *)((int)param_5 + 0xe) = 5;
              *(undefined1 *)(param_5 + 3) = 5;
            }
            else {
              *(undefined1 *)((int)param_5 + 0xf) = 1;
              *(undefined1 *)((int)param_5 + 0xe) = 0xb;
            }
          }
          else if ((uVar1 >> 0x14 & 1) == 0) {
            *(undefined1 *)((int)param_5 + 0xe) = 5;
            *(undefined1 *)(param_5 + 3) = 5;
            if ((*param_5 >> 0x13 & 1) == 0) {
              *param_4 = *param_4 | 0x80000;
            }
          }
          else {
            *(undefined1 *)((int)param_5 + 0xf) = 1;
            *(undefined1 *)((int)param_5 + 0xe) = 0xb;
          }
        }
        else if ((uVar1 >> 0x14 & 1) == 0) {
          *(undefined1 *)((int)param_5 + 0xe) = 6;
          *(undefined1 *)(param_5 + 3) = 5;
          if ((*param_5 >> 0x13 & 1) == 0) {
            *param_4 = *param_4 | 0x80000;
          }
        }
        else {
          *(undefined1 *)((int)param_5 + 0xf) = 1;
          *(undefined1 *)((int)param_5 + 0xe) = 0xb;
        }
      }
      else {
        *(uint *)(param_6 + 0xc) = uVar2 | 0x1000000;
        *(undefined1 *)(param_5 + 3) = 6;
        uVar1 = param_5[2];
        if ((uVar1 >> 0x1a & 1) == 0) {
          uVar2 = *param_5;
          if ((uVar2 >> 0x14 & 1) == 0) {
            if ((uVar1 >> 0x1c & 1) == 0) {
              *(undefined1 *)((int)param_5 + 0xe) = 3;
            }
            else if ((uVar1 >> 0x14 & 1) == 0) {
              if ((((uVar2 >> 0x1a & 1) == 0) && ((uVar2 >> 0x19 & 1) == 0)) &&
                 (((uVar2 >> 0x1b & 1) == 0 &&
                  ((((uVar2 >> 0x18 & 1) == 0 && (-1 < (int)uVar2)) && ((uVar2 >> 0x11 & 1) == 0))))
                 )) {
                *(undefined1 *)(param_5 + 3) = 6;
              }
              else {
                *(undefined1 *)(param_5 + 3) = 2;
              }
            }
            else {
              *(undefined1 *)((int)param_5 + 0xf) = 3;
              *(undefined1 *)((int)param_5 + 0xe) = 0xb;
            }
          }
          else if ((uVar1 >> 0x14 & 1) == 0) {
            *(undefined1 *)((int)param_5 + 0xe) = 1;
            *(undefined1 *)(param_5 + 3) = 5;
          }
          else {
            *(undefined1 *)((int)param_5 + 0xf) = 1;
            *(undefined1 *)((int)param_5 + 0xe) = 0xb;
          }
        }
        else if ((uVar1 >> 0x14 & 1) == 0) {
          *(undefined1 *)((int)param_5 + 0xe) = 1;
          *(undefined1 *)(param_5 + 3) = 5;
          if ((*param_5 >> 0x13 & 1) == 0) {
            *param_4 = *param_4 | 0x80000;
          }
        }
        else {
          *(undefined1 *)((int)param_5 + 0xf) = 1;
          *(undefined1 *)((int)param_5 + 0xe) = 0xb;
        }
      }
    }
    else if ((uVar1 >> 0x14 & 1) == 0) {
      *(undefined1 *)((int)param_5 + 0xe) = 1;
      *(undefined1 *)(param_5 + 3) = 5;
      if ((*param_5 >> 0x13 & 1) == 0) {
        *param_4 = *param_4 | 0x80000;
      }
    }
    else {
      *(undefined1 *)((int)param_5 + 0xf) = 1;
      *(undefined1 *)((int)param_5 + 0xe) = 0xb;
    }
    break;
  case 5:
  case 6:
  case 10:
    uVar1 = *(uint *)(param_6 + 0xc);
    *(uint *)(param_6 + 0xc) = uVar1 & 0xfc3fffff | 0x4000000;
    if ((*(char *)((int)param_5 + 0xe) == '\x05') || (*(char *)((int)param_5 + 0xe) == '\n')) {
      *(uint *)(param_6 + 0xc) = *(uint *)(param_6 + 0xc) | 0x2000000;
    }
    else {
      *(uint *)(param_6 + 0xc) = uVar1 & 0xf83fffff;
    }
    if (*(char *)((int)param_5 + 0xe) == '\n') {
      *(uint *)(param_6 + 0xc) = *(uint *)(param_6 + 0xc) | 0x800000;
    }
    else {
      *(uint *)(param_6 + 0xc) = *(uint *)(param_6 + 0xc) & 0xff7fffff;
    }
    uVar1 = param_5[2];
    if ((uVar1 >> 0x14 & 1) == 0) {
      if ((uVar1 >> 0x1b & 1) == 0) {
        uVar2 = *param_5;
        if (((int)uVar2 < 0) || ((uVar2 >> 0x1d & 1) != 0)) {
          if ((int)param_5[2] < 0) {
            *(undefined1 *)((int)param_5 + 0xe) = 2;
            *(undefined1 *)(param_5 + 3) = 2;
          }
          else {
            *(undefined1 *)(param_5 + 3) = 4;
          }
        }
        else if (((uVar2 >> 0x1e & 1) == 0) && ((uVar2 >> 0x1c & 1) == 0)) {
          if (((((uVar1 >> 0x18 & 1) == 0) || (*(char *)((int)param_5 + 0xe) != '\x06')) &&
              (((param_5[2] >> 0x17 & 1) == 0 || (*(char *)((int)param_5 + 0xe) != '\x05')))) &&
             (((param_5[2] >> 0x15 & 1) == 0 || (*(char *)((int)param_5 + 0xe) != '\n')))) {
            if (*(char *)((int)param_5 + 0xe) == '\x06') {
              *param_4 = *param_4 | 0x80000;
              *(undefined1 *)(param_5 + 3) = 5;
            }
          }
          else if (*(char *)(param_1 + 4) == '\x01') {
            *(undefined1 *)((int)param_5 + 0xe) = 1;
          }
          else if (*(char *)(param_1 + 4) == '\x03') {
            *(undefined1 *)((int)param_5 + 0xe) = 7;
          }
          else {
            *(undefined1 *)((int)param_5 + 0xe) = 0;
          }
        }
        else if ((param_5[2] >> 0x1e & 1) == 0) {
          *(undefined1 *)(param_5 + 3) = 0xb;
        }
        else {
          *(undefined1 *)((int)param_5 + 0xe) = 8;
          *(undefined1 *)(param_5 + 3) = 9;
        }
      }
      else if ((byte)(*(char *)((int)param_5 + 0xe) - 5U) < 2) {
        *(undefined1 *)((int)param_5 + 0xe) = 1;
      }
    }
    else {
      if ((byte)(*(char *)((int)param_5 + 0xe) - 5U) < 2) {
        *(undefined1 *)((int)param_5 + 0xf) = 1;
      }
      else {
        *(undefined1 *)((int)param_5 + 0xf) = 7;
      }
      *(undefined1 *)((int)param_5 + 0xe) = 0xb;
    }
    break;
  case 7:
    *(uint *)(param_6 + 0xc) = *(uint *)(param_6 + 0xc) & 0xf03fffff;
    *(undefined1 *)(param_5 + 3) = 8;
    if ((param_5[2] >> 0x14 & 1) == 0) {
      if (*(char *)(param_1 + 4) == '\x01') {
        *(undefined1 *)((int)param_5 + 0xe) = 1;
      }
      else if (*(char *)(param_1 + 4) == '\x03') {
        uVar1 = *param_5;
        if (((uVar1 >> 0x1e & 1) == 0) && ((uVar1 >> 0x1c & 1) == 0)) {
          if ((uVar1 >> 0x11 & 1) != 0) {
            *(undefined1 *)(param_5 + 3) = 9;
          }
        }
        else if ((param_5[2] >> 0x1e & 1) == 0) {
          *(undefined1 *)(param_5 + 3) = 0xb;
        }
        else {
          *(undefined1 *)((int)param_5 + 0xe) = 8;
          *(undefined1 *)(param_5 + 3) = 9;
        }
      }
      else {
        *(undefined1 *)((int)param_5 + 0xe) = 0;
      }
    }
    else {
      *(undefined1 *)((int)param_5 + 0xf) = 7;
      *(undefined1 *)((int)param_5 + 0xe) = 0xb;
    }
    break;
  case 8:
  case 9:
    *(uint *)(param_6 + 0xc) = *(uint *)(param_6 + 0xc) & 0xfdffffff | 0x4800000;
    *(undefined1 *)(param_5 + 3) = 10;
    if (*(char *)((int)param_5 + 0xe) == '\t') {
      *(uint *)(param_6 + 0xc) = *(uint *)(param_6 + 0xc) | 0x1000000;
    }
    else {
      *(uint *)(param_6 + 0xc) = *(uint *)(param_6 + 0xc) & 0xfeffffff;
    }
    uVar1 = *param_5;
    if (((uVar1 >> 0x14 & 1) == 0) && ((param_5[2] >> 0x16 & 1) == 0)) {
      if ((((uVar1 >> 0x17 & 1) != 0) || (((uVar1 >> 0x16 & 1) != 0 || ((uVar1 >> 0x1b & 1) != 0))))
         || ((uVar1 >> 0x18 & 1) != 0)) {
        *(undefined1 *)(param_5 + 3) = 9;
      }
      if ((*param_5 >> 0x11 & 1) != 0) {
        *(undefined1 *)(param_5 + 3) = 9;
      }
      if (*(char *)((int)param_5 + 0xe) == '\b') {
        if ((param_5[2] >> 0x1c & 1) != 0) {
          *(undefined1 *)((int)param_5 + 0xe) = 9;
        }
      }
      else if ((param_5[2] >> 0x1c & 1) == 0) {
        *(undefined1 *)((int)param_5 + 0xe) = 8;
      }
    }
    else if ((param_5[2] >> 0x14 & 1) == 0) {
      if (*(char *)((int)param_5 + 0xe) == '\b') {
        *(undefined1 *)((int)param_5 + 0xe) = 10;
      }
      else {
        *(undefined1 *)((int)param_5 + 0xe) = 7;
      }
      *(undefined1 *)(param_5 + 3) = 0xc;
      if ((param_5[2] >> 0x16 & 1) != 0) {
        *param_4 = *param_4 | 0x80000;
      }
    }
    else {
      *(undefined1 *)((int)param_5 + 0xf) = 7;
      *(undefined1 *)((int)param_5 + 0xe) = 0xb;
    }
    break;
  case 0xb:
    *(uint *)(param_6 + 0xc) = *(uint *)(param_6 + 0xc) & 0xf87fffff;
    *(undefined1 *)(param_5 + 3) = 0xd;
    uVar1 = param_5[2];
    if ((uVar1 >> 0x14 & 1) == 0) {
      uVar2 = *param_5;
      if (((int)uVar2 < 0) || ((uVar2 >> 0x1d & 1) != 0)) {
        if ((int)param_5[2] < 0) {
          *(undefined1 *)((int)param_5 + 0xe) = 2;
          *(undefined1 *)(param_5 + 3) = 2;
        }
        else {
          *(undefined1 *)(param_5 + 3) = 4;
        }
      }
      else if (((uVar2 >> 0x1e & 1) == 0) && ((uVar2 >> 0x1c & 1) == 0)) {
        if ((*(char *)((int)param_5 + 0xf) == '\x03') &&
           ((((uVar1 >> 0x1a & 1) != 0 || ((uVar1 >> 0x1b & 1) != 0)) || ((uVar2 >> 0x14 & 1) != 0))
           )) {
          *(undefined1 *)((int)param_5 + 0xf) = 1;
          *(undefined1 *)(param_5 + 3) = 5;
        }
      }
      else if ((param_5[2] >> 0x1e & 1) == 0) {
        *(undefined1 *)(param_5 + 3) = 0xb;
      }
      else {
        *(undefined1 *)((int)param_5 + 0xe) = 8;
        *(undefined1 *)(param_5 + 3) = 9;
      }
    }
    else {
      *(undefined1 *)((int)param_5 + 0xe) = *(undefined1 *)((int)param_5 + 0xf);
    }
  }
  if ((*(uint *)(param_3 + 0x14) >> 0x18 & 1) == 0) {
    if ((*(uint *)(param_2 + 0x18) >> 0x1d & 1) == 0) {
      *(undefined1 *)(param_5 + 4) = 2;
    }
    else {
      *(undefined1 *)(param_5 + 4) = 1;
    }
  }
  else {
    *(undefined1 *)(param_5 + 4) = 0;
  }
  if ((*param_5 >> 0x11 & 1) != 0) {
    *(undefined1 *)(param_5 + 3) = 2;
  }
  return;
}


