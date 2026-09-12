# Minimal ISR work

> Canonical C topic note — Chapter 44. An ISR should perform the minimum work required to capture/acknowledge the event and hand it to a context designed for longer processing.

## Definition
Minimal ISR work usually includes reading the required hardware state, clearing/acknowledging the source, recording bounded data, and signaling deferred processing. Parsing, allocation, complex logging, and lengthy computation normally belong outside the interrupt context.

## Mechanism and language rules
The C language does not impose an ISR execution limit, but target interrupt latency does. Every function called by an ISR contributes to its worst-case execution time, stack usage, and reentrancy requirements.

### What to reason about
- What must happen before the interrupt source can be safely acknowledged?
- How much data must be captured before hardware overwrites it?
- Is the work bounded for every input?
- Are all callees nonblocking and ISR-safe?
- Can events arrive faster than deferred processing consumes them?

## Embedded implications
A short ISR reduces interrupt latency and nesting pressure. It can copy a timestamp/sample, acknowledge a peripheral, and push a small record into a ring buffer. The deferred worker can perform protocol parsing or expensive computation.

### Firmware review angle
Set an explicit ISR cycle and stack budget. Review the transitive call graph and queue-overflow policy. Avoid `printf`, dynamic allocation, and unbounded loops unless the platform explicitly proves them safe.

## Edge cases and failure modes
- Clearing the source before capturing required data loses information.
- ISR performs too much work and causes lower-priority starvation.
- Queue fills and the ISR silently drops critical events.
- A called function takes a lock held by the interrupted context.

## Example pattern
```c
void ADC_IRQHandler(void)
{
    uint16_t sample = ADC_DATA;
    ADC_CLEAR = ADC_IRQ_FLAG;
    adc_push_from_isr(sample);
}
```
The queue primitive and register semantics are target-specific; the example illustrates the short-capture/handoff pattern.

## Verification / debugging
Measure worst-case cycles, not average time. Stress maximum interrupt rates and queue saturation. Use static call-graph analysis and stack measurement. Verify event loss behavior explicitly.

Staff-level questions: What work is truly time-critical? What is the minimum capture state? What happens when producer rate exceeds consumer rate?

## Staff-level takeaway
A good ISR is a **fast boundary between hardware urgency and software processing**. Capture only what must not be lost, acknowledge correctly, and defer everything else under an explicit overflow and latency contract.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
