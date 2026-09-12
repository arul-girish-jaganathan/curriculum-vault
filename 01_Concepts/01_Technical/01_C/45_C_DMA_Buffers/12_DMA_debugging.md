# DMA debugging

> Canonical C topic note — Chapter 45. DMA failures require simultaneous reasoning about C objects, descriptor layout, ownership, cache visibility, address translation, interrupts, and peripheral state. The CPU call stack alone is incomplete evidence.

## Definition
DMA debugging identifies why device reads/writes differ from software expectations. The DMA engine is an independent bus master, so the causal path can continue after the CPU function returns.

## Mechanism and language rules
A useful timeline is: identify/allocate buffer -> prepare data -> synchronize cache -> build descriptor -> publish ownership -> start DMA -> transfer -> completion/error -> synchronize for CPU -> consume -> release/reuse. Each transition is a possible fault boundary.

### What to reason about
- Buffer address, length, alignment, and lifetime.
- Descriptor bytes as actually visible to hardware.
- Ownership state.
- Cache state and barriers.
- CPU versus device address mapping.
- Completion semantics.
- Abort/reset behavior.

## Embedded implications
Common symptoms include stale data, missing packets, corrupted buffers, descriptor loops, and failures only with cache or optimization enabled. Debugger memory windows can be misleading when caches or other bus masters are involved.

### Firmware review angle
Capture descriptor snapshots, buffer addresses, lengths, ownership bits, sequence numbers, and error status. Use deterministic patterns and one-descriptor tests before adding ring complexity.

## Edge cases and failure modes
- DMA reads stale descriptor contents from cache.
- CPU reuses a buffer before completion.
- Length exceeds the real object/buffer.
- CPU-valid address is device-invalid.
- Completion is observed before payload visibility is synchronized.
- Device continues after a software timeout.

## Example pattern
```c
fill_pattern(buf, len);
cache_clean_for_device(buf, len);
program_dma(buf, len);
start_dma();
/* wait for documented completion */
cache_invalidate_for_cpu(buf, len);
verify_pattern(buf, len);
```
The synchronization helpers are platform-specific and represent the ownership/visibility boundaries.

## Verification / debugging
Begin with one buffer and one descriptor. Verify address, length, alignment, ownership, cache state, and completion. Then test bursts, wraparound, descriptor reuse, timeout, abort, reset, and concurrent traffic.

Use sequence numbers and known patterns to distinguish stale data, overwrite, wrong address, and ordering failures. Correlate CPU logs with peripheral/bus trace when available.

Staff-level questions: Which agent wrote the bad bytes? What did the device actually see? Is the descriptor lifetime valid? What evidence separates cache, ownership, address, and silicon faults?

## Staff-level takeaway
DMA debugging is a **distributed memory-visibility and ownership problem**. Build a precise timeline of who owns and can see each object, then reduce complex transfers to the smallest reproducible hardware transaction.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
