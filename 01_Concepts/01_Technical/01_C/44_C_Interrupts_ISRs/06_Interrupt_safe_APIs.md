# Interrupt-safe APIs

> Canonical C topic note — Chapter 44. An interrupt-safe API has a contract appropriate for interrupt context: bounded execution, no unsafe blocking, valid shared-state handling, correct hardware access, and reentrancy behavior suitable for its callers.

## Definition
“ISR-safe” is not a property of a function name; it is a property of the complete implementation and its transitive callees on a specific platform. A function may be safe from one ISR but unsafe from another if locking, priority, or hardware assumptions differ.

## Mechanism and language rules
Review allocation, locks, static state, recursion, library calls, and shared objects. C does not define interrupt context, so safety depends on the RTOS, ABI, compiler, interrupt controller, and target.

### What to reason about
- Can the function block or wait for an event?
- Can it acquire a lock held by the interrupted context?
- Is its static/global state reentrant?
- Is execution time bounded?
- Are all memory accesses correctly synchronized?
- Does it call a non-reentrant library routine?

## Embedded implications
Many RTOSes provide dedicated `*_from_isr()` APIs because ordinary queue/semaphore operations may manipulate scheduler state or block. Driver APIs should similarly distinguish ISR and thread variants when their contracts differ.

### Firmware review angle
Encode context restrictions in naming, documentation, static-analysis annotations, and API structure. Keep the ISR-safe surface area small and test it independently.

## Edge cases and failure modes
- ISR calls a blocking API.
- Lock is held by the interrupted task.
- Static scratch buffer is shared by nested interrupts.
- Library function uses hidden global state.
- API is fast normally but has an unbounded worst-case path.

## Example pattern
```c
bool ring_push_from_isr(ring_t *r, uint8_t value)
{
    /* Target-specific atomic/index protocol required here. */
    return ring_try_push(r, value);
}
```
The `_from_isr` name is a contract marker, not proof of correctness.

## Verification / debugging
Inspect the complete call graph, stress nested interrupts, and inject queue-full and error conditions. Measure worst-case cycles and stack usage. Test with the scheduler and interrupt priorities configured as in production.

Staff-level questions: What exactly makes this function ISR-safe? Which resources can it touch? What happens if it is re-entered? Can the target implementation introduce a hidden lock?

## Staff-level takeaway
ISR safety is a **transitive contract**. Prove the entire call graph, synchronization model, and timing bound rather than relying on naming conventions or `volatile` variables.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
