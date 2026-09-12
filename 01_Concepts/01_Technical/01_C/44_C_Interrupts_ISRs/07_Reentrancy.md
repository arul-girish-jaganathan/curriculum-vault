# Reentrancy

> Canonical C topic note — Chapter 44. A function is reentrant when concurrent or nested invocations can execute safely without corrupting shared state. ISR preemption is a common source of accidental non-reentrancy.

## Definition
A reentrant function can be interrupted and invoked again, or called concurrently, while each invocation preserves its required correctness. Pure functions and functions using only caller-owned state are easier to make reentrant than functions using shared mutable globals or static scratch storage.

## Mechanism and language rules
C permits static storage and shared objects, but concurrent access requires a defined synchronization model. A function with hidden mutable state may be unsafe even if its parameters are independent.

### What to reason about
- Does the function use static/global mutable state?
- Does it call another non-reentrant function?
- Is shared state atomic or protected?
- Can an ISR interrupt the function while it owns a resource?
- Does it use a shared buffer or singleton context?
- Are callbacks invoked in a context that can re-enter the API?

`volatile` does not make a function reentrant.

## Embedded implications
Typical failures include an ISR calling a formatter while a task is using the same static buffer, or an interrupt re-entering a driver while its state machine is mid-update.

### Firmware review angle
Prefer explicit context objects passed by pointer, per-task state, and ISR-specific APIs. If serialization is required, make the lock/context boundary explicit and verify that the ISR can never block on it.

## Edge cases and failure modes
- Static local scratch buffer shared by invocations.
- Global state updated in multiple steps and observed midway.
- Callback re-enters the same module.
- Signal/interrupt interrupts a library routine using shared internal state.

## Example pattern
```c
size_t format_value(char *dst, size_t cap, uint32_t value)
{
    /* Caller-owned storage makes reentrancy easier to reason about. */
    return format_into_buffer(dst, cap, value);
}
```
Avoid hidden module-level scratch buffers when concurrent use is possible.

## Verification / debugging
Call the function concurrently, interrupt it at vulnerable points where the target permits controlled testing, and use ThreadSanitizer for host-thread analogues where applicable. Inspect static/global state and the transitive call graph.

Staff-level questions: What shared state exists below this API? What happens if an ISR re-enters it halfway through? Can state be moved into an explicit context object?

## Staff-level takeaway
Reentrancy is about **hidden mutable state and interruption boundaries**. Make state ownership explicit and design APIs so nested/concurrent execution cannot corrupt shared context.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
