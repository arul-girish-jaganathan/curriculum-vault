# Descriptor lifetime

> Canonical C topic note — Chapter 45. A DMA descriptor must remain valid, correctly mapped, and hardware-visible for the entire interval during which the device may access it.

## Definition
C object lifetime follows storage duration and object rules. DMA adds a hardware-use lifetime because a device may retain an address after the initiating C function returns. Therefore storage duration must cover the complete asynchronous operation.

## Mechanism and language rules
Software prepares a descriptor, synchronizes its fields, transfers ownership, and starts hardware. The descriptor must not be modified, moved, freed, or reused until completion/error/reset definitively releases ownership.

### What to reason about
- Storage duration of descriptor and referenced buffers.
- Device completion semantics.
- Mapping lifetime and address stability.
- Cache visibility.
- Abort/reset behavior.
- Pool reuse policy.

## Embedded implications
Static or dedicated DMA pools are common. Stack allocation is unsafe when DMA may outlive the function. Dynamic allocation adds fragmentation and failure modes. Peripheral reset may be required before ownership can safely return after an abort.

### Firmware review angle
Model descriptor states explicitly and define the release event. Never infer release merely from a software timeout unless the hardware contract proves DMA has stopped.

## Edge cases and failure modes
- Function returns while DMA references a stack object.
- Pool slot is reused before completion.
- Cache contains stale ownership fields.
- Abort leaves the descriptor partially consumed.
- Firmware resets while the peripheral is still active.

## Example pattern
```c
status_t start_dma(struct dma_desc *desc)
{
    prepare_desc(desc);
    DMA_SYNC_FOR_DEVICE(desc);
    transfer_ownership_to_dma(desc);
    dma_start(desc);
    return STATUS_OK;
}
```
The caller must retain the descriptor until the documented completion/release event.

## Verification / debugging
Test normal completion, timeout, abort, reset, power-cycle, and immediate reuse. Track descriptor IDs and ownership transitions to detect use-after-release.

Staff-level questions: What exact event proves hardware no longer references the descriptor? Does reset guarantee release? Can a stale descriptor remain in the device after software thinks it is free?

## Staff-level takeaway
DMA lifetime can outlive the initiating C call. Treat **descriptor lifetime, buffer lifetime, address mapping, and ownership** as one invariant and prove release before reuse.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
