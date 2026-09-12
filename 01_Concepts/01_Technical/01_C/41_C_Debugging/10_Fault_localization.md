# Fault localization

> Canonical C topic note — Chapter 41. Fault localization narrows a failure from symptom to the earliest violated invariant or smallest defensible causal region. The instruction where a fault surfaces is often not where the defect originated.

## Definition
Fault localization is the evidence-driven process of identifying where and when incorrect state or behavior was introduced. A buffer overrun may corrupt a pointer, and the pointer may fault thousands of instructions later. Localization therefore means finding the earliest useful causal boundary, not merely the final crash site.

## Mechanism and language rules
Use a narrowing loop: establish the symptom, define invariants, capture state, divide the candidate region, add the least-perturbing observation, reproduce, and repeat. C semantics determine whether candidate operations are defined; compiler transformations determine the machine-level path.

### What to reason about
- What invariant was first violated?
- Who owned the object immediately before corruption?
- Is the failure deterministic, probabilistic, load-dependent, or timing-dependent?
- Does the fault address match the instruction's access size and operands?
- Could UB, a data race, lifetime error, DMA write, or hardware fault explain the same symptom?
- Does instrumentation change the schedule or memory layout?

Binary search over execution stages is often effective: record bounded checkpoints and identify the first checkpoint after which the invariant fails.

## Embedded implications
Use GPIO markers, event IDs, monotonic counters, watchdog breadcrumbs, trace, and persistent crash records when breakpoints are too intrusive. DMA and interrupts require treating memory ownership as part of the causal graph because the writer may not appear in the current C stack.

### Firmware review angle
Instrumentation must have a defined CPU, RAM, flash, bandwidth, and latency budget. Prefer fixed-size binary events over formatted logs in hard real-time paths. Make diagnostic builds selectable without accidentally changing unrelated optimization or scheduling assumptions.

## Edge cases and failure modes
- **Crash site is downstream:** earlier memory corruption is the actual defect.
- **Heisenbug:** instrumentation removes or creates the failure.
- **Counter wrap:** naive timestamp comparisons become wrong.
- **Multiple faults:** the first fault triggers a secondary watchdog or reset fault.
- **Optimization:** source stepping hides the actual instruction boundaries.

## Example pattern
```c
ASSERT(buffer != NULL);
ASSERT(length <= BUFFER_CAPACITY);
record_event(EVENT_BEFORE_COPY, length);
copy_payload(buffer, data, length);
record_event(EVENT_AFTER_COPY, length);
```
The important evidence is whether the invariant was already false before the copy and whether the bound corresponds to the real destination capacity.

## Verification / debugging
For every experiment, write a hypothesis and a falsifiable prediction. Correlate source, disassembly, registers, stack, event history, ownership, and hardware activity. Once localized, encode the discovered invariant as a test, assertion, static-analysis rule, or design contract.

Staff-level questions: What is the earliest proven bad state? Which experiment separates competing hypotheses? What is the least perturbing measurement? How can the root cause be prevented from recurring?

## Staff-level takeaway
Good localization finds the **first violated invariant**, not merely the last instruction executed. The Staff-level outcome is a reproducible mechanism plus a durable prevention or detection strategy.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
