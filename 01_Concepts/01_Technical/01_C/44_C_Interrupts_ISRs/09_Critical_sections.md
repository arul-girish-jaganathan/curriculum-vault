# Critical sections

> Canonical C topic note — Chapter 44. A critical section is a region protected against the concurrency event that could violate its invariants. Disabling interrupts is only one target-specific implementation.

## Definition
A critical section protects a sequence of operations so another execution context cannot interfere in an unsafe way. C does not define critical sections; implementations use interrupt masking, locks, atomics, scheduler suspension, or hardware primitives.

## Mechanism and language rules
Protection must cover the complete invariant, not just one C statement. A `volatile` access remains visible to the compiler but does not prevent another context from interleaving between multiple operations.

### What to reason about
- Which context is being excluded?
- Is interrupt masking sufficient if another core/DMA can modify state?
- What is the maximum critical-section duration?
- Is nesting supported and are previous interrupt states restored?
- Are memory-ordering barriers required?

## Embedded implications
Disabling interrupts can guarantee atomicity against interrupt handlers on a single core, but increases interrupt latency. Locking can preserve responsiveness but introduces contention and deadlock risk.

### Firmware review angle
Use the narrowest protection mechanism that covers the actual concurrency model. Save/restore the previous interrupt mask rather than blindly enabling interrupts on exit. Measure worst-case disabled-interrupt duration.

## Edge cases and failure modes
- Critical section too long, causing missed deadlines.
- Early return leaves interrupts disabled.
- Nested critical sections restore the wrong mask.
- DMA/another core changes memory despite interrupt masking.
- Lock acquisition from ISR deadlocks.

## Example pattern
```c
uint32_t state = irq_save();
shared_count++;
irq_restore(state);
```
The save/restore operations are target-specific and must preserve the caller's prior interrupt state.

## Verification / debugging
Instrument entry/exit and measure maximum duration. Stress nested interrupts and fault paths. Review every exit path and verify that the protection primitive matches all possible writers.

## Staff-level takeaway
A critical section is a **concurrency boundary with a latency cost**. Define the invariant, identify every competing execution agent, choose the smallest sufficient protection, and prove its worst-case duration.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
