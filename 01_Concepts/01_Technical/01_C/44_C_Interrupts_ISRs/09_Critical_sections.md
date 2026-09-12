# Critical sections

> Canonical C topic note — Chapter 44. A critical section protects an invariant from the concurrency event that could otherwise violate it. Disabling interrupts is only one target-specific mechanism.

## Definition
A critical section is a bounded sequence during which selected concurrency sources are prevented from interfering. Implementations may use interrupt masking, locks, atomics, scheduler suspension, or hardware transaction primitives.

## Mechanism and language rules
Protection must cover the whole invariant, not merely one statement. A `volatile` object can still be changed between two C operations. Atomicity and memory ordering are separate concerns from compiler-visible volatility.

### What to reason about
- Which execution agents are excluded?
- Does another core or DMA remain active?
- What is the maximum protected duration?
- Is nesting supported?
- Is the previous interrupt state restored correctly?
- Are memory barriers required at the boundary?

## Embedded implications
Disabling interrupts can protect a single-core shared RAM update from ISR interference but increases interrupt latency. Locks preserve interrupt responsiveness but can introduce contention, deadlock, and priority inversion.

### Firmware review angle
Choose the narrowest mechanism sufficient for the actual writer set. Save/restore prior interrupt state rather than blindly enabling interrupts on exit. Measure maximum disabled time and lock hold time.

## Edge cases and failure modes
- Critical section is too long.
- Early return leaves interrupts disabled.
- Nested sections restore the wrong mask.
- DMA/other core modifies state despite interrupt masking.
- ISR attempts to acquire a task-held lock.

## Example pattern
```c
uint32_t key = irq_save();
shared_count++;
irq_restore(key);
```
The primitives are target-specific and must preserve the caller's previous interrupt state.

## Verification / debugging
Instrument entry/exit and measure worst-case duration. Stress nested interrupts and every failure path. Verify that the protection covers all actual writers, not just the CPU contexts visible in the source.

Staff-level questions: What invariant is protected? Which agents can violate it? What is the worst-case latency cost? Is a lock, atomic operation, or hardware primitive better?

## Staff-level takeaway
A critical section is a **concurrency boundary with a measurable latency cost**. Protect the invariant, identify every competing agent, and prove both correctness and worst-case duration.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
