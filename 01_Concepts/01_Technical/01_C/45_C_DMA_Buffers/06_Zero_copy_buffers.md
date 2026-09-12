# Zero-copy buffers

> Canonical C topic note — Chapter 45. Zero-copy designs let data move between producer and consumer without unnecessary CPU copying, but they transfer complexity into ownership, lifetime, alignment, cache, and synchronization contracts.

## Definition
A zero-copy path passes a buffer reference from one component or hardware agent to another. The producer must not modify or reuse the buffer until ownership is returned.

## Mechanism and language rules
A C pointer only identifies storage in the CPU's address space. For DMA, the device may require a mapped address and specific memory attributes. The object's lifetime must extend through every asynchronous user.

### What to reason about
- Who owns the buffer now?
- Can producer and consumer overlap access?
- Is the buffer CPU- and device-visible?
- Are alignment and cache constraints satisfied?
- Does the consumer retain the pointer asynchronously?
- What is the release event?

## Embedded implications
Zero-copy can reduce CPU cycles, RAM bandwidth, and latency, but may increase buffer-pool size and fragmentation pressure. Cache maintenance can erase some of the expected performance benefit.

### Firmware review angle
Use explicit buffer states such as FREE, CPU, DMA, and CONSUMER. Keep ownership transitions observable in debug builds and define timeout/reset behavior for stuck owners.

## Edge cases and failure modes
- Buffer reused before DMA completion.
- CPU writes while device reads.
- Cache line sharing causes stale or lost data.
- Device address mapping is invalid after reset.
- Pool exhaustion creates hidden blocking.

## Example pattern
```c
typedef enum {
    BUF_FREE,
    BUF_DMA,
    BUF_CPU
} buf_state_t;

struct buffer {
    uint8_t data[1536];
    buf_state_t state;
};
```
The state machine is only a model; synchronization and hardware mapping remain platform-specific.

## Verification / debugging
Measure copy elimination against cache and synchronization costs. Stress buffer starvation, delayed completion, reset, and error paths. Add sequence IDs and ownership assertions.

Staff-level questions: What cost was actually removed by zero-copy? What new lifetime and cache obligations were introduced? Is a bounded copy simpler and fast enough?

## Staff-level takeaway
Zero-copy is a **complexity trade**, not a free optimization. Choose it when measured copy cost justifies the stronger ownership, cache, lifetime, and debugging contracts.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
