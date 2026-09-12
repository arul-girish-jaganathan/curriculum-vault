# Producer-consumer ownership

> Canonical C topic note — Chapter 45. Producer-consumer ownership defines when a producer may write a buffer and when a consumer may read or reuse it. DMA makes the producer/consumer relationship extend across software and hardware.

## Definition
A producer creates or fills data; a consumer processes it. Ownership transfer is the synchronization point that prevents simultaneous conflicting access. In DMA systems, the device can be either producer or consumer.

## Mechanism and language rules
The protocol must establish both **ownership** and **visibility**. An atomic index or flag can establish synchronization, but associated payload must also become visible before the consumer acts on the ownership signal.

### What to reason about
- Who owns the storage at each state?
- Which event transfers ownership?
- What ordering publishes payload before metadata?
- Can ownership be transferred twice?
- What happens if the consumer is delayed?
- Can the producer overrun available storage?

## Embedded implications
Typical states are FREE -> PRODUCER -> READY -> CONSUMER -> FREE. DMA may replace one software actor in this state machine. Buffer depth must cover worst-case producer bursts and consumer stalls.

### Firmware review angle
Make state transitions explicit and define overflow, timeout, and reset behavior. Avoid hidden ownership through raw pointers passed between modules.

## Edge cases and failure modes
- Consumer sees metadata before payload.
- Producer reuses a buffer still owned by consumer.
- Queue full condition is ignored.
- DMA completes after software has reclaimed the buffer.
- Reset leaves a device-owned buffer marked free.

## Example pattern
```c
typedef enum {
    BUF_FREE,
    BUF_PRODUCER,
    BUF_READY,
    BUF_CONSUMER
} state_t;
```
The transitions must be synchronized according to the execution model.

## Verification / debugging
Stress producer bursts, consumer stalls, wraparound, timeouts, and reset. Track buffer IDs and state transitions. For DMA, capture descriptor ownership and cache synchronization alongside software state.

Staff-level questions: What is the ownership invariant? What proves the release event? Can the consumer observe a partially written payload? What is the maximum backlog?

## Staff-level takeaway
Producer-consumer correctness is **ownership plus visibility**. Define legal states and transitions, then prove the ordering and capacity assumptions that make them safe.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
