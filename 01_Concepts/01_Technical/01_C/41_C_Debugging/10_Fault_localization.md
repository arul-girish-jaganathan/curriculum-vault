# Fault localization

> Canonical C topic note — Chapter 41. Fault localization narrows a failure from symptom to the smallest defensible region of code, state, time, or hardware interaction. It is an evidence-driven process, not simply finding the instruction where a fault surfaced.

## Definition
A fault is localized when evidence identifies where an incorrect state or behavior was introduced or first became observable. In C firmware, the visible crash site can be downstream of the actual defect: an out-of-bounds write may corrupt a pointer, and the pointer may fault much later.

## Mechanism and language rules
Use a narrowing loop: establish the symptom, define invariants, capture state, divide the possible causal region, add the least intrusive instrumentation, and repeat. C semantics determine whether candidate operations are defined; compiler output determines how those operations execute.

### What to reason about
- What invariant was violated first?
- Which component last owned the corrupted object?
- Is the failure deterministic, probabilistic, or load/timing-dependent?
- Is the apparent fault address consistent with the instruction and access size?
- Could UB, data races, lifetime errors, or hardware faults invalidate the hypothesis?

Binary search is often effective: add checkpoints around major stages, reproduce, and narrow the first checkpoint after which the invariant fails.

## Embedded implications
Use GPIO markers, monotonic counters, compact event IDs, trace, watchdog breadcrumbs, and fault records for failures that cannot tolerate a breakpoint. Timestamp sources must be understood: CPU cycle counters, RTOS ticks, peripheral timers, and wall-clock time have different semantics.

DMA and interrupts complicate localization because the writer may be outside the current C call stack. Memory ownership and bus activity must therefore be part of the fault model.

### Firmware review angle
Avoid instrumentation that changes scheduling enough to remove the bug. Prefer fixed-cost counters or binary event records over large formatted logs in hard real-time paths. Build feature flags so diagnostic instrumentation can be enabled without changing unrelated code generation when possible.

## Edge cases and failure modes
- **Crash site ≠ root cause.** The faulting load/store may merely expose prior corruption.
- **Heisenbug:** instrumentation changes timing and hides the failure.
- **Wraparound:** finite counters make naive timestamp comparisons wrong.
- **Multiple faults:** a first memory error can trigger a secondary watchdog reset.
- **Optimization:** source stepping can obscure the actual instruction boundary.

## Example pattern
```c
ASSERT(buffer != NULL);
ASSERT(length <= BUFFER_CAPACITY);

record_event(EVENT_BEFORE_COPY, length);
copy_payload(buffer, data, length);
record_event(EVENT_AFTER_COPY, length);
```
The useful question is not merely whether the copy faults, but whether the invariant was already false before the copy and whether `length` is validated against the actual destination capacity.

## Verification / debugging
Define a concrete hypothesis and a falsifiable prediction for each experiment. Correlate source, disassembly, stack/register state, event history, and ownership. Once localized, remove temporary instrumentation and reproduce using a permanent regression test or targeted assertion.

Staff-level questions:
- What is the earliest proven bad state?
- Which observation separates competing hypotheses?
- What is the least perturbing experiment?
- Can the discovered invariant become a permanent test or runtime guard?

## Staff-level takeaway
Good localization finds the **first violated invariant**, not merely the last instruction executed. The Staff-level goal is to convert the incident into a reproducible mechanism and a durable prevention measure.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
