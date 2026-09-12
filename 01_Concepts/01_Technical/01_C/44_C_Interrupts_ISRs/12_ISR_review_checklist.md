# ISR review checklist

> Canonical C topic note — Chapter 44. Review an ISR as a hardware-facing concurrency boundary with explicit latency, stack, synchronization, and peripheral contracts.

## Definition
A complete ISR review asks whether the handler is correct for its interrupt architecture, compiler/ABI, peripheral semantics, concurrency model, and real-time budget. ISO C answers only the language-level portion.

## Mechanism and language rules
Review the complete transitive call graph, not just the handler body. Confirm that every shared object has a defined ownership/atomicity model and that every volatile/MMIO access matches the hardware specification.

### What to reason about
- **Entry/exit:** correct interrupt declaration and ABI.
- **Acknowledgement:** source cleared/latched correctly.
- **Latency:** bounded worst-case execution and masking.
- **Stack:** handler frame plus maximum nesting.
- **Synchronization:** atomicity and ordering of shared state.
- **Callees:** no forbidden blocking/allocation/non-reentrant operations.
- **Handoff:** queue/flag ownership and overflow behavior.

## Embedded implications
Verify event rates, queue depth, watchdog interactions, DMA ownership, and power-state behavior. A handler that is functionally correct can still be system-incorrect if it violates latency or stack budgets.

### Firmware review angle
Require measured worst-case timing and stack evidence for critical handlers. Keep target-specific attributes and register definitions centralized. Make diagnostic behavior bounded and ISR-safe.

## Edge cases and failure modes
- Interrupt storms from uncleared sources.
- Lost events due to incorrect clear order.
- Data races hidden by `volatile`.
- Queue overflow ignored.
- Nested interrupts exhausting stack.
- Debugging changes the timing enough to hide the defect.

## Example pattern
```c
void TIMER_IRQHandler(void)
{
    uint32_t status = TIMER_STATUS;
    TIMER_CLEAR = status;
    timer_events_from_isr(status);
}
```
Review the exact clear semantics and whether `status` can contain multiple coalesced events.

## Verification / debugging
Use static call-graph analysis, maximum-load timing tests, interrupt storms, nested-source tests, queue saturation, and stack high-water measurement. Verify generated ISR prologue/epilogue and register access widths.

## Staff-level takeaway
A strong ISR review proves four things: **correct context, bounded latency, safe shared-state handling, and correct hardware interaction**. If any one is uncertain, the handler is not yet production-ready.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
