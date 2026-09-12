# Interrupt-safe APIs

> Canonical C topic note — Chapter 44. An interrupt-safe API has a documented execution-context contract and avoids operations that are unsafe, blocking, non-reentrant, or unbounded in ISR context.

## Definition
An API is ISR-safe only when its implementation and all callees satisfy the required interrupt constraints. ISO C has no concept of ISR-safe functions.

## Mechanism and language rules
Dangerous operations include blocking synchronization, heap allocation with non-reentrant allocators, unbounded loops, formatted I/O, and functions that use shared mutable state without synchronization. A function's name is not evidence of ISR safety.

### What to reason about
- Does it block?
- Does it acquire a lock that task context can hold?
- Does it allocate/free memory?
- Does it access shared state atomically?
- Is execution bounded?
- Does it touch MMIO with required ordering?

A safe API often has an explicit `_from_isr` variant so the context contract is visible at call sites.

## Embedded implications
RTOS kernels commonly provide specialized ISR APIs that perform a minimal operation and request a context switch after the interrupt returns. Using the ordinary task API can corrupt scheduler state or deadlock.

### Firmware review angle
Maintain a call graph of ISR-reachable functions and classify each as ISR-safe, ISR-forbidden, or conditionally safe. Review transitive dependencies after library changes.

## Edge cases and failure modes
- A logging API allocates internally.
- A mutex is taken from an ISR while its owner is preempted.
- A “nonblocking” function loops until hardware is ready.
- A helper invokes a callback that is not ISR-safe.

## Example pattern
```c
void adc_IRQHandler(void)
{
    uint16_t sample = ADC_DATA;
    clear_adc_irq();
    adc_queue_push_from_isr(sample);
}
```
The suffix documents the intended execution context; the implementation must actually honor it.

## Verification / debugging
Use static call-graph checks, code review annotations, stress tests, and ISR latency measurement. Deliberately trigger the API under interrupt load and queue saturation.

## Staff-level takeaway
ISR safety is a **transitive property of the call graph**. A function is not safe merely because its own body is short; every reachable operation must satisfy the interrupt-context contract.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
