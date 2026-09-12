# Fault localization

> Canonical C topic note — chapter 41.

## Definition
Fault localization narrows a failure from a broad symptom to the smallest code, state transition, or hardware interaction responsible for violating an expected invariant. It is different from simply identifying the crash site.

## Mechanism and language rules
Use a hypothesis-driven process. Define the observable symptom, identify invariants, collect evidence, and bisect the execution path. For C, useful invariants include pointer validity, buffer bounds, object lifetime, ownership, initialization, state-machine legality, integer ranges, alignment, and synchronization.

A useful distinction is:
- **failure site:** where the system becomes observably wrong;
- **fault site:** where the invalid action occurs;
- **root cause:** the design/process condition that allowed it.

Example: a HardFault in `memcpy` may be the failure site; the fault may be an invalid length computed earlier; the root cause may be a protocol parser lacking a checked length invariant.

## Embedded implications
Localization must account for asynchronous agents: interrupts, DMA, peripherals, other cores, watchdogs, and power transitions. A value can become corrupt without a corresponding C statement in the current thread.

Useful techniques include binary search over revisions, feature flags, tracepoints, watchpoints, guard patterns, CRCs, GPIO timing markers, fault injection, and controlled reproduction. For timing bugs, preserve event ordering and latency information rather than adding heavy logging.

### Example
```c
if (len <= sizeof(rx_buf)) {
    memcpy(rx_buf, src, len);
}
```
If `len` is corrupt, the key question becomes where `len` first became invalid—not merely whether this check exists.

## Edge cases and failure modes
- The first visible symptom may be far downstream from corruption.
- Instrumentation can perturb races and timing.
- Reproduction may depend on optimization, memory placement, or interrupt load.
- A debugger stop can suppress the failure.
- Overly broad logging can obscure the causal sequence.
- Fixing the symptom can leave the violating invariant intact.

## Verification / debugging
Create a minimal reproduction. Capture before/after values around the suspected transition. Use assertions and sanitizers on host builds, static analysis for structural defects, watchpoints for CPU writes, and hardware trace/instrumentation for asynchronous behavior.

For regressions, use `git bisect` with a deterministic test. For nondeterministic failures, classify runs statistically and identify which conditions increase failure probability. Verify the proposed root cause by making one controlled change that removes the failure and, ideally, by injecting the suspected fault to reproduce the same signature.

## Staff-level takeaway
Fault localization is an evidence pipeline. Senior engineers reduce uncertainty systematically rather than making increasingly complex guesses. The strongest conclusion explains the symptom, identifies the earliest invalid transition, names the violated invariant, and has an independent experiment that confirms causality.

## Related
[[00_Chapter_Index]]
[[09_Post_mortem_analysis]]
[[11_Debugger_scripting]]
[[../39_C_Diagnostics_Static_Analysis/00_Chapter_Index]]
[[../40_C_Sanitizers_Fuzzing/00_Chapter_Index]]
