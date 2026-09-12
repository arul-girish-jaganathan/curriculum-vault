# Ring buffers

> Canonical C topic note — Chapter 45. A ring buffer provides bounded cyclic storage for producer/consumer traffic. With DMA, correctness additionally requires ownership, cache visibility, descriptor semantics, and hardware wrap behavior.

## Definition
A ring uses storage plus producer and consumer positions. The indices determine which slots are available and which contain data. A full/empty convention must be explicit, such as reserving one slot or maintaining a count.

## Mechanism and language rules
Index arithmetic must avoid invalid array access and unintended signed overflow. Power-of-two capacities can permit efficient masking, but only when the capacity is actually a power of two and the index type is chosen appropriately.

### What to reason about
- What represents full versus empty?
- Can producer and consumer update indices concurrently?
- Are index accesses atomic on the target?
- What memory ordering publishes data before the index?
- Does DMA own slots between producer/consumer transitions?
- What happens on overflow?

## Embedded implications
DMA rings are common for UART, Ethernet, ADC, and storage engines. A ring can eliminate copies but creates precise ownership transitions and cache-management requirements.

### Firmware review angle
Document slot state, index ownership, wrap semantics, capacity, burst tolerance, and overflow policy. Size the ring from worst-case producer/consumer mismatch, not average throughput.

## Edge cases and failure modes
- Full and empty states are ambiguous.
- Index wraps incorrectly.
- Consumer sees index before payload is visible.
- Producer reuses a DMA-owned slot.
- Ring capacity is not a power of two but bitmask indexing is used.

## Example pattern
```c
#define RING_CAP 8U

struct ring {
    uint8_t data[RING_CAP];
    unsigned head;
    unsigned tail;
};

static unsigned next_index(unsigned i)
{
    return (i + 1U) % RING_CAP;
}
```
A concurrent implementation needs explicit atomic/order rules; this example only illustrates wrap arithmetic.

## Verification / debugging
Test zero, one, full, empty, wraparound, burst traffic, and producer/consumer stalls. Add sequence numbers to detect lost or duplicated slots. For DMA, inspect ownership and cache state at each transition.

Staff-level questions: What is the maximum backlog? Can events be dropped? Who owns a slot between indices? Are index publication and payload visibility correctly ordered?

## Staff-level takeaway
A DMA ring is a **bounded ownership protocol**, not merely an array with two counters. Prove full/empty semantics, concurrency, visibility, and worst-case backlog together.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
