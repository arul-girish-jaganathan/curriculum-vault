# IOMMU-facing pointers

> Canonical C topic note — Chapter 45. A device-facing DMA address is not necessarily a CPU pointer. IOMMUs and SoC memory systems can translate, restrict, or remap device addresses independently of the CPU address space.

## Definition
A CPU pointer identifies storage in the CPU's address space. A DMA descriptor may require an I/O virtual address, bus address, physical address, or device-specific token. The mapping is platform-specific and must never be inferred by casting a pointer.

## Mechanism and language rules
A platform DMA layer maps a CPU buffer into a device-visible address space and returns an address with defined permissions, lifetime, alignment, and synchronization semantics. The mapping must remain valid while the device may access the buffer.

### What to reason about
- CPU address space versus device address space.
- Mapping and unmapping lifetime.
- Address width and truncation.
- IOMMU permissions and domains.
- Cache/coherency attributes.
- Suspend/reset effects.
- Whether the device can access the entire mapped range.

## Embedded implications
IOMMUs are common in complex SoCs and high-end embedded platforms. They improve isolation and support virtualization but introduce mapping setup, TLB, fault handling, and debugging complexity.

### Firmware review angle
Use an explicit device-address type and platform mapping API. Never store a CPU pointer in a 32-bit descriptor field merely because the current board happens to use low addresses.

## Edge cases and failure modes
- CPU pointer truncated to 32 bits.
- Mapping removed while DMA is active.
- IOMMU permission rejects access.
- Mapping attributes conflict with cache policy.
- Device reset invalidates mappings.

## Example pattern
```c
void submit(void *cpu_buf, size_t len)
{
    dma_addr_t dev_addr = dma_map_for_device(cpu_buf, len);
    program_descriptor(dev_addr, len);
}
```
`dma_addr_t` and mapping APIs are platform abstractions, not ISO C constructs.

## Verification / debugging
Record CPU and device addresses separately during diagnosis. Test address-width boundaries, permission failures, unmap-before-completion, suspend/resume, and device reset. Inspect IOMMU fault records when available.

Staff-level questions: Which address space does the descriptor contain? Who owns the mapping lifetime? What proves the mapping remains valid until completion? Can the device reach every byte of the buffer?

## Staff-level takeaway
A device address is **not a C pointer value**. Treat address translation, permissions, cache attributes, alignment, and mapping lifetime as first-class DMA contracts.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
