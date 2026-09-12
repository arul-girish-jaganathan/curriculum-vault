# IOMMU-facing pointers

> Canonical C topic note — Chapter 45. An IOMMU can translate or restrict device-visible addresses, so a CPU virtual pointer is not necessarily a valid DMA address.

## Definition
A C pointer is meaningful to the CPU's execution environment. A DMA descriptor may instead require an I/O virtual address, bus address, physical address, or device-specific token. The mapping is platform-specific and must not be inferred by casting a pointer.

## Mechanism and language rules
A driver normally asks the platform memory-management layer to map a buffer for a device and receives a device-visible address. The mapping may impose permissions, alignment, lifetime, and synchronization requirements.

### What to reason about
- CPU address space vs device address space.
- Mapping/unmapping lifetime.
- Address width and truncation.
- IOMMU permissions.
- Cache/coherency attributes.
- Whether the mapping survives suspend/reset.

## Embedded implications
IOMMUs are more common in complex SoCs and high-end embedded systems than small MCUs. They can isolate devices and support virtualized or protected DMA, but add mapping setup, TLB behavior, fault handling, and debugging complexity.

### Firmware review angle
Keep device addresses in explicitly typed integer/address abstractions rather than pretending they are ordinary C pointers. Validate that descriptor fields can represent the complete device address range.

## Edge cases and failure modes
- Casting a CPU pointer to `uint32_t` truncates a 64-bit address.
- Device accesses after an IOMMU mapping is removed.
- Permissions reject an otherwise valid CPU buffer.
- Mapping attributes disagree with cache policy.
- Device reset invalidates mappings.

## Example pattern
```c
void submit(void *cpu_buf, size_t len)
{
    dma_addr_t dev_addr = dma_map_for_device(cpu_buf, len);
    program_descriptor(dev_addr, len);
}
```
`dma_addr_t` and mapping operations are platform abstractions, not ISO C constructs.

## Verification / debugging
Log CPU and device addresses separately when debugging mappings. Test invalid permissions, unmap-before-completion, address-width boundaries, and device reset. Inspect IOMMU fault records where available.

## Staff-level takeaway
A device-facing address is **not necessarily a C pointer value**. Treat address-space translation, permissions, lifetime, and cache attributes as explicit parts of the DMA contract.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
