# ISR constraints

> Canonical C topic note — Chapter 44. An interrupt service routine is hardware-triggered execution with target-specific entry/exit rules and strict latency, stack, concurrency, and API constraints. ISO C does not define ISRs.

## Definition
An ISR executes in response to an interrupt source. The CPU and interrupt controller determine recognition, priority, context stacking, masking, nesting, and return semantics; the compiler provides the required interrupt calling convention through target-specific mechanisms.

## Mechanism and language rules
The ISR body is C code, but its calling convention differs from an ordinary function on many targets. Entry may save architectural registers automatically; compiler-generated prologue/epilogue may save additional state. The handler must obey the target ABI and interrupt declaration rules.

### What to reason about
- Which hardware context is saved automatically?
- What registers/flags must the compiler preserve?
- What interrupts remain enabled during the handler?
- Which shared objects can the ISR access?
- Are operations bounded and nonblocking?
- Are all transitive callees ISR-safe?

`volatile` is not a substitute for atomicity, ordering, or mutual exclusion.

## Embedded implications
Long handlers increase interrupt latency and can cause FIFO overflow, missed deadlines, or interrupt storms. Dynamic allocation, blocking calls, unbounded loops, formatted logging, and non-reentrant library functions are generally unsuitable unless the platform explicitly provides safe variants.

### Firmware review angle
Review the entire call graph and hardware interaction. Define a maximum execution time, maximum stack consumption, nesting policy, shared-state protocol, and deferred-work mechanism.

## Edge cases and failure modes
- Incorrect interrupt attribute corrupts return state.
- ISR calls a function that waits for an event it has prevented from running.
- Long critical sections cause missed interrupts.
- Shared multi-byte state is read non-atomically.
- Fault handler has insufficient stack.

## Example pattern
```c
void UART_IRQHandler(void)
{
    uint32_t status = UART_STATUS;
    UART_CLEAR = status;
    uart_event_push_from_isr(status);
}
```
The exact declaration, register semantics, and queue primitive are target-specific.

## Verification / debugging
Measure worst-case latency and stack use under maximum interrupt rates. Review every transitive callee for blocking, allocation, locking, and reentrancy. Test interrupt storms and nested handlers.

Staff-level questions: What is the maximum interrupt-off time? What is the longest ISR path? What hardware events can arrive concurrently? Where is deferred work executed?

## Staff-level takeaway
An ISR is a **hardware-facing concurrency boundary**. Keep it short, bounded, context-correct, and explicit about ownership; defer substantial work to normal execution context.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
