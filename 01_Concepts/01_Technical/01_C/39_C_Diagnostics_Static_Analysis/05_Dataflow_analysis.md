# Dataflow analysis

> Canonical C topic note — chapter 39.

## Definition
Dataflow analysis computes facts about values and program states as control flows through a program. It underpins many compiler warnings and static-analysis checks.

## Mechanism and language rules
Typical analyses include reaching definitions, live variables, constant propagation, nullability, range analysis, taint flow, and use-before-initialization. Path-sensitive tools maintain different facts for different branches and may merge them conservatively at joins.

## Embedded implications
Dataflow analysis can expose error paths, unchecked lengths, stale state, missing initialization, and resource leaks in complex firmware. It is particularly useful where hardware-driven control flow creates many states.

## Edge cases and failure modes
- Analysis imprecision at aliasing or function-pointer boundaries.
- Assuming a warning proves an actual runtime failure.
- Missing configuration macros causing false paths.
- Ignoring interprocedural effects.

## Verification / debugging
Reduce critical findings to small reproductions and inspect the paths reported by the tool. Compare analyzer assumptions with the actual API contracts and hardware model.

## Staff-level takeaway
Learn to read the *proof path* behind a finding: which assumptions, definitions, branches, and aliases caused the analyzer to reach its conclusion. That makes triage faster and suppressions safer.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
