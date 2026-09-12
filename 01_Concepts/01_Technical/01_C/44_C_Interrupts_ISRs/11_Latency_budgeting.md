# Latency budgeting

> Canonical C topic note — Chapter 44. Interrupt latency is a system-level deadline budget from an external event to the required response. Average timing is insufficient; worst-case interference must be included.

## Definition
A latency budget decomposes response time into interrupt recognition, hardware entry, interrupt masking, higher-priority work, handler execution, synchronization, deferred processing, and peripheral response. ISO C defines none of these timing properties.

## Mechanism and language rules
Compiler output, instruction scheduling, memory accesses, cache/flash wait states, branches, calls, and synchronization primitives determine actual execution. The production compiler and target configuration therefore matter.

### What to reason about
- Maximum interrupt-disabled duration.
- Higher-priority interference.
- Worst-case handler path.
- Peripheral acknowledgement/synchronization time.
- Queue and scheduler delay.
- Clock/frequency changes.
- Measurement uncertainty and instrumentation overhead.

A budget should include margin rather than targeting exactly the deadline.

## Embedded implications
Missing latency can overflow hardware FIFOs, destabilize control loops, lose communication frames, or violate safety timing. Burst rates and nested interrupts matter more than nominal periodic rates.

### Firmware review angle
Write the budget as explicit assumptions and measurements. Re-measure after compiler, clock, RTOS, flash wait-state, driver, or priority changes. Prefer GPIO timestamps, cycle counters, trace, or hardware timers over debugger stepping for timing evidence.

## Edge cases and failure modes
- Average timing hides rare worst-case paths.
- Logging changes the schedule.
- Unrelated critical sections consume the budget.
- Deferred queue backlog dominates end-to-end latency.
- Dynamic frequency scaling invalidates fixed cycle assumptions.

## Example pattern
```c
void ADC_IRQHandler(void)
{
    uint16_t sample = ADC_DATA;
    ADC_CLEAR = ADC_IRQ_FLAG;
    adc_queue_push_from_isr(sample);
}
```
ISR execution is only one component of the sample-to-processing deadline.

## Verification / debugging
Measure distributions and worst-case values under maximum CPU, interrupt, and communication load. Include nesting and longest critical sections. Validate event-rate assumptions and queue depth.

Staff-level questions: What is the deadline? Which components consume the budget? What is the worst-case interference? How much margin remains after measurement uncertainty?

## Staff-level takeaway
Latency is a **system budget**, not a property of one ISR. Allocate it across masking, priority interference, handler work, deferred processing, and hardware response, then prove the worst case on the production configuration.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
