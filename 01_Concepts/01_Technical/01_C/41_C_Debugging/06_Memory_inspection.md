# Memory inspection

> Canonical C topic note — chapter 41.

## Definition
Memory inspection is the deliberate examination of raw bytes and interpreted objects in memory during or after program execution. It is one of the most reliable ways to bridge a C-level hypothesis with the actual contents, layout, alignment, and lifetime state of the target address space.

A debugger's typed view is an interpretation. A raw memory dump is closer to the physical evidence, although memory may be volatile, device-backed, cached, protected, or changed by another execution agent.

## Mechanism and language rules
A memory location can be interpreted at several levels:

```text
raw bytes → target address → alignment/layout → C type interpretation → semantic hypothesis
```

C object representation is determined by the implementation. Padding bytes may exist within structures, integer representation is implementation-dependent within the standard's constraints, and reading arbitrary storage through an incompatible type can violate C's effective-type/alignment/lifetime rules.

Therefore a debugger command that displays bytes as `uint32_t`, `float`, or a struct is a visualization choice, not proof that the program was permitted to access those bytes that way.

### Useful inspection modes
Inspect memory as:

- bytes for corruption patterns and serialization;
- words for pointer/index/register state;
- structures for target-layout validation;
- strings for terminator/length problems;
- stack regions for frame corruption;
- guard/canary regions for overflow evidence.

Use the target endianness when interpreting multi-byte values.

## Embedded implications
Embedded address spaces are heterogeneous. A numeric address can refer to:

- SRAM;
- flash/ROM;
- peripheral MMIO;
- retained backup RAM;
- external memory;
- memory-mapped accelerators;
- unmapped/protected regions.

Reading an MMIO location from a debugger is not equivalent to reading ordinary RAM. Status registers may clear on read, FIFO registers may consume an entry, and bus faults can result from unsupported access widths or privilege levels.

DMA also changes the model: CPU memory inspection observes the memory state at one instant and may race with an in-flight transfer.

### Example corruption pattern
```c
struct packet {
    uint16_t len;
    uint8_t  data[32];
};
```
If `data[32]` overwrote the following field, inspect the raw bytes around the object and identify where the expected pattern stops. Then correlate the address with the linker map, object layout, and the last known writer. Do not infer the exact source statement from bytes alone.

## Edge cases and failure modes
- The memory changed between CPU halt and debugger read.
- Cache coherency causes the CPU and DMA engine to observe different data.
- Structure padding makes expected byte patterns non-contiguous.
- Endianness is misread during manual interpretation.
- A pointer value is valid-looking but outside the object's lifetime.
- Reading MMIO causes side effects.
- A memory protection/security boundary blocks the debugger.
- Stack/heap regions are reused, so old bytes are not evidence of current ownership.

## Verification / debugging
Use a layered procedure:

1. Record the exact address and expected object size.
2. Dump raw bytes first.
3. Check alignment and target endianness.
4. Compare against the compiler's structure layout and map file.
5. Inspect neighboring guard values or allocation metadata where applicable.
6. Identify all possible writers: CPU, ISR, DMA, another core, peripheral.
7. Repeat the observation at a controlled time or after freezing relevant execution agents.

For corruption bugs, fill unused memory with a known pattern at startup and sample high-water marks. For production devices, capture small targeted regions rather than dumping unbounded memory.

## Staff-level takeaway
Memory inspection is strongest when used as **evidence about state**, not as a substitute for C semantics. Start with raw bytes, then explain layout, ownership, lifetime, and writer history. A successful reconstruction should answer not only “what bytes are wrong?” but “which execution agent could legally or illegally have produced them, and at what time?”

## Related
[[00_Chapter_Index]]
[[03_Watchpoints]]
[[04_Call_stacks]]
[[08_Core_dumps]]
[[../27_C_Alignment_Object_Representation/00_Chapter_Index]]
[[../28_C_Endianness_Serialization/00_Chapter_Index]]
