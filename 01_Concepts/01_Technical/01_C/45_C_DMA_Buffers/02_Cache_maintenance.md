# Cache maintenance

> Canonical C topic note — Chapter 45. Cache maintenance keeps CPU-visible and DMA-visible memory coherent on systems where caches are not automatically coherent with the DMA master.

## Definition
For a CPU writing a DMA source buffer, cache clean/write-back operations may be required before DMA reads it. For DMA-written memory, cache invalidation may be required before the CPU consumes it. Exact operations are architecture and cache-policy specific.

## Mechanism and language rules
C's memory model does not define hardware cache coherency. `volatile` does not flush caches. Compiler barriers do not necessarily perform cache maintenance, and CPU memory barriers do not necessarily clean or invalidate caches.

### What to reason about
- Is the region cacheable?
- Is the DMA master coherent?
- What cache line size and alignment apply?
- Must clean/invalidate cover complete lines?
- What ordering is required before starting or after completing DMA?

## Embedded implications
Partial-line maintenance can corrupt unrelated data when cache operations operate at line granularity. Non-cacheable DMA pools simplify coherency at the cost of access latency and memory-region constraints.

### Firmware review angle
Centralize cache/DMA synchronization APIs and document ownership transitions. Do not scatter architecture-specific cache instructions throughout drivers.

## Edge cases and failure modes
- CPU reads stale cache after DMA completion.
- CPU dirty cache overwrites newer DMA data later.
- Cleaning an incorrectly aligned range affects neighboring objects.
- Assuming coherent behavior on one MCU family and porting to a non-coherent system.

## Example pattern
```c
prepare_dma_for_device(buf, len); /* architecture-specific */
start_dma(buf, len);
wait_for_completion();
prepare_dma_for_cpu(buf, len);    /* architecture-specific */
consume(buf, len);
```
The helper boundaries should hide cache-line and barrier details.

## Verification / debugging
Test with caches enabled and deliberately use patterns that expose stale data. Inspect cache-line alignment and memory attributes. Compare behavior using coherent and non-coherent mappings where the platform supports both.

## Staff-level takeaway
DMA cache handling is a **memory-visibility protocol**, not a C qualifier problem. Separate cache maintenance, compiler ordering, CPU barriers, and hardware ownership, and implement each at the correct abstraction layer.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
