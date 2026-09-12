# Volatile DMA status

> Canonical C topic note — Chapter 45. DMA status handling requires separating compiler-visible access, hardware ownership, cache coherence, atomicity, and ordering. `volatile` addresses only a narrow part of this problem.

## Definition
`volatile` can be appropriate for MMIO or memory that changes independently of normal program flow, but it does not make a DMA protocol atomic, coherent, or synchronized. The status representation must be interpreted according to the hardware contract.

## Mechanism and language rules
For MMIO status registers, volatile preserves required compiler-visible accesses. For DMA descriptors in RAM, applying `volatile` to the entire object is not automatically correct; cache maintenance and ownership protocols may be more important.

### What to reason about
- Is status stored in MMIO or RAM?
- Who writes it and at what width?
- When is it guaranteed visible to CPU?
- Does reading clear/acknowledge the status?
- Is the payload visible before completion metadata?
- Are cache lines coherent?

## Embedded implications
A device can update RAM while the CPU cache contains an old descriptor. Conversely, invalidating a cache line can discard unrelated CPU-owned data if ownership is not controlled.

### Firmware review angle
Define a completion protocol: device writes payload, updates completion metadata, signals completion; software synchronizes visibility, validates status, consumes payload, and returns ownership.

## Edge cases and failure modes
- `volatile` added while cache remains stale.
- CPU sees completion before payload visibility.
- Status read clears an event unexpectedly.
- Multiword status is observed during a hardware update.

## Example pattern
```c
struct dma_status {
    uint32_t length;
    uint32_t flags;
};

static struct dma_status status;
```
Do not add `volatile` mechanically; derive the access model from the platform and hardware specification.

## Verification / debugging
Test cache-enabled and cache-disabled configurations, repeated completions, partial transfers, and error status. Capture raw descriptor bytes and correlate them with device completion events.

Staff-level questions: Who writes the status? What proves visibility? Does reading have side effects? Is the status atomic at the device's access width?

## Staff-level takeaway
For DMA status, always ask **who writes, who observes, when visibility is guaranteed, and what reading means**. `volatile` is only one piece of that protocol.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
