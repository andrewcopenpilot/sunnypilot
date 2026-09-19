
short FUN_0013bbc0(int param_1,int param_2,int param_3)

{
  short sVar1;
  int iVar2;
  
  iVar2 = (((int)(((*(short *)(param_2 + 0x1a) * 0x2652) / 1000 +
                  (param_1 * *(short *)(param_2 + 0x1c)) / 1000) * (uint)*(ushort *)(param_2 + 0x10)
                 ) / 10 +
           (((((*(short *)(param_2 + 0x14) * param_3) / 100) * param_3) / 100) * 1000) / 1000) /
          1000) * (((uint)*(ushort *)(param_2 + 0x12) * 10000) / 0xf570);
  sVar1 = (short)(iVar2 >> 0x1f);
  return ((short)(iVar2 / 1000) + sVar1) - ((short)((short)(iVar2 / 0x3e80000) + sVar1) >> 0xf);
}

