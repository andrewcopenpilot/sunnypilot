
void FUN_0013a5d0(longlong param_1,int param_2,short *param_3,int param_4,int param_5,short *param_6
                 ,short *param_7)

{
  char cVar1;
  ushort uVar2;
  int iVar3;
  int iVar4;
  short sVar5;
  short sVar6;
  short sVar7;
  undefined2 uVar8;
  longlong lVar9;
  uint uVar10;
  longlong lVar11;
  longlong lVar12;
  
  iVar4 = FUN_0012e610((longlong)param_7[*(byte *)(param_7 + 0x70) + 0xc] - (longlong)param_7[7]);
  if (iVar4 < 0x65) {
    if ((ushort)param_7[0x72] < 5000) {
      param_7[0x72] = param_7[0x72] + (short)param_1;
    }
  }
  else {
    param_7[0x72] = 0;
  }
  cVar1 = *(char *)(param_7 + 0x70);
  *(byte *)(param_7 + 0x70) = cVar1 + 1U;
  if (99 < (byte)(cVar1 + 1U)) {
    *(undefined1 *)(param_7 + 0x70) = 0;
  }
  param_7[*(byte *)(param_7 + 0x70) + 0xc] = param_7[7];
  uVar10 = (uint)*(ushort *)(DAT_40037a40 + 0x764);
  if (((ushort)param_7[0x72] <= *(ushort *)(DAT_40037a40 + 0x764)) &&
     (lVar9 = (ulonglong)(ushort)param_7[0x72] - param_1, uVar10 = (uint)lVar9, lVar9 < 0)) {
    uVar10 = 0;
  }
  sVar5 = FUN_0013a570(uVar10 & 0xffff,param_1,param_7 + 0xc,*(undefined1 *)(param_7 + 0x70),100);
  sVar5 = param_7[7] - sVar5;
  uVar2 = *(ushort *)(DAT_40037a40 + 0x764);
  sVar6 = FUN_0012e3e0(DAT_40037a40 + 0x768,3,*param_3);
  uVar10 = ((sVar5 * 1000) / (int)(uint)uVar2) * (int)sVar6;
  iVar4 = (int)param_1;
  sVar6 = FUN_0012e5e0((ulonglong)(uVar10 >> 0x1f) +
                       (longlong)((int)uVar10 / 1000 + ((int)uVar10 >> 0x1f)),param_7[5],
                       (int)(uint)*(ushort *)(DAT_40037a40 + 0x766) / iVar4);
  param_7[5] = sVar6;
  uVar2 = param_7[0x71];
  uVar10 = (uint)uVar2;
  if ((*(char *)(param_2 + 0xe) == *(char *)(param_2 + 0xf)) || (*(char *)(param_4 + 10) != '\x01'))
  {
    if ((*(uint *)(param_3 + 10) >> 0x18 & 1) == 0) {
      if (*(char *)(param_4 + 10) == '\x01') {
        if (sVar5 < 0) {
          uVar10 = (uint)*(ushort *)(DAT_40037a40 + 0x82a);
        }
        else {
          uVar10 = (uint)*(ushort *)(DAT_40037a40 + 0x82c);
        }
      }
      else if (*(char *)(param_4 + 10) == '\x02') {
        if (sVar5 < 0) {
          uVar10 = (uint)*(ushort *)(DAT_40037a40 + 0x82e);
        }
        else {
          uVar10 = (uint)*(ushort *)(DAT_40037a40 + 0x830);
        }
      }
    }
    else {
      uVar10 = (uint)*(ushort *)(DAT_40037a40 + 0x828);
    }
  }
  else {
    uVar10 = (uint)uVar2 + iVar4;
  }
  sVar5 = FUN_0012e5e0(uVar10 & 0xffff,uVar2,(int)(uint)*(ushort *)(DAT_40037a40 + 0x79e) / iVar4);
  param_7[0x71] = sVar5;
  sVar5 = FUN_0013a570(sVar5,param_1,param_7 + 0xc,*(undefined1 *)(param_7 + 0x70),100);
  DAT_4001e182 = FUN_0012e5e0(sVar5,DAT_4001e182,
                              (int)(uint)*(ushort *)(DAT_40037a40 + 0x79c) / iVar4);
  lVar11 = (longlong)DAT_4001e182 - (longlong)param_3[1];
  lVar9 = (longlong)sVar5 - (longlong)param_3[1];
  if ((((*(uint *)(param_3 + 10) >> 0x18 & 1) != 0) && (*param_7 < 0)) ||
     (*(char *)(param_7 + 0x74) == '\x01')) {
    lVar11 = 0;
    lVar9 = 0;
  }
  param_7[0x75] = DAT_4001e182;
  param_7[0x76] = sVar5;
  if ((*(uint *)(param_5 + 0xc) >> 0x1a & 1) == 0) {
    DAT_4001e188 = 0;
    param_7[0x73] = 0;
  }
  else {
    if (((*(uint *)(param_5 + 0xc) >> 0x18 & 1) == 0) &&
       (1 < (byte)(*(char *)((int)param_7 + 0x293) - 3U))) {
      if ((ushort)param_7[0x73] < 10000) {
        param_7[0x73] = param_7[0x73] + (short)param_1;
      }
    }
    else {
      param_7[0x73] = 0;
    }
    if ((((((DAT_4001e17c >> 0x1a & 1) == 0) && ((*(uint *)(param_5 + 0xc) >> 0x1a & 1) != 0)) ||
         (((*(uint *)(param_5 + 0xc) >> 0x18 & 1) != 0 ||
          ((*(char *)((int)param_7 + 0x293) == '\x03' || (*(char *)((int)param_7 + 0x293) == '\x04')
           ))))) || ((*(char *)(param_4 + 10) == '\x01' && (DAT_4001e171 != '\x01')))) ||
       ((*(char *)(param_4 + 10) == '\x02' && (DAT_4001e171 != '\x02')))) {
      DAT_4001e182 = param_3[1];
      if ((*(char *)(param_4 + 10) == '\x02') && (*(char *)(DAT_40037a40 + 0x6ba) == '\0')) {
        lVar12 = 0;
        DAT_4001e188 = 0;
      }
      else {
        sVar5 = param_6[2];
        lVar12 = (longlong)sVar5;
        sVar6 = FUN_0012e3e0(DAT_40037a40 + 0x73e,3,*param_3);
        if ((int)sVar5 < ((int)*param_6 - (int)param_3[1]) * (int)sVar6) {
          sVar5 = FUN_0012e3e0(DAT_40037a40 + 0x73e,3,*param_3);
          lVar12 = ((longlong)*param_6 - (longlong)param_3[1]) * (longlong)sVar5;
        }
        DAT_4001e188 = (int)lVar12;
      }
      DAT_4001e184 = 0;
      if (((DAT_4001e17c >> 0x1a & 1) != 0) && ((byte)(*(char *)((int)param_7 + 0x293) - 3U) < 2)) {
        DAT_4001e188 = FUN_0012e5e0(lVar12,DAT_4001e1ac,2000 / iVar4);
      }
    }
    else {
      sVar5 = FUN_0012e610(param_7[1]);
      sVar6 = FUN_0012e610(*param_7);
      sVar7 = FUN_0012e610(lVar11);
      if ((((sVar5 <= *(short *)(DAT_40037a40 + 0x7a0)) &&
           (sVar6 <= *(short *)(DAT_40037a40 + 0x7a2))) &&
          (sVar7 <= *(short *)(DAT_40037a40 + 0x7a4))) &&
         ((DAT_4001e18c == 0 &&
          ((int)DAT_4001dae8 <=
           (int)((uint)*(byte *)(DAT_40037a40 + 0x72d) * (int)DAT_4001dc94) / 100 +
           (int)DAT_4001dc94)))) {
        sVar5 = FUN_0012e3e0(DAT_40037a40 + 0x736,2,*param_3);
        iVar3 = (int)sVar5 * (int)lVar11;
        if ((DAT_4001d8f2 == -1) && (DAT_4001d990 == '\x01')) {
          iVar3 = (int)(iVar3 * (uint)*(byte *)(DAT_40037a40 + 0x72c)) / 100;
        }
        iVar3 = (iVar3 * iVar4) / 1000;
        if (((*(char *)(DAT_40037a40 + 0x5df) != '\x01') || (DAT_4001d924 == 0)) ||
           ((iVar3 < 1 || (DAT_4001e188 < 1)))) {
          if ((*(char *)(param_4 + 10) == '\x02') && (*(char *)(DAT_40037a40 + 0x6ba) == '\0')) {
            DAT_4001e188 = 0;
          }
          else {
            DAT_4001e188 = DAT_4001e188 + iVar3;
          }
        }
      }
    }
  }
  sVar5 = (short)(DAT_4001e188 >> 0x1f);
  param_7[3] = ((short)(DAT_4001e188 / 1000) + sVar5) -
               ((short)((short)(DAT_4001e188 / 0x3e80000) + sVar5) >> 0xf);
  DAT_4001e1ac = DAT_4001e188;
  sVar5 = FUN_0012e3e0(DAT_40037a40 + 0x774,6,DAT_4001d8f4);
  param_7[6] = sVar5;
  sVar5 = FUN_0012e610(lVar9);
  sVar6 = FUN_0012e610(*param_7);
  sVar5 = FUN_0012e3e0(DAT_40037a40 + 0x74e,2,sVar6 + sVar5 * 2);
  uVar10 = (int)lVar9 * (int)sVar5;
  lVar12 = (longlong)((int)uVar10 / 1000 + ((int)uVar10 >> 0x1f)) + (ulonglong)(uVar10 >> 0x1f);
  if (param_7[0x73] == 0) {
    param_7[2] = 0;
  }
  else if (((*(char *)(DAT_40037a40 + 0x5df) == '\x01') && (DAT_4001d924 != 0)) && (0 < (int)lVar12)
          ) {
    param_7[2] = 0;
  }
  else if (*(char *)(param_2 + 0xe) == *(char *)(param_2 + 0xf)) {
    uVar8 = FUN_0012e3e0(DAT_40037a40 + 0x756,3,param_7[0x73]);
    sVar5 = FUN_0012e5e0(lVar12,param_7[2],uVar8);
    param_7[2] = sVar5;
  }
  else {
    uVar8 = FUN_0012e3e0(DAT_40037a40 + 0x756,3,0);
    sVar5 = FUN_0012e5e0(lVar12,param_7[2],uVar8);
    param_7[2] = sVar5;
  }
  if ((*(char *)(param_4 + 10) == '\x02') && (*(char *)(DAT_40037a40 + 0x6ba) == '\0')) {
    param_7[2] = 0;
  }
  if ((*(uint *)(param_5 + 0xc) >> 0x19 & 1) != 0) {
    *(uint *)(param_3 + 10) = *(uint *)(param_3 + 10) | 0x8000000;
    sVar5 = FUN_0012e630(param_6[2],param_7[1],*(undefined4 *)(DAT_40037a40 + 0x6d8),
                         *(undefined4 *)(DAT_40037a40 + 0x6d4),param_1);
    param_7[1] = sVar5;
    if ((*(uint *)(param_5 + 0xc) >> 0x17 & 1) == 0) {
      if (*(char *)(param_4 + 10) == '\x01') {
        if (sVar5 <= param_6[2]) {
          *(uint *)(param_3 + 10) = *(uint *)(param_3 + 10) & 0xf7ffffff;
          param_7[1] = param_6[2];
        }
      }
      else if ((*(char *)(param_4 + 10) == '\x02') && (param_6[2] <= sVar5)) {
        *(uint *)(param_3 + 10) = *(uint *)(param_3 + 10) & 0xf7ffffff;
        param_7[1] = param_6[2];
      }
    }
    else {
      sVar5 = FUN_0012e630(param_6[3],sVar5,-(ulonglong)*(uint *)(DAT_40037a40 + 0x6d0),
                           (ulonglong)*(uint *)(DAT_40037a40 + 0x6d0),param_1);
      param_7[1] = sVar5;
      if ((param_6[3] <= sVar5) || ((*(uint *)(param_3 + 10) >> 0x1a & 1) != 0)) {
        *(uint *)(param_3 + 10) = *(uint *)(param_3 + 10) & 0xf7ffffff;
      }
    }
    goto LAB_0013adac;
  }
  param_7[1] = param_7[2] + param_7[5] + *param_7 + param_7[3];
  *(uint *)(param_3 + 10) = *(uint *)(param_3 + 10) & 0xf7ffffff;
  if (*(char *)(param_2 + 0xe) == *(char *)(param_2 + 0xf)) {
    if (((param_7[1] <= param_6[3]) || (*param_7 < param_3[1])) &&
       (((DAT_4001e18c == 0 || (*param_3 < 0x12d)) ||
        ((param_7[1] <= param_6[3] && (*param_7 < param_3[1])))))) goto LAB_0013acd0;
    uVar10 = (int)lVar9 * (int)*(short *)(DAT_40037a40 + 0x74a) * iVar4;
    lVar9 = (ulonglong)(uVar10 >> 0x1f) + (longlong)((int)uVar10 / 1000 + ((int)uVar10 >> 0x1f)) +
            (ulonglong)DAT_4001e18c;
    DAT_4001e18c = (uint)lVar9;
    DAT_4001e18c = FUN_0012e5a0(lVar9,(longlong)*(short *)(DAT_40037a40 + 0x762) *
                                      SUB168(SEXT216(1000),0),0);
  }
  else {
LAB_0013acd0:
    if (((ushort)(*param_3 - 0x65U) < 199) && (param_7[7] < 1)) {
      sVar5 = FUN_0012e3e0(DAT_40037a40 + 0x736,2);
      uVar10 = (int)sVar5 * (int)lVar11 * iVar4;
      lVar9 = (ulonglong)(uVar10 >> 0x1f) + (longlong)((int)uVar10 / 1000 + ((int)uVar10 >> 0x1f)) +
              (ulonglong)DAT_4001e18c;
      DAT_4001e18c = (uint)lVar9;
      DAT_4001e18c = FUN_0012e5a0(lVar9,(longlong)*(short *)(DAT_40037a40 + 0x762) *
                                        SUB168(SEXT216(1000),0),
                                  (~(longlong)*(short *)(DAT_40037a40 + 0x762) + 1U) *
                                  SUB168(SEXT216(1000),0));
    }
    else if (*param_3 < 1000) {
      DAT_4001e18c = FUN_0012e5e0(DAT_4001e18c,0,2000 / iVar4);
    }
    else {
      DAT_4001e18c = FUN_0012e5e0(0,DAT_4001e18c,
                                  (int)(uint)*(ushort *)(DAT_40037a40 + 0x74c) / iVar4);
    }
  }
  sVar5 = (short)((int)DAT_4001e18c >> 0x1f);
  sVar5 = ((short)((int)DAT_4001e18c / 1000) + sVar5) -
          ((short)((short)((int)DAT_4001e18c / 0x3e80000) + sVar5) >> 0xf);
  param_7[4] = sVar5;
  sVar5 = sVar5 + param_7[1];
  param_7[1] = sVar5;
  if ((*(uint *)(param_5 + 0xc) >> 0x1a & 1) != 0) {
    param_7[1] = sVar5 + param_7[6];
  }
LAB_0013adac:
  DAT_4001e17c = *(undefined4 *)(param_5 + 0xc);
  DAT_4001e180 = (undefined2)lVar11;
  param_7[7] = *param_7;
  param_7[8] = param_7[1];
  return;
}

