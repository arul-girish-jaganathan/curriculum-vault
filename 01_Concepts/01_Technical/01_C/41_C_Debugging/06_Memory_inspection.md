# Memory inspection

> Canonical C topic note — Chapter 41. Memory inspection reads raw target bytes and interprets them using C object representation, ABI, linker layout, and target memory-map knowledge.

## Definition
Memory inspection is examination of target memory at an address, usually as bytes, words, or typed values. ISO C does not define debugger memory windows. It does define object representations and rules around accessing objects through appropriate lvalues and character types, but debugger reads occur outside the C abstract machine.

## Mechanism and language rules
A debugger can display the same bytes as hexadecimal, signed/unsigned integers, pointers, floating-point values, or structures. Interpretation is meaningful only when the type, alignment, endianness, ABI representation, and lifetime are known.

### What to reason about
- What object, if any, owns this address?
- Is the object alive at the time being inspected?
- What is its alignment and representation?
- What is the target endianness?
- Is the region RAM, flash, MMIO, retention RAM, or unmapped space?
- Is another CPU, ISR, DMA engine, or peripheral modifying it?
- Could a debugger read trigger a hardware side effect?

Raw bytes can reveal stack corruption, buffer overruns, allocator metadata damage, stale DMA descriptors, and corrupted return addresses, but a byte pattern alone does not prove a particular C-level cause.

## Embedded implications
MCUs often have sparse and aliased address maps. Invalid reads may generate bus faults. Memory windows over peripheral registers can clear flags or consume FIFO data. Some memories are inaccessible while clocks or power domains are disabled.

Linker map files are essential for interpreting addresses: they connect symbols and sections to RAM/flash regions. Stack boundaries, heap boundaries, DMA pools, bootloader regions, and retained crash storage should be known before inspecting arbitrary addresses.

### Firmware review angle
For cache-enabled systems, distinguish CPU cache state from backing memory and DMA visibility. A debugger may observe memory that differs from what a CPU or peripheral currently sees. For multicore targets, establish which observer and memory domain is being examined.

## Edge cases and failure modes
- **Wrong type interpretation:** identical bytes can represent different values under different types.
- **Endian confusion:** `0x12345678` has different byte order in memory depending on target endianness.
- **Dead object:** memory may have been reused after lifetime ended.
- **MMIO side effects:** reading a register is not equivalent to reading ordinary RAM.
- **Stale cache:** displayed RAM may not reflect a device's view.
- **Corrupt debugger context:** a halted CPU does not freeze every bus master.

## Example pattern
```c
struct packet {
    uint16_t length;
    uint8_t payload[8];
};

static struct packet p;
```
To inspect `p`, first resolve its symbol address and size, then examine raw bytes, then interpret fields according to the ABI. Do not assume that a debugger's structure rendering is proof of the wire format.

## Verification / debugging
Start from a known symbol or linker address. Dump raw bytes, compare them with expected initialization, inspect adjacent guard regions, and correlate changes with code or DMA ownership. For corruption, take snapshots before and after the suspected operation and use watchpoints where hardware supports them.

Staff-level questions:
- What memory region is this address in?
- Which agent owns it?
- What representation should be expected?
- Is cache/coherency involved?
- Could inspection itself have side effects?

## Staff-level takeaway
Memory inspection is most useful when **address -> region -> object -> owner -> representation -> timeline** is established. Hex dumps are evidence; interpretation requires C object rules plus the target's ABI and memory architecture.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
