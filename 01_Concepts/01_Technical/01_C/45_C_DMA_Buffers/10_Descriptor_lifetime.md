# Descriptor lifetime

> Canonical C topic note — Chapter 45. A DMA descriptor must remain valid and hardware-visible for the entire interval in which the device may access it.

## Definition
C object lifetime is defined by storage duration and object creation rules. DMA adds a hardware lifetime requirement: the device may retain an address after the initiating C function returns. Therefore stack allocation is dangerous for asynchronous descriptors unless completion is guaranteed before scope exit.

## Mechanism and language rules
The CPU writes descriptor fields, transfers ownership, and starts hardware. The descriptor cannot be reused, moved, freed, or repurposed until hardware completion/error/reset has definitively released ownership.

### What to reason about
- Storage duration of descriptor and buffers.
- Hardware completion semantics.
- Cache visibility.
- Reset/abort behavior.
- Whether descriptors are reused from a pool.
- Address stability for the hardware-visible mapping.

## Embedded implications
Static pools or dedicated DMA memory are common. Dynamic allocation complicates fragmentation and lifetime; stack allocation is unsuitable when DMA may outlive the function call.

### Firmware review angle
Represent descriptor states explicitly and ensure every error path returns ownership. A peripheral reset may be required before descriptors can safely be reused after a failed transfer.

## Edge cases and failure modes
- Function returns while DMA still references a stack object.
- Descriptor pool slot reused before completion.
- Cache contains stale ownership fields.
- DMA abort leaves a descriptor partially consumed.
- Firmware reset occurs without stopping the peripheral.

## Example pattern
```c
status_t start_dma(struct dma_desc *desc)
{
    prepare_desc(desc);
    transfer_ownership_to_dma(desc);
    dma_start(desc);
    return STATUS_OK;
}
```
The caller must not modify or release `desc` until the documented completion event transfers ownership back.

## Verification / debugging
Test normal completion, timeout, abort, reset, power-cycle, and descriptor reuse. Instrument ownership and descriptor IDs to detect use-after-release.

## Staff-level takeaway
DMA lifetime extends beyond the C call when hardware retains an address. Treat **descriptor lifetime and ownership as one invariant** and prove release before reuse.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
