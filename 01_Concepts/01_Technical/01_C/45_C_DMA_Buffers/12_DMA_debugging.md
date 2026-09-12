# DMA debugging

> Canonical C topic note — Chapter 45. DMA failures require simultaneous reasoning about C objects, hardware descriptors, ownership, cache visibility, address translation, interrupts, and peripheral state.

## Definition
DMA debugging identifies why a device read/write differs from software expectations. The CPU call stack alone is insufficient because the DMA engine is an independent bus master.

## Mechanism and language rules
A useful timeline is: allocate/identify buffer -> prepare data -> synchronize cache -> build descriptor -> publish ownership -> start DMA -> device transfers -> completion/error -> synchronize for CPU -> consume -> release/reuse. Each transition is a possible defect boundary.

### What to reason about
- Buffer address and size.
- Descriptor contents as seen by hardware.
- Ownership state.
- Cache state and barriers.
- Alignment and memory region.
- Completion semantics.
- Reset/abort behavior.

## Embedded implications
Typical symptoms include stale data, missing packets, corrupted buffers, descriptor loops, sporadic faults, and failures only when optimization/cache is enabled. Debugger memory views can mislead when cache or another bus master is involved.

### Firmware review angle
Capture descriptor snapshots, buffer addresses, lengths, ownership bits, and sequence numbers. Use known patterns to distinguish stale data from overwrite and address errors. If possible, use bus/peripheral trace rather than halting the CPU.

## Edge cases and failure modes
- DMA uses a stale descriptor due to cache.
- CPU reuses a buffer too early.
- Length exceeds the actual object/buffer.
- Address is valid to CPU but invalid to device.
- Completion interrupt is acknowledged before all required visibility synchronization.
- Device continues after software timeout.

## Example pattern
```c
fill_pattern(buf, len);
cache_clean_for_device(buf, len);
program_dma(buf, len);
start_dma();
/* wait for completion */
cache_invalidate_for_cpu(buf, len);
verify_pattern(buf, len);
```
The helpers are platform-specific and represent the required visibility boundaries.

## Verification / debugging
Start with deterministic patterns and one descriptor. Validate address, length, alignment, ownership, cache maintenance, and completion before adding ring complexity. Then test bursts, wraparound, errors, reset, and concurrent traffic.

Staff-level questions:
- Which agent wrote the bytes that are wrong?
- What did the device actually see?
- Is the descriptor lifetime valid?
- What evidence distinguishes cache, ownership, address, and hardware faults?

## Staff-level takeaway
DMA debugging is a **distributed memory-visibility problem**. Build a timeline of ownership and visibility, inspect what hardware—not just the CPU debugger—could see, and reduce complex rings to a minimal reproducible transfer before diagnosing higher-level code.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
