# Memory inspection

> Canonical C topic note — Chapter 41. Memory inspection compares raw bytes and addresses with the C object's type, lifetime, alignment, ownership, and target memory map. A debugger's memory window is not itself a proof of C-level validity.

## Definition
Memory inspection is examining bytes at selected addresses to determine object state, corruption, layout, stack contents, heap metadata, descriptors, or hardware state. C defines object representations and access rules, but debugger commands that read arbitrary addresses are target-specific.

The expert workflow is to ask both **what bytes are present** and **whether interpreting those bytes as this C object is valid**.

## Mechanism and language rules
Objects have representations consisting of bytes. Structure padding may contain unspecified values; trap representations can make some interpretations invalid on implementations that support them; alignment requirements constrain valid typed access. A debugger can display raw bytes without performing a C lvalue access, so its ability to show bytes does not mean program code could safely dereference the same address.

### What to reason about
- What memory region contains the address: stack, heap, static RAM, flash, MMIO, shared memory, or DMA buffer?
- What object lifetime and type apply?
- Is the address aligned for the intended type?
- Does the debugger read trigger hardware side effects?
- Are caches, memory protection, remapping, or bus faults involved?
- Could another execution agent change the memory between observations?

Interpret endianness explicitly when converting byte sequences to multi-byte values.

## Embedded implications
MCU memory maps often include aliased regions, tightly coupled memory, external RAM, flash, peripheral registers, and reserved holes. A seemingly valid address may be inaccessible in the current privilege mode or may have read side effects.

DMA introduces a second writer and cache maintenance can make CPU-visible bytes differ from memory visible to a peripheral. Inspect descriptors, ownership bits, buffer addresses, and cache state together.

### Firmware review angle
Maintain a documented memory map and symbolized inspection procedure. For persistent fault records, preserve raw bytes plus metadata such as image version, CPU context, region identity, and length rather than only a formatted interpretation.

## Edge cases and failure modes
- **Wrong interpretation:** viewing bytes with the wrong type or endianness.
- **Padding confusion:** assuming every structure byte is initialized meaningfully.
- **MMIO side effects:** a read changes status or clears an event.
- **Stale cache:** CPU and DMA views are inconsistent.
- **Out-of-lifetime memory:** an address remains readable after the C object no longer exists.
- **Corrupted debugger context:** the inspection itself can disturb the fault evidence.

## Example pattern
```c
struct header {
    uint16_t type;
    uint16_t length;
    uint32_t sequence;
};
```
When inspecting a serialized or in-memory header, first establish `sizeof`, alignment, padding, and byte order. Do not assume the in-memory representation is a wire-format representation.

## Verification / debugging
Capture both raw bytes and typed interpretations. Compare the observed layout with compiler output (`sizeof`, `_Alignof`, `offsetof`) and the target memory map. For suspected corruption, inspect surrounding canaries and the last known owner of the region.

Use debugger memory reads cautiously on MMIO. For DMA problems, compare CPU cache state, memory barriers, descriptor ownership, and peripheral-visible memory rather than relying on a single memory window.

Staff-level questions: What makes this address a valid object? Who can write it? Which memory domain is being observed? Is the debugger reading the same storage that the failing agent used?

## Staff-level takeaway
Memory inspection is strongest when **bytes, object semantics, ownership, and hardware memory topology agree**. Raw bytes are evidence, but their meaning must be established rather than assumed.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
