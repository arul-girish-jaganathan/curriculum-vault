# Volatile DMA status

> Canonical C topic note — Chapter 45. DMA status fields that software observes through shared memory or MMIO require careful separation of compiler visibility, hardware ownership, and synchronization.

## Definition
`volatile` can be appropriate for memory that may change independently from ordinary program flow, but it does not make a DMA status protocol atomic, coherent, or ordered. A DMA completion indication must be interpreted according to the hardware contract.

## Mechanism and language rules
For MMIO status registers, `volatile` preserves required compiler-visible accesses. For DMA descriptors in RAM, whether a field needs `volatile` is a design-specific question; cache maintenance and synchronization often matter more. Marking an entire descriptor volatile can impose unnecessary compiler traffic without solving cache coherency.

### What to reason about
- Is the status in MMIO or RAM?
- Who writes it?
- Is the write atomic at the hardware access width?
- When is it guaranteed visible to the CPU?
- Does reading it acknowledge/clear hardware state?

## Embedded implications
A status bit can be set by DMA while the CPU cache still contains an old descriptor. Conversely, CPU reads may see stale payload unless invalidation occurs. Completion ordering must cover both descriptor/status and payload.

### Firmware review angle
Define a completion protocol: DMA writes payload, updates completion metadata, raises interrupt; CPU synchronizes visibility, validates completion, consumes payload, and returns ownership.

## Edge cases and failure modes
- `volatile` added but cache remains stale.
- CPU observes completion before payload visibility.
- Status read clears a hardware event unexpectedly.
- Multiword status is read while hardware updates it.

## Example pattern
```c
struct dma_status {
    uint32_t length;
    uint32_t flags;
};

/* Visibility/ownership rules must be established around this object. */
static struct dma_status status;
```
Do not add `volatile` mechanically; derive qualifiers from the actual access model.

## Verification / debugging
Test cache-enabled operation, repeated completion, partial transfers, and error status. Inspect memory before/after cache maintenance and correlate hardware completion with CPU observations.

## Staff-level takeaway
For DMA status, ask **who writes, who observes, when visibility is guaranteed, and what reading means**. `volatile` answers only one part of that chain.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
