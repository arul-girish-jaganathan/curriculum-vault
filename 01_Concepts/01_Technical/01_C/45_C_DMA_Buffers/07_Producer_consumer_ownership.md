# Producer-consumer ownership

> Canonical C topic note — Chapter 45. Producer-consumer ownership defines when one agent may write a buffer and when another may read or reuse it.

## Definition
A producer creates or fills data; a consumer reads/processes it. With DMA, either side can be hardware. Correctness requires explicit transfer points and synchronization.

## Mechanism and language rules
Publishing data requires ordering the data writes before the ownership/index update. Consuming requires observing the ownership update before reading the data. C atomics can provide ordering between software threads/agents, but hardware DMA may require platform-specific barriers and cache maintenance.

### What to reason about
- What is the publication event?
- Which agent writes the ownership state?
- Is ownership state atomic?
- Are data accesses ordered relative to ownership?
- Can the consumer modify storage before the producer releases it?

## Embedded implications
Typical pipelines are ISR/DMA -> queue -> task or CPU -> DMA -> peripheral. Double/triple buffering can maintain throughput while one buffer is processed and another is transferred.

### Firmware review angle
Calculate buffer capacity from worst-case service latency and producer rate. Define behavior when the consumer falls behind: drop, backpressure, overwrite, or fault.

## Edge cases and failure modes
- Ownership flag observed before payload is visible.
- Buffer reused before hardware completion.
- Producer and consumer both mutate shared metadata.
- Queue overflow silently loses data.

## Example pattern
```c
/* Conceptual state machine: FREE -> PRODUCING -> READY -> CONSUMING -> FREE */
typedef enum { FREE, PRODUCING, READY, CONSUMING } buffer_state_t;
```
The transitions, not the enum itself, establish correctness.

## Verification / debugging
Instrument state transitions and assert that only legal transitions occur. Stress maximum rates, delayed consumers, errors, reset, and concurrent completion.

## Staff-level takeaway
Producer-consumer correctness is a **protocol of ownership plus visibility**. Model the states explicitly and prove that no agent accesses a buffer outside its ownership interval.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
