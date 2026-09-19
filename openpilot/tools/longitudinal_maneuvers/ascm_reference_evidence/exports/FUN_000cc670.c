
void FUN_000cc670(undefined4 param_1,int param_2,undefined4 param_3,int param_4,undefined8 param_5,
                 undefined8 param_6,undefined8 param_7,undefined8 param_8,undefined1 param_9,
                 undefined4 param_10,undefined4 param_11,undefined1 param_12,undefined1 param_13,
                 undefined4 param_14,undefined4 param_15,undefined1 *param_16,undefined1 *param_17,
                 undefined1 *param_18,undefined1 *param_19,undefined1 *param_20,undefined1 *param_21
                 )

{
  undefined1 local_70;
  undefined1 local_6f;
  undefined1 local_6e;
  undefined1 local_6d;
  undefined1 local_6c;
  undefined1 local_6b;
  undefined1 local_6a;
  undefined1 local_69;
  undefined1 local_68;
  undefined1 local_67;
  undefined1 local_66;
  undefined1 local_65;
  undefined1 local_64;
  undefined1 local_63;
  undefined1 local_62;
  undefined1 local_61;
  undefined1 local_60;
  undefined1 local_5f;
  
  FUN_000ca270(param_5,*(undefined4 *)(DAT_40037a30 + 3000),(uint)LZCOUNT(param_1) >> 5,
               (uint)LZCOUNT(param_2 + -0x42) >> 5,&local_70);
  FUN_000ca270(param_6,*(undefined4 *)(DAT_40037a30 + 3000),(uint)LZCOUNT(param_3) >> 5,
               (uint)LZCOUNT(param_4 + -0x42) >> 5,&local_6f);
  FUN_000ca2b0(param_10,param_11,*(undefined4 *)(DAT_40037a30 + 0xbbc),param_12,param_13,param_14,
               param_15,*(undefined4 *)(DAT_40037a30 + 0xbd8));
  FUN_000c91f0(param_7,*(undefined1 *)(DAT_40037a30 + 0xbce),param_8,param_9,local_5f,
               *(undefined1 *)(DAT_40037a30 + 0xbb3),*(undefined1 *)(DAT_40037a30 + 0xbb2),
               *(undefined4 *)(DAT_40037a30 + 0xbe0));
  FUN_000c91f0(param_7,*(undefined1 *)(DAT_40037a30 + 0xbcc),param_8,param_9,local_70,
               *(undefined1 *)(DAT_40037a30 + 0xbb1),*(undefined1 *)(DAT_40037a30 + 0xbb0),
               *(undefined4 *)(DAT_40037a30 + 0xbdc));
  FUN_000c91f0(param_7,*(undefined1 *)(DAT_40037a30 + 0xbcc),param_8,param_9,local_6f,
               *(undefined1 *)(DAT_40037a30 + 0xbb1),*(undefined1 *)(DAT_40037a30 + 0xbb0),
               *(undefined4 *)(DAT_40037a30 + 0xbdc));
  *param_21 = local_67;
  param_21[1] = local_68;
  *param_16 = local_65;
  *param_17 = local_64;
  param_21[2] = local_61;
  param_21[3] = local_62;
  param_21[4] = local_63;
  param_21[5] = local_60;
  *param_18 = local_6e;
  param_21[6] = local_6b;
  param_21[7] = local_6c;
  param_21[8] = local_6d;
  *param_19 = local_6a;
  *param_20 = local_69;
  param_21[9] = local_66;
  return;
}

