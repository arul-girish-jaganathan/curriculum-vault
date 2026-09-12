# Zero-copy buffers

> Canonical C topic note — Chapter 45. Zero-copy designs avoid copying payload data between software buffers by transferring ownership or exposing the same storage across processing stages.

## Definition
A zero-copy path can reduce CPU cycles and memory bandwidth, but it requires stronger lifetime and ownership contracts. The fact that two pointers refer to the same storage does not establish who may modify it.

## Mechanism and language rules
C pointers describe addresses into objects; they do not encode ownership or synchronization. A zero-copy API must document whether a buffer is borrowed, transferred, immutable, or retained asynchronously.

### What to reason about
- Who owns the object?
- How long is it valid?
- Is it writable by both producer and consumer?
- Is cache coherence maintained?
- Can the producer reuse it before the consumer completes?
- Does the ABI require alignment or address conversion?

## Embedded implications
Zero-copy can reduce RAM, CPU time, and power, especially for high-rate peripherals. It can also increase fragmentation of ownership logic and expose hardware constraints directly to higher layers.

### Firmware review angle
Use explicit buffer states such as FREE, CPU_OWNED, DMA_OWNED, and COMPLETE. Do not pass stack storage to asynchronous zero-copy operations.

## Edge cases and failure modes
- Use-after-free/lifetime end while DMA still owns the buffer.
- Producer modifies data after publishing it.
- Consumer retains a buffer beyond its ownership interval.
- Cache state is inconsistent.
- Upper layers assume a mutable buffer is private when it is shared.

## Example pattern
```c
typedef struct {
    uint8_t *data;
    size_t len;
    bool immutable;
} buffer_view_t;
```
The structure expresses a view, not ownership; the surrounding API must define lifetime and transfer rules.

## Verification / debugging
Track buffer IDs through every ownership transition. Stress concurrent reuse, early completion, errors, reset, and maximum throughput. Use sanitizers on host equivalents for lifetime bugs.

## Staff-level takeaway
Zero-copy is an **ownership optimization**. It is worthwhile only when the saved copy cost exceeds the added complexity of lifetime, cache, synchronization, and API contracts.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
