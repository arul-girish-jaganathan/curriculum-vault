# Latency budgeting

> Canonical C topic note — Chapter 44. Interrupt latency is the time from an interrupt-causing event to the required service point. Correct budgeting uses worst-case bounds, not average ISR execution time.

## Definition
A latency budget decomposes a deadline into interrupt recognition, hardware entry, masking delays, higher-priority work, handler execution, deferred processing, and required peripheral response. ISO C does not define any of these timings.

## Mechanism and language rules
Compiler-generated instructions, memory accesses, cache/flash wait states, branches, and function calls contribute to execution time. C semantics permit transformations that preserve observable behavior, so timing must be measured on the actual compiler/target configuration.

### What to reason about
- Maximum interrupt-disabled interval.
- Higher-priority interrupt interference.
- Worst-case ISR path.
- Peripheral synchronization/acknowledgement latency.
- Deferred queue/scheduler delay.
- Measurement uncertainty.

## Embedded implications
Missing a deadline can cause data loss, control instability, FIFO overflow, or safety failure. Budgeting must include bursts and nesting, not just nominal interrupt rates.

### Firmware review angle
Write a latency budget with explicit assumptions and margin. Re-measure after compiler, clock, flash wait-state, RTOS, or driver changes. GPIO timestamps and hardware trace are often more trustworthy than debugger single-stepping.

## Edge cases and failure modes
- Average timing hides rare worst-case paths.
- A logging statement changes the timing under test.
- Interrupt masking in unrelated code consumes the budget.
- Queue backlog converts a short ISR into large end-to-end latency.
- Frequency scaling invalidates cycle-based assumptions.

## Example pattern
```c
void ADC_IRQHandler(void)
{
    uint16_t sample = ADC_DATA;
    clear_adc_irq();
    adc_queue_push_from_isr(sample);
}
```
The ISR's execution time is only one component of the end-to-end sample-processing deadline.

## Verification / debugging
Measure min/max and distribution under worst-case load, including flash/cache state and interrupt nesting. Test maximum event rates and long critical sections. Track the budget in code-review and release criteria.

## Staff-level takeaway
Latency is a **system budget**, not a function-local property. Allocate it across interrupt masking, priority interference, ISR work, deferred processing, and hardware response, then validate the worst case on the production configuration.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
