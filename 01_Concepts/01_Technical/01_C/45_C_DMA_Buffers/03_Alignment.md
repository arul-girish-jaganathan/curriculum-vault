# Alignment

> Canonical C topic note — Chapter 45. DMA buffers and descriptors often require stronger alignment than ordinary C objects because hardware accesses memory in fixed-width or cache-line-sized transactions.

## Definition
C requires objects to meet their type's alignment requirements. DMA hardware can impose additional constraints: descriptor alignment, buffer alignment, address boundaries, burst boundaries, or cache-line alignment. These hardware requirements are outside ISO C.

## Mechanism and language rules
Use `_Alignas`/`alignas` or target-specific attributes when the C object must have stronger alignment. Correct alignment does not guarantee DMA addressability, physical contiguity, or cache coherence.

### What to reason about
- What alignment does the C type require?
- What alignment does the DMA engine require?
- Does the linker place the object in a DMA-accessible memory region?
- Are cache-line boundaries relevant?
- Can the address be represented by the DMA descriptor format?

## Embedded implications
A correctly aligned buffer in ordinary RAM may still be inaccessible to a DMA engine if it resides in tightly coupled memory, external memory with unsuitable attributes, or a protected region. Alignment and placement must be specified together.

### Firmware review angle
Use linker sections and linker assertions to guarantee placement and alignment. Centralize DMA buffer declarations so future changes cannot silently move them into incompatible memory.

## Edge cases and failure modes
- Descriptor starts at an invalid alignment.
- Buffer crosses a hardware boundary with special restrictions.
- Cache maintenance rounds down/up to lines and touches neighbors.
- Over-alignment changes RAM footprint or linker placement.
- Casting an unaligned byte pointer to a wider object pointer causes misaligned access.

## Example pattern
```c
struct dma_desc {
    uint32_t addr;
    uint32_t len;
};

_Alignas(32) struct dma_desc descriptors[8];
```
The `32` is illustrative; the required value must come from the hardware/platform contract.

## Verification / debugging
Inspect the linker map and runtime address. Assert alignment with `_Static_assert` where compile-time known, and test actual DMA operation under cache-enabled and boundary-address conditions.

## Staff-level takeaway
DMA alignment is a **three-way contract: C object alignment, linker placement, and hardware DMA constraints**. Satisfying only one layer is insufficient.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
