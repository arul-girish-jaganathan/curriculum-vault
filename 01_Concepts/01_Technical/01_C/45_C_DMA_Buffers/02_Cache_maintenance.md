# Cache maintenance

> Canonical C topic note — Chapter 45. Cache maintenance keeps CPU and DMA views of memory coherent when the platform does not provide hardware coherency. It is a platform concern beyond ISO C.

## Definition
For CPU-to-device transfers, dirty CPU cache lines may need cleaning/write-back before DMA reads memory. For device-to-CPU transfers, stale CPU cache lines may need invalidation before software consumes DMA-written data.

## Mechanism and language rules
C's memory model does not describe CPU caches or DMA. A compiler barrier and a CPU/device memory barrier solve different problems: compiler ordering constrains code generation, while hardware barriers constrain memory-system visibility/order. Cache clean/invalidate operations address cache contents.

### What to reason about
- Is the region cached?
- Is the platform coherent?
- What cache-line size and alignment apply?
- Which direction is the transfer?
- What ordering is required around ownership transfer?
- Could adjacent data in the same cache line be affected?

Do not substitute `volatile` for cache maintenance.

## Embedded implications
Non-coherent Cortex-class SoCs and many peripheral systems require explicit cache APIs. Incorrect maintenance can produce intermittent stale packets or corrupted descriptors, often disappearing in debug builds.

### Firmware review angle
Centralize DMA cache operations and document whether APIs operate on aligned ranges, whole lines, or exact byte ranges. Avoid cleaning a buffer while another owner can modify it.

## Edge cases and failure modes
- Dirty cache not written before device read.
- CPU reads stale cache after device write.
- Invalidate discards unrelated dirty data sharing a cache line.
- Wrong cache-line alignment/range.
- Cache maintenance performed before final CPU writes are complete.

## Example pattern
```c
prepare_tx_buffer(buf, len);
cache_clean_for_device(buf, len);
dma_start_tx(buf, len);
```
For receive buffers, invalidate/synchronize at the documented completion boundary before CPU consumption.

## Verification / debugging
Run tests with caches enabled and disabled. Compare behavior across memory regions and transfer directions. Inspect cache-line alignment and use platform tracing or memory tests to distinguish stale data from actual overwrites.

Staff-level questions: Is the interconnect coherent? What exactly does the cache API guarantee? Which barrier pairs with ownership transfer? Can two logical buffers share a cache line?

## Staff-level takeaway
DMA cache correctness requires **coherency model + cache maintenance + ordering + ownership**. Treat these as one protocol rather than assuming `volatile` or a generic memory barrier is sufficient.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
