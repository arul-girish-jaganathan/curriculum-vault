# Scatter-gather descriptors

> Canonical C topic note — Chapter 45. Scatter-gather DMA uses a list of descriptors so one transfer can consume or produce multiple non-contiguous memory regions.

## Definition
A descriptor typically contains an address, length, control flags, and linkage to the next descriptor. The descriptor layout is a hardware ABI and must match exact width, alignment, endianness, ownership, and valid-bit semantics.

## Mechanism and language rules
A C structure can model a descriptor, but its layout must not be assumed to match hardware without verification. Padding, pointer representation, integer width, and endian assumptions matter. Hardware often requires physical/device addresses rather than C virtual pointers.

### What to reason about
- Descriptor size and alignment.
- Address width and address space.
- Ownership bit ordering.
- Cache visibility.
- Ring termination and chaining rules.
- Lifetime of buffers referenced by descriptors.

## Embedded implications
Scatter-gather reduces copying and can support fragmented buffers, but increases descriptor management complexity and error recovery paths. A descriptor may remain hardware-owned after the CPU believes the transfer is complete unless the completion semantics are correctly understood.

### Firmware review angle
Keep descriptor creation and validation centralized. Use static assertions for expected structure size/offsets where the implementation permits, and explicit serialization when hardware layout is not naturally represented by the ABI.

## Edge cases and failure modes
- Hardware follows a descriptor whose buffer has been freed/reused.
- Cache contains stale descriptor ownership bits.
- Address width truncates a high address.
- Reserved descriptor bits are set incorrectly.
- Ring wrap creates a cycle or skips an entry.

## Example pattern
```c
struct dma_desc {
    uint32_t addr;
    uint16_t len;
    uint16_t flags;
};
```
This is a software model only until the hardware specification confirms layout and access requirements.

## Verification / debugging
Test single, chained, maximum-length, empty, wraparound, error, and reset cases. Dump descriptors and compare against hardware-visible memory after cache synchronization.

## Staff-level takeaway
A DMA descriptor is an **external ABI consumed by hardware**. Treat its layout, ownership, address space, and lifetime as a formal contract rather than ordinary C structure data.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
