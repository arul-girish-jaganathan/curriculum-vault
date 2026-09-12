# Nested interrupts

> Canonical C topic note — Chapter 44. Nested interrupts occur when a higher-priority interrupt preempts an ISR that is already executing. The behavior is target-specific and must be analyzed as an interrupt-priority and stack-depth problem.

## Definition
With nesting enabled, interrupt context can form a stack: task -> ISR A -> ISR B -> ... . Hardware and startup/runtime code determine what state is saved at each entry. ISO C does not define nesting.

## Mechanism and language rules
Nested execution increases the number of active contexts and therefore stack consumption. Shared state may be accessed by several priority levels, creating ordering and atomicity requirements beyond ordinary task/ISR interaction.

### What to reason about
- Which priorities can preempt which?
- Are interrupts masked during critical portions?
- How much hardware/software context is saved per nesting level?
- Can the same peripheral generate nested events?
- Are shared structures safe under priority-based preemption?

## Embedded implications
Worst-case interrupt latency and stack use must include maximum nesting. A lower-priority ISR can be delayed by repeated high-priority events, causing starvation or deadline misses.

### Firmware review angle
Define a maximum nesting depth and verify it under worst-case interrupt arrival. Keep high-priority handlers extremely bounded. Avoid calling complex shared services from multiple interrupt priorities without an explicit serialization strategy.

## Edge cases and failure modes
- Stack overflow due to unexpected nesting.
- Priority inversion/starvation from interrupt storms.
- Shared data updated by multiple priority levels without atomicity.
- Interrupt source not cleared, causing recursive re-entry.
- Debugging hides nesting because halting suppresses or changes interrupt behavior.

## Example pattern
```c
void HIGH_IRQHandler(void)
{
    capture_urgent_event();
    clear_high_irq();
}

void LOW_IRQHandler(void)
{
    queue_event_from_isr();
    clear_low_irq();
}
```
The actual priority and nesting policy is configured outside ISO C and must be verified against the MCU architecture.

## Verification / debugging
Measure worst-case nesting with trace or GPIO instrumentation. Test simultaneous interrupt sources and sustained high-priority load. Validate stack high-water marks and exception-frame decoding.

## Staff-level takeaway
Nested interrupts are fundamentally a **worst-case resource analysis problem** involving priority, latency, stack, and shared state. Average interrupt behavior is not sufficient evidence for correctness.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
