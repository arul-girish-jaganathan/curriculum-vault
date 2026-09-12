# Memory inspection

> Canonical C topic note — chapter 41.

## Definition
Memory inspection is the examination of bytes, typed objects, pointers, and memory regions while diagnosing a running or stopped program. The debugger may display raw bytes, integers, floating-point values, structures, arrays, or strings, but the interpretation must respect the C object model and target memory map.

## Mechanism and language rules
A C object has a type, lifetime, alignment, and storage duration. Looking at its representation as bytes is useful, but interpreting arbitrary bytes as another object type can violate effective-type/aliasing or alignment rules when performed by the program. A debugger is an external observation mechanism, so its display should not be mistaken for a valid C expression.

Always distinguish:
- virtual/logical address from physical/bus address;
- object address from register/MMIO address;
- initialized storage from indeterminate bytes;
- cached CPU memory from DMA-visible memory.

## Embedded implications
MCUs commonly have distinct flash, SRAM, peripheral, retention, tightly coupled, external, and memory-mapped regions. A debugger memory window may fail or trigger a bus fault when reading an inaccessible address. Peripheral registers can be destructive on read or change asynchronously.

For DMA, inspect descriptor ownership, buffer address, transfer length, alignment, cache state, and completion status. A buffer containing “wrong” data can be caused by cache coherency or a producer/consumer ownership bug rather than a bad C assignment.

### Example
```c
struct packet {
    uint16_t len;
    uint8_t  data[8];
};

static struct packet p;
```
Inspecting `p` as fields is more meaningful than merely dumping 12 bytes. Also inspect the raw representation when diagnosing packing, endian, alignment, or corruption issues.

## Edge cases and failure modes
- Reading an invalid address can fault the target.
- Reading a volatile register can have side effects.
- A memory view can be stale if the debugger caches results.
- Compiler optimization can eliminate or move the object being inspected.
- Stack memory may have been reused after an object's lifetime ended.
- Uninitialized/indeterminate storage should not be treated as a meaningful value.
- Cache maintenance errors can make CPU and DMA observations disagree.

## Verification / debugging
Start with the target memory map and linker map. Determine the expected address, size, alignment, and ownership of the object. Compare typed and raw-byte views. Check neighboring guard bytes for overwrite evidence. For corruption, capture the earliest known-good state and establish the first transition to bad data using watchpoints, trace, periodic CRCs, or instrumentation.

For structures crossing interfaces, verify `sizeof`, `_Alignof`, member offsets, endian representation, and serialization rules rather than assuming host and target layouts match.

## Staff-level takeaway
Memory inspection is evidence gathering, not proof by itself. The strongest diagnosis connects **C object → address → instruction/agent → memory system → ownership/lifetime**. This is especially important for MMIO, DMA, caches, packed data, concurrent access, and optimized builds.

## Related
[[00_Chapter_Index]]
[[03_Watchpoints]]
[[05_Registers]]
[[10_Fault_localization]]
[[../27_C_Alignment_Object_Representation/00_Chapter_Index]]
[[../28_C_Endianness_Serialization/00_Chapter_Index]]
