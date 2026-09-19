// Recover the RAM jump table from its firmware initialization descriptor; read-only project invocation.
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.*;
import ghidra.program.model.mem.*;
import ghidra.program.model.listing.*;
import java.io.*;
public class RecoverASCMState extends GhidraScript {
  public void run() throws Exception {
    var mem = currentProgram.getMemory();
    if (mem.getInt(toAddr(0x40220)) != 0x154fe0 ||
        mem.getInt(toAddr(0x40224)) != 0x4001d7d0 ||
        mem.getInt(toAddr(0x40228)) != 0xe68)
      throw new IllegalStateException("Firmware startup descriptor does not match this audit");
    var start = toAddr(0x4001d7d0L);
    var block = mem.getBlock(start);
    if (!block.isInitialized()) mem.convertToInitialized(block, (byte)0);
    byte[] data = new byte[0xe68];
    mem.getBytes(toAddr(0x154fe0),data);
    mem.setBytes(start,data);
    // Proven descriptor at 0x40220: source, destination, byte count.
    var lo = toAddr(0x4001d860L); var hi = lo.add(48);
    block = mem.getBlock(lo);
    if (!block.getStart().equals(lo)) mem.split(block,lo);
    block = mem.getBlock(lo);
    if (block.getEnd().compareTo(hi)>=0) mem.split(block,hi);
    mem.getBlock(lo).setWrite(false);
    var f = getFunctionAt(toAddr(0x138c90));
    var body = new AddressSet(toAddr(0x138c90),toAddr(0x13926f));
    for (int i=0;i<12;i++) disassemble(toAddr(mem.getInt(lo.add(i*4)) & 0xfffffffeL));
    f.setBody(body);
    var dec = new DecompInterface(); dec.openProgram(currentProgram);
    var r = dec.decompileFunction(f,120,monitor);
    try(var out=new PrintWriter(getScriptArgs()[0])) {
      out.println("// RAM seeded from descriptor at 0x40220; table 0x155070 -> 0x4001d860.");
      out.println(r.getDecompiledFunction()==null?r.getErrorMessage():r.getDecompiledFunction().getC());
    }
    dec.dispose();
  }
}
