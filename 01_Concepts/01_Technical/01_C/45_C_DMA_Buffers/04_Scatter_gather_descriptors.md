# Scatter-gather descriptors

> Canonical C topic note — Chapter 45. Scatter-gather DMA uses a descriptor chain or table so one transfer can span multiple non-contiguous buffers. Descriptor layout, ownership, addressability, alignment, and lifetime are hardware contracts.

## Definition
A descriptor commonly contains a device-visible buffer address, length, control flags, status, and a link to another descriptor. The DMA engine consumes descriptors without executing C code.

## Mechanism and language rules
C structures can describe descriptor layout only if their size, field offsets, alignment, endian representation, and access semantics match the hardware specification. `sizeof` and `offsetof` can be checked at compile time, but device address encoding remains platform-specific.

### What to reason about
- Descriptor ownership state.
- Field byte order and width.
- Alignment and cache-line constraints.
- Device-visible address versus CPU pointer.
- Chain termination and maximum length.
- Lifetime while hardware may fetch descriptors.

## Embedded implications
Scatter-gather reduces copying and can support fragmented buffers, but increases failure modes: bad links can create loops, invalid addresses can fault the bus, and stale cached descriptors can cause the device to execute old commands.

### Firmware review angle
Use explicit descriptor states and sequence identifiers. Validate every link and length before publishing ownership. Keep descriptors in a memory region accessible under the required DMA attributes.

## Edge cases and failure modes
- Device follows a stale cached link.
- Descriptor points to a released buffer.
- Ring/list contains a cycle unexpectedly.
- Length exceeds hardware maximum.
- CPU modifies a DMA-owned descriptor.

## Example pattern
```c
struct dma_desc {
    uint32_t next;
    uint32_t buffer;
    uint32_t length;
    uint32_t flags;
};
```
The actual field representation may require endian conversion, address translation, and target-specific alignment.

## Verification / debugging
Start with one descriptor, then two, before testing long chains. Inspect the exact descriptor bytes as hardware sees them. Test maximum lengths, invalid links, cache maintenance, abort, reset, and wraparound.

Staff-level questions: Can the device observe every descriptor update? What prevents cycles? Who owns each descriptor and referenced buffer? What is the failure state if a descriptor is partially consumed?

## Staff-level takeaway
Scatter-gather is a **distributed data structure executed by hardware**. Treat descriptor layout, address mapping, ownership, lifetime, and cache visibility as one correctness contract.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
