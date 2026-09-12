# ISR review checklist

> Canonical C topic note — Chapter 44. Review an ISR as a hardware-facing concurrency boundary with explicit entry/exit, latency, stack, synchronization, and peripheral contracts.

## Definition
A complete ISR review asks whether the handler is correct for its interrupt architecture, ABI, compiler configuration, hardware semantics, concurrency model, and worst-case real-time budget. ISO C covers only the language portion.

## Mechanism and language rules
Review the complete transitive call graph. Confirm shared objects have defined ownership/atomicity, volatile/MMIO accesses match the device specification, and the interrupt declaration uses the required target mechanism.

### What to reason about
- **Entry/exit:** correct interrupt calling convention and context.
- **Acknowledgement:** source is captured and cleared correctly.
- **Latency:** bounded worst-case execution and masking.
- **Stack:** hardware frame, compiler frame, calls, and nesting.
- **Synchronization:** atomicity and ordering of shared state.
- **Callees:** no forbidden blocking, allocation, or non-reentrant operations.
- **Handoff:** queue/flag ownership and overflow behavior.

## Embedded implications
Check event rates, burst behavior, DMA ownership, watchdog interaction, low-power modes, and peripheral reset behavior. Functional correctness is insufficient if the ISR violates latency or stack limits.

### Firmware review angle
Require timing and stack evidence for critical handlers. Keep target-specific attributes and register definitions centralized. Make diagnostics bounded and interrupt-safe.

## Edge cases and failure modes
- Uncleared source causes an interrupt storm.
- Incorrect clear order loses coalesced events.
- `volatile` hides a race without solving it.
- Queue overflow is ignored.
- Nested handlers exhaust stack.
- Debugger halting changes timing enough to hide a defect.

## Example pattern
```c
void TIMER_IRQHandler(void)
{
    uint32_t status = TIMER_STATUS;
    TIMER_CLEAR = status;
    timer_events_from_isr(status);
}
```
Review whether the register clear is write-one-to-clear, whether reading status has side effects, and whether multiple events can be represented in `status`.

## Verification / debugging
Use static call-graph analysis, worst-case timing tests, interrupt storms, nested-source tests, queue saturation, and stack high-water measurement. Inspect generated prologue/epilogue and register access widths.

Staff-level questions: Is the context correct? What is the worst-case latency? Which shared state is touched? What happens when the producer outruns the consumer? What evidence proves stack margin?

## Staff-level takeaway
A production-ready ISR review proves **context correctness, bounded latency, safe shared-state handling, and correct hardware interaction**. All four are necessary.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
