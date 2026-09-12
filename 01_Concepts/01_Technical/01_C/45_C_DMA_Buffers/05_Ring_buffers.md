# Ring buffers

> Canonical C topic note — Chapter 45. A ring buffer uses fixed storage with wrapping producer/consumer positions. DMA integration adds ownership, cache, memory-ordering, and hardware wrap semantics.

## Definition
A ring has a finite array plus producer and consumer indices. Correctness depends on a precise full/empty convention and on which execution agent owns each slot.

## Mechanism and language rules
For a single-producer/single-consumer design, separate indices can often avoid locks if atomicity and memory ordering are correct. The C memory model must be respected for concurrent software agents; DMA hardware requires additional synchronization beyond C.

### What to reason about
- Is capacity power-of-two or arbitrary?
- Can indices wrap safely?
- Which agent writes each index?
- When is data considered published?
- Can DMA overwrite an unconsumed slot?
- What happens on full/empty?

## Embedded implications
Ring buffers are ideal for UART, SPI, ADC, network, and logging streams. DMA can fill a circular buffer while software consumes completed regions. Cache maintenance and interrupt/coalescing behavior become part of the protocol.

### Firmware review angle
Prefer monotonic counters with explicit width and modulo reasoning. Define overflow behavior and maximum producer lead. Avoid relying on signed integer wraparound.

## Edge cases and failure modes
- Producer overtakes consumer and overwrites unread data.
- Index wrap is confused with full/empty.
- Consumer reads data before DMA completion.
- Cache invalidation is omitted.
- ISR and task update the same index without synchronization.

## Example pattern
```c
#define RING_CAP 256U
static uint8_t ring[RING_CAP];
static atomic_uint write_pos;
static atomic_uint read_pos;
```
The actual memory-order protocol must be designed with the producer/consumer ownership model.

## Verification / debugging
Test empty, one-item, full, wraparound, burst, overrun, reset during transfer, and maximum producer/consumer skew. Instrument sequence numbers to detect drops and duplication.

## Staff-level takeaway
A DMA ring is a **streaming ownership protocol**, not merely an array with modulo arithmetic. Prove capacity, index, publication, cache, and overflow semantics together.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
