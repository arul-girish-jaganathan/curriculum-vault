# Minimal ISR work

> Canonical C topic note — Chapter 44. ISR work should be minimized to preserve interrupt latency, stack capacity, scheduler responsiveness, and system determinism.

## Definition
A minimal ISR acknowledges the interrupt, captures the smallest necessary state, and signals deferred processing. The exact acceptable work depends on latency and safety requirements, but unbounded processing is generally inappropriate.

## Mechanism and language rules
An ISR interrupts ordinary execution and may execute between any two points permitted by the hardware. Therefore it should avoid assumptions about what shared state is temporarily consistent unless the protocol guarantees them.

### What to reason about
- Interrupt entry/exit overhead.
- Worst-case handler execution time.
- Nesting and priority effects.
- Shared-state atomicity and ordering.
- Peripheral acknowledgement timing.
- Whether a called API is ISR-safe.

## Embedded implications
Long ISRs increase worst-case latency for other interrupts and can cause FIFO overflow, missed sampling deadlines, motor-control jitter, or watchdog problems. Stack usage must include ISR nesting on top of task stack use where applicable.

### Firmware review angle
Use the ISR for capture and acknowledgement; move parsing, logging, protocol handling, and heavy computation to deferred context. Measure worst-case execution rather than relying on average timing.

## Edge cases and failure modes
- Clearing an interrupt too late causes repeated entry.
- Clearing it too early loses an event.
- Doing formatted logging from the ISR blocks or consumes excessive stack.
- Calling a mutex/blocking API deadlocks or corrupts scheduler state.
- Assuming one interrupt corresponds to one event when hardware coalesces events.

## Example pattern
```c
static volatile uint32_t rx_snapshot;
static volatile bool rx_pending;

void RX_IRQHandler(void)
{
    rx_snapshot = UART_RX_REG;
    clear_rx_irq();
    rx_pending = true;
}
```
The deferred context should process the snapshot under an appropriate synchronization protocol.

## Verification / debugging
Measure minimum/maximum/percentile ISR duration, interrupt-to-service latency, and nesting depth. Stress with maximum event rates and simultaneous higher-priority interrupts.

## Staff-level takeaway
“Minimal” means **bounded and sufficient**, not merely short in source lines. Design the ISR/deferred boundary around measurable latency, event-loss behavior, ownership, and stack constraints.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
