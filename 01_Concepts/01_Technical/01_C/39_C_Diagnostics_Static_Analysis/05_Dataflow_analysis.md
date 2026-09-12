# Dataflow analysis

## Definition
**Dataflow analysis** derives facts about program states as information flows through a control-flow graph. It is a foundation of many compiler optimizations and static-analysis checks, including reaching definitions, live variables, constant propagation, nullness, range analysis, and use-before-initialization detection.

## Scope and boundaries
Analysis results are generally conservative approximations. A tool may model all feasible paths imperfectly, especially with function pointers, concurrency, inline assembly, dynamic configuration, or unknown external behavior.

## Mechanism and language rules
A program is represented as basic blocks connected by control-flow edges. An analysis computes facts entering and leaving blocks until the equations stabilize. Conceptually:

```text
entry facts -> transfer(block) -> exit facts -> successor blocks
```

For example, after `x = 5`, a constant-propagation analysis can record that `x` is known to be 5 until a possible write invalidates that fact.

### Path sensitivity
A path-sensitive analysis distinguishes conditions such as:

```c
if (p != NULL) {
    use(*p);
}
```

inside the true branch. Path-insensitive analysis may merge states and produce less precise results.

## Embedded implications
Dataflow analysis can identify error paths, stale state, impossible branches, missing initialization, range violations, and resource-handling defects in firmware. It can also reason about state-machine transitions and configuration-dependent paths that are difficult to exercise on hardware.

## Edge cases and failure modes
- Analyzer assumes a function never changes memory when it actually does.
- Interrupt/concurrency effects are absent from the model.
- Macros and generated code alter control flow from what the developer expects.
- Pointer aliasing makes dataflow facts less precise.
- A “possible” path is reported that hardware guarantees cannot occur, or a real path is missed because the model is incomplete.

## Verification / debugging
When a finding appears, inspect the control-flow path reported by the analyzer and verify each assumption. Create a minimal test case when necessary. Feed the analyzer the exact compile commands and target configuration so type widths and macros match production.

## Performance, memory, timing and power
Dataflow analysis has no target runtime cost. It can be computationally expensive, but its ability to find defects before execution is especially valuable for expensive-to-test embedded paths.

## Staff-level takeaway
Understand the analysis model behind a warning. A Staff engineer should be able to ask **which fact was inferred, across which paths, under which assumptions, and where those assumptions differ from the hardware contract**.