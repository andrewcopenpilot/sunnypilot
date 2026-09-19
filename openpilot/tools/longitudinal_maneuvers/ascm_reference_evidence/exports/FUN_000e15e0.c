
void FUN_000e15e0(undefined8 param_1,undefined8 param_2,undefined8 param_3,undefined8 param_4,
                 undefined4 param_5,undefined8 param_6,undefined8 param_7,undefined8 param_8,
                 undefined4 param_9,undefined4 param_10,undefined4 param_11,undefined4 param_12,
                 undefined4 param_13,undefined4 *param_14,undefined4 *param_15,undefined4 *param_16,
                 undefined4 *param_17,undefined4 *param_18,undefined4 *param_19,undefined4 *param_20
                 ,undefined4 *param_21,int param_22,undefined4 *param_23)

{
  undefined4 local_70;
  undefined4 local_6c;
  undefined4 local_68;
  undefined4 local_64;
  undefined4 local_60;
  undefined4 local_5c;
  undefined4 local_58;
  undefined4 local_54 [21];
  
  FUN_000e1390(param_1,param_2,*(undefined4 *)(DAT_40037a30 + 0x7c0),
               *(undefined2 *)(DAT_40037a30 + 0x7b8),*(undefined4 *)(DAT_40037a30 + 0x950),param_3,
               *param_23,param_4,*(undefined4 *)(DAT_40037a30 + 0x948),
               *(undefined4 *)(DAT_40037a30 + 0x94c),param_5,&local_6c,&local_70,param_22 + 0xcc);
  *param_14 = local_70;
  *param_15 = local_6c;
  FUN_000e1390(param_6,param_7,*(undefined4 *)(DAT_40037a30 + 0x7c0),
               *(undefined2 *)(DAT_40037a30 + 0x7b8),*(undefined4 *)(DAT_40037a30 + 0x950),param_8,
               *param_23,param_4,*(undefined4 *)(DAT_40037a30 + 0x948),
               *(undefined4 *)(DAT_40037a30 + 0x94c),param_9,&local_64,&local_68,param_22 + 0x88);
  *param_16 = local_68;
  *param_17 = local_64;
  FUN_000e1390(param_10,param_11,*(undefined4 *)(DAT_40037a30 + 0x7c0),
               *(undefined2 *)(DAT_40037a30 + 0x7b8),*(undefined4 *)(DAT_40037a30 + 0x950),param_3,
               *param_23,param_4,*(undefined4 *)(DAT_40037a30 + 0x948),
               *(undefined4 *)(DAT_40037a30 + 0x94c),param_5,&local_5c,&local_60,param_22 + 0x44);
  *param_18 = local_60;
  *param_19 = local_5c;
  FUN_000e1390(param_12,param_13,*(undefined4 *)(DAT_40037a30 + 0x7c0),
               *(undefined2 *)(DAT_40037a30 + 0x7b8),*(undefined4 *)(DAT_40037a30 + 0x950),param_8,
               *param_23,param_4,*(undefined4 *)(DAT_40037a30 + 0x948),
               *(undefined4 *)(DAT_40037a30 + 0x94c),param_9,local_54,&local_58,param_22);
  *param_20 = local_58;
  *param_21 = local_54[0];
  return;
}

