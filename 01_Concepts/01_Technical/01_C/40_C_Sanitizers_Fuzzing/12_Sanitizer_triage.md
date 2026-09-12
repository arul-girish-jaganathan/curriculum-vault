# Sanitizer triage

## Definition
**Sanitizer triage** is the disciplined process of turning a sanitizer report into a minimized, understood, fixed, and permanently tested defect. A sanitizer finding is evidence of a violated runtime property; triage determines the actual root cause and scope.

## Scope and boundaries
Do not assume the first crashing instruction is the root cause. Heap corruption, use-after-free, and undefined arithmetic can propagate until a later operation triggers a report. Sanitizer output must be interpreted together with source, ownership, control flow, and test input.

## Mechanism and language rules
A useful sequence is:

```text
report -> classify -> reproduce -> minimize -> root cause -> fix
       -> regression test -> broaden search for variants
```

Classify the finding as memory safety, arithmetic UB, race, leak, or another instrumented defect. Preserve the exact toolchain and runtime configuration used to reproduce it.

## Embedded implications
When a host sanitizer finds a parser overflow, inspect equivalent target code and neighboring APIs for the same contract violation. A fix that only changes the host harness is insufficient. For target-only faults, correlate sanitizer-like evidence with hardware watchpoints, MPU faults, stack guards, trace, and register state.

## Edge cases and failure modes
- Fixing the symptom instead of ownership/lifetime root cause.
- Losing the original input after minimization.
- Treating nondeterministic reports as harmless.
- Running with a different sanitizer configuration and concluding the bug disappeared.
- Fixing one instance while the same unsafe API pattern exists elsewhere.

## Verification / debugging
Make the report reproducible, reduce the input, identify the violated C rule, and add a regression test that fails without the fix. Re-run under multiple relevant sanitizer modes. Search the codebase for the same pattern and review the API contract that allowed it.

## Performance, memory, timing and power
Sanitizer configurations are usually too expensive for production firmware. Their value is accelerated discovery and diagnosis. After a fix, verify the optimized target build separately because instrumentation can alter layout and timing.

## Staff-level takeaway
A sanitizer report should create **permanent engineering knowledge**: root cause, violated contract, regression test, and prevention mechanism. The goal is not merely to make the current run green.