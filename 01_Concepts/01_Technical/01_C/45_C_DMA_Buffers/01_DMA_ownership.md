# DMA ownership

> Canonical C topic note — Chapter 45. DMA ownership defines which execution agent may read or modify a buffer at each phase of a transfer. Correct C pointer usage alone cannot establish hardware ownership.

## Definition
A DMA transfer gives a peripheral/DMA engine access to memory while the CPU may otherwise continue executing. Ownership must transition explicitly: CPU-owned -> DMA-owned -> CPU-owned, or through a more detailed descriptor state machine.

## Mechanism and language rules
The pointer passed to DMA is a machine address interpreted by hardware. C object lifetime and pointer validity still matter, but the DMA engine is not a C abstract-machine thread. Synchronization therefore spans C memory semantics, cache/coherency rules, bus fabric, and DMA programming requirements.

### What to reason about
- Who may read/write the buffer now?
- When is ownership transferred?
- Is the buffer still alive and mapped?
- Are cache clean/invalidate operations required?
- What barrier orders descriptor publication before DMA start?
- Can the CPU touch the buffer while DMA owns it?

## Embedded implications
DMA improves CPU efficiency but introduces coherency, lifetime, alignment, and race hazards. A stack buffer is generally unsafe if DMA outlives the function call.

### Firmware review angle
Represent ownership explicitly in driver state. Do not expose a mutable buffer to callers while hardware can still write it. Define completion semantics precisely: interrupt may mean descriptor complete, FIFO consumed, or final bus write visible depending on hardware.

## Edge cases and failure modes
- CPU modifies a buffer while DMA is reading it.
- DMA writes after the C object lifetime ends.
- Cache contains stale CPU data.
- Descriptor is reused before hardware stops using it.
- Peripheral error path fails to return ownership.

## Example pattern
```c
typedef enum { BUF_CPU, BUF_DMA } owner_t;

struct dma_buf {
    uint8_t data[256];
    owner_t owner;
};
```
The enum is only a software model; hardware and cache rules must enforce the actual transition.

## Verification / debugging
Instrument ownership transitions and assert legal state changes. Test early completion, errors, reset during DMA, cache-enabled operation, and maximum transfer lengths.

## Staff-level takeaway
DMA ownership is a **lifetime + concurrency + hardware-address contract**. Make ownership transitions explicit and impossible to bypass casually.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
