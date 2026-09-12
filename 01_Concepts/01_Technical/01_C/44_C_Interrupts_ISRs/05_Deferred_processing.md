# Deferred processing

> Canonical C topic note — Chapter 44. Deferred processing moves non-urgent interrupt work into task/thread context while the ISR performs only time-critical capture and acknowledgement.

## Definition
Common mechanisms include flags, counters, ring buffers, RTOS queues, task notifications, event bits, and bottom-half/work-queue models. The handoff defines an ownership boundary between interrupt and normal execution.

## Mechanism and language rules
The producer and consumer must share state through a defined synchronization mechanism. A plain non-atomic shared variable can create a data race in a C11 concurrent model; `volatile` alone does not provide atomicity or ordering.

### What to reason about
- What data is captured before hardware changes it?
- Who owns the buffer at each stage?
- Can producer and consumer run concurrently?
- What memory ordering publishes the data?
- What happens on queue overflow?
- Is the consumer guaranteed to run before hardware storage is exhausted?

## Embedded implications
Deferred work reduces ISR latency but adds queueing latency. Buffer depth must cover worst-case bursts, not average event rate. Event coalescing is acceptable only when the event semantics permit it.

### Firmware review angle
Document producer rate, consumer service time, queue depth, overflow policy, and maximum end-to-end latency. Keep ISR-to-task synchronization primitives dedicated to that context where possible.

## Edge cases and failure modes
- Queue overflow silently drops data.
- Flag coalesces multiple events when each event matters.
- Consumer reads data before publication is ordered.
- Buffer is reused while DMA/consumer still owns it.
- Deferred task starvation defeats the latency budget.

## Example pattern
```c
static sample_t queue[QUEUE_CAPACITY];

void ADC_IRQHandler(void)
{
    sample_t s = ADC_DATA;
    queue_push_from_isr(s);
}

void adc_task(void)
{
    sample_t s;
    while (queue_pop(&s)) {
        process_sample(s);
    }
}
```
The queue must define atomicity, ownership, overflow, and memory-order semantics.

## Verification / debugging
Stress maximum interrupt bursts, delayed consumers, queue-full conditions, and task preemption. Measure both ISR time and end-to-end event latency. Add counters for dropped/coalesced events.

Staff-level questions: What is the worst burst? Is the queue dimensioned mathematically? Which events can be coalesced? What is the maximum deferred latency?

## Staff-level takeaway
Deferred processing trades **ISR latency for queueing latency and storage**. Size and synchronize the handoff from worst-case rates and make overflow behavior an explicit system contract.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
