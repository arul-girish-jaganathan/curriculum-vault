# ISR constraints

> Canonical C topic note — Chapter 44. An interrupt service routine (ISR) executes in an execution context imposed by the target interrupt architecture. ISO C does not define ISRs, interrupt attributes, interrupt priorities, or latency semantics.

## Definition
An ISR is code entered asynchronously in response to a hardware/software interrupt. The target ABI/compiler defines how the handler is declared and how context is saved/restored. The C body must obey stronger constraints than ordinary task code because it can interrupt arbitrary program state.

## Mechanism and language rules
An ISR may run with interrupts masked or partially enabled, on a dedicated exception stack, or using the interrupted stack. Hardware may automatically save registers and status state. Compiler attributes can change prologue/epilogue generation and must match the startup/vector-table mechanism.

### What to reason about
- What state is automatically saved by hardware?
- Which registers does the ISR compiler convention preserve?
- Can the ISR nest or be preempted?
- Which shared objects can it access?
- Is every access atomic and correctly synchronized?
- Can the ISR block, allocate, or call non-reentrant code?

`volatile` may be required for MMIO or certain shared flags, but it is not a general substitute for atomicity or synchronization.

## Embedded implications
ISR execution consumes latency budget, stack, CPU time, and potentially power. Long handlers increase worst-case interrupt latency and can cause lower-priority interrupts to miss deadlines.

### Firmware review angle
Keep ISR work bounded and minimal. Move parsing, formatting, allocation, and complex state machines into deferred context unless the architecture explicitly requires otherwise.

## Edge cases and failure modes
- Calling a blocking RTOS API from an ISR.
- Using a non-reentrant library function from interrupt context.
- Updating multiword shared state without atomicity.
- Assuming interrupt entry saves all registers used by ordinary C.
- Failing to acknowledge/clear the source, causing an interrupt storm.

## Example pattern
```c
static volatile bool rx_pending;

void UART_IRQHandler(void)
{
    clear_rx_irq();
    rx_pending = true;
}
```
The main/deferred context should perform substantial processing according to the system's synchronization rules.

## Verification / debugging
Measure entry-to-exit cycles under worst-case conditions, including nesting. Review compiler-generated ISR prologue/epilogue and stack use. Test interrupt storms, simultaneous sources, and recovery from malformed peripheral state.

## Staff-level takeaway
An ISR is a **hardware/ABI execution boundary**, not merely a fast C function. Its contract must cover context, latency, stack, shared-state synchronization, peripheral acknowledgement, and permitted callees.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
