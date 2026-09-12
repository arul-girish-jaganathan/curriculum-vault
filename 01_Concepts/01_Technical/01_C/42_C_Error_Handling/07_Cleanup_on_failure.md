# Cleanup on failure

> Canonical C topic note — Chapter 42. Cleanup-on-failure ensures resources acquired before an error are released or returned to a known state before control leaves a function.

## Definition
C has no automatic destructor mechanism. Resource cleanup must be encoded explicitly through control flow. Common patterns use a single cleanup section, reverse-order release, helper functions, or structured status handling.

## Mechanism and language rules
Every acquisition creates an obligation. If acquisition A succeeds and acquisition B fails, the function must undo A before returning unless ownership has deliberately transferred elsewhere.

### What to reason about
- What resources have been acquired at each point?
- In what order must they be released?
- Is cleanup itself fallible?
- Can the same resource be released twice?
- Does cleanup run on every exit path?
- Does the compiler's control-flow transformation preserve the defined semantics?

A common C idiom uses `goto cleanup;` because it gives one auditable cleanup path without duplicating release logic. This is often safer than deeply nested conditionals.

## Embedded implications
Resources include clocks, IRQ enables, mutexes, DMA channels, buffers, peripheral ownership, power rails, and hardware configuration—not only heap memory. Cleanup may need to restore registers and disable interrupts in the correct order.

### Firmware review angle
For real-time systems, define whether cleanup has a bounded worst-case duration. Do not perform blocking cleanup from ISR context. For hardware, distinguish “disable” from “restore previous state.”

## Edge cases and failure modes
- Double-free or double-release after partially initialized state.
- Cleanup assumes an initialization step that failed.
- Cleanup order violates hardware dependencies.
- Error path forgets a resource introduced by a later code change.
- Cleanup failure overwrites the original error without preserving context.

## Example pattern
```c
status_t start(void)
{
    status_t st = STATUS_OK;
    bool clock_on = false;
    bool irq_on = false;

    if (clock_enable() != STATUS_OK) { st = STATUS_IO; goto cleanup; }
    clock_on = true;
    if (irq_enable() != STATUS_OK) { st = STATUS_IO; goto cleanup; }
    irq_on = true;

cleanup:
    if (irq_on)  { irq_disable(); }
    if (clock_on) { clock_disable(); }
    return st;
}
```
The state flags make partial acquisition explicit and cleanup idempotent with respect to this function's path.

## Verification / debugging
Inject failure after each acquisition and verify that every resource is released exactly once. Add assertions for ownership state in debug builds and use static analysis for leak/double-release patterns.

Staff-level questions:
- Is every acquisition paired with a release?
- Is reverse-order cleanup required?
- What if cleanup itself fails?
- Can the cleanup path be shared safely across future changes?

## Staff-level takeaway
Prefer **one auditable cleanup strategy** over clever control flow. Model resources as obligations and make partial initialization states explicit so that every failure path is deterministic and reviewable.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
