# Deferred processing

> Canonical C topic note — Chapter 44. Deferred processing separates urgent interrupt capture from substantial work performed later in task or scheduler context.

## Definition
The ISR records an event and schedules or signals a deferred handler. Common mechanisms include queues, ring buffers, task notifications, event flags, software interrupts, and RTOS work queues.

## Mechanism and language rules
The boundary requires a safe handoff. Data captured by the ISR must remain valid until the consumer finishes. A flag, index, or queue operation must obey the concurrency model; `volatile` alone is insufficient for general synchronization.

### What to reason about
- Is the queue operation ISR-safe?
- What happens when the queue is full?
- Can events be coalesced or lost?
- Is ordering preserved?
- Who owns the buffer after enqueue?

## Embedded implications
Deferred processing improves interrupt latency but moves work into task latency and queueing constraints. A producer faster than the consumer eventually fills finite storage. The overflow policy must be explicit: drop newest, drop oldest, merge events, raise an alarm, or reset.

### Firmware review angle
Size queues from worst-case burst rate, not average rate. Account for scheduler latency and higher-priority work. For hard real-time systems, derive a bound on backlog and processing time.

## Edge cases and failure modes
- Queue overflow silently drops critical events.
- ISR writes into a buffer before the consumer has finished reading it.
- Deferred handler runs after the hardware state has changed.
- Priority inversion or starvation delays processing.

## Example pattern
```c
struct event { uint16_t id; uint16_t data; };

void TIMER_IRQHandler(void)
{
    clear_timer_irq();
    queue_push_from_isr((struct event){EVENT_TICK, 0});
}
```
The queue API must explicitly support ISR context and define full-queue behavior.

## Verification / debugging
Stress burst rates, queue-full conditions, nested interrupts, scheduler delays, and consumer stalls. Measure interrupt latency and event age from capture to processing.

## Staff-level takeaway
Deferred processing is a **rate-matching and ownership boundary**. It is correct only when event capacity, overflow policy, synchronization, and worst-case service latency are explicitly engineered.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
