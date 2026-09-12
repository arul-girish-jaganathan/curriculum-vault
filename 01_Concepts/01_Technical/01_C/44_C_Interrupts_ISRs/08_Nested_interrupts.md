# Nested interrupts

> Canonical C topic note — Chapter 44. Nested interrupts occur when a higher-priority interrupt preempts an active handler. They improve responsiveness but multiply stack, latency, synchronization, and reentrancy complexity.

## Definition
Whether nesting occurs depends on interrupt masking, priority configuration, CPU architecture, and handler policy. C itself has no interrupt nesting semantics.

## Mechanism and language rules
On preemption, hardware and/or software saves the interrupted context. The nested handler executes, then the previous context resumes. The exact saved frame, priority rules, tail chaining, and return sequence are architecture-specific.

### What to reason about
- Which priorities may preempt which handlers?
- What context is saved at each nesting level?
- Are shared resources reentrant?
- What is the maximum nesting depth?
- Can a lower-priority ISR hold a resource needed by a higher-priority ISR?
- What happens if an interrupt source remains asserted?

## Embedded implications
Nesting can reduce response latency for urgent events but increases worst-case stack use and makes timing less deterministic. Interrupt storms can create starvation where normal task execution receives insufficient CPU time.

### Firmware review angle
Define priority levels based on deadlines and bounded execution. Calculate worst-case nesting rather than measuring only nominal depth. Keep high-priority handlers especially short.

## Edge cases and failure modes
- Stack exhaustion from deep nesting.
- Priority inversion through shared state.
- Non-reentrant helper called from nested handlers.
- Interrupt source not acknowledged, causing repeated entry.
- Critical section masks an interrupt longer than its deadline.

## Example pattern
```c
void HIGH_PRIORITY_IRQHandler(void)
{
    capture_urgent_event();
}

void LOW_PRIORITY_IRQHandler(void)
{
    capture_deferred_event();
}
```
The priority relationship is target configuration, not C syntax.

## Verification / debugging
Force worst-case nesting and measure stack high-water mark and response latency. Verify priority configuration against the design document and test interrupt storms.

Staff-level questions: What is the maximum nesting depth? Which resources cross priority levels? Is every high-priority handler bounded even when preempting another ISR?

## Staff-level takeaway
Nested interrupts trade **latency for complexity and stack consumption**. Establish a mathematically defensible priority/nesting policy and design shared state for the resulting preemption model.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
