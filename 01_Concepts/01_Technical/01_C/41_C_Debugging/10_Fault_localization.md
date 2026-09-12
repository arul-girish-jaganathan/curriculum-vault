# Fault localization

> Canonical C topic note — chapter 41.

## Definition
Fault localization narrows a failure from a broad symptom to the smallest code path, state transition, memory operation, or hardware interaction responsible for violating an expected invariant. It is distinct from identifying the crash site.

A useful separation is:

- **failure site:** where the system becomes observably wrong;
- **fault site:** where an invalid action or state transition occurs;
- **root cause:** the design, implementation, integration, or process condition that allowed it.

## Mechanism and language rules
C debugging is strongest when hypotheses are expressed as invariants:

- pointers refer to valid live objects;
- array indexes stay within bounds;
- lengths are representable and validated;
- objects are initialized before use;
- alignment requirements are satisfied;
- aliasing/lifetime rules are respected;
- shared state has the required synchronization;
- state machines accept only legal transitions;
- resource ownership is unique or explicitly shared.

Consider:

```c
if (len <= sizeof(rx_buf)) {
    memcpy(rx_buf, src, len);
}
```
The check is useful, but if `len` is already corrupted the key localization question is where it first ceased to satisfy its invariant.

### Binary search and temporal localization
Localization can operate across:

- code revisions using `git bisect`;
- execution phases using checkpoints/markers;
- data flow using guards and validation points;
- configuration matrices using feature toggles;
- timing windows using trace timestamps.

The goal is to reduce a large search space into a controlled experiment.

## Embedded implications
Asynchronous execution agents complicate localization. Consider interrupts, DMA engines, peripherals, multicore accesses, watchdogs, reset controllers, and low-power transitions.

For timing-sensitive faults, heavy logging can destroy causality. Prefer compact event IDs, timestamps, counters, GPIO markers, hardware trace, or fixed-size ring buffers.

For memory corruption, combine guard patterns with ownership metadata and targeted watchpoints. For hardware interactions, capture the relevant peripheral status before it is destroyed by clear-on-read behavior.

### Example
A HardFault occurs in a copy routine. A weak conclusion is “copying caused the crash.” A stronger localization sequence is:

```text
fault PC → exact instruction → source/destination/length
→ object lifetime/bounds → writer history → ownership transition
→ first invalid value → violated invariant
```

## Edge cases and failure modes
- The first visible failure can be far downstream from the original corruption.
- Instrumentation can alter timing or memory layout.
- A debugger can suppress a race.
- Optimization differences can change failure probability.
- A symptom-fix can leave the violated invariant intact.
- Multiple independent defects can produce the same signature.
- Statistical failures require distinguishing correlation from causation.

## Verification / debugging
Build a minimal reproduction whenever possible. Capture state immediately before and after the suspected transition. Use host sanitizers and assertions for memory/contract violations, static analysis for structural defects, debugger watchpoints for CPU writers, and hardware tracing for asynchronous behavior.

For regression defects, automate a deterministic test and use `git bisect`. For intermittent defects, collect enough samples to quantify failure probability and vary one causal factor at a time.

The strongest confirmation is a controlled intervention: remove the suspected cause and observe that the failure disappears, then inject the same invalid condition in a test environment and reproduce the original signature.

## Staff-level takeaway
Fault localization is uncertainty reduction. Senior debugging does not accumulate guesses; it partitions the search space until one violated invariant explains the complete evidence. A root-cause claim should survive an independent experiment and should identify the preventive control that will catch or eliminate the defect earlier.

## Related
[[00_Chapter_Index]]
[[09_Post_mortem_analysis]]
[[11_Debugger_scripting]]
[[../26_C_Lifetime_Aliasing/00_Chapter_Index]]
[[../39_C_Diagnostics_Static_Analysis/00_Chapter_Index]]
[[../40_C_Sanitizers_Fuzzing/00_Chapter_Index]]
