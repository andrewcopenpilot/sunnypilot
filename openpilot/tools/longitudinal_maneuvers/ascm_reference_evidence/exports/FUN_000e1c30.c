
void FUN_000e1c30(undefined4 param_1,undefined4 param_2,undefined4 param_3,undefined4 param_4,
                 undefined8 param_5,undefined8 param_6,undefined8 param_7,undefined8 param_8,
                 undefined4 param_9,undefined4 param_10,undefined4 param_11,undefined4 param_12,
                 undefined4 *param_13,undefined4 *param_14,undefined4 *param_15,undefined4 *param_16
                 ,undefined4 *param_17,undefined4 *param_18,undefined4 *param_19,
                 undefined4 *param_20,uint param_21)

{
  ulonglong uVar1;
  undefined4 local_70;
  undefined4 local_6c;
  undefined4 local_68;
  undefined4 local_64;
  undefined4 local_60;
  undefined4 local_5c;
  undefined4 local_58;
  undefined4 local_54 [21];
  
  uVar1 = (ulonglong)param_21;
  FUN_000e1af0((uint)LZCOUNT(param_1) >> 5,param_5,param_6,&local_70,&local_6c,uVar1 + 0x3c);
  *param_13 = local_70;
  *param_14 = local_6c;
  FUN_000e1af0((uint)LZCOUNT(param_2) >> 5,param_9,param_10,&local_60,&local_5c,uVar1 + 0x14);
  *param_15 = local_60;
  *param_16 = local_5c;
  FUN_000e1af0((uint)LZCOUNT(param_3) >> 5,param_7,param_8,&local_68,&local_64,uVar1 + 0x28);
  *param_17 = local_68;
  *param_18 = local_64;
  FUN_000e1af0((uint)LZCOUNT(param_4) >> 5,param_11,param_12,&local_58,local_54,uVar1);
  *param_19 = local_58;
  *param_20 = local_54[0];
  return;
}

