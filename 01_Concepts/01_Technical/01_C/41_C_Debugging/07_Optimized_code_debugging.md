# Optimized-code debugging

> Canonical C topic note — chapter 41.

## Definition
Optimized-code debugging is the practice of diagnosing a program while accounting for transformations performed by the compiler and linker. Optimization may preserve C's required observable behavior while radically changing instruction order, variable locations, control flow, inlining, stack layout, and the relationship between source lines and machine instructions.

The correct goal is not to force optimized code to look like `-O0`; it is to understand the optimized execution precisely enough to prove or disprove the failure hypothesis.

## Mechanism and language rules
Common transformations include:

- constant propagation and folding;
- dead-code elimination;
- common-subexpression elimination;
- loop transformations;
- instruction scheduling;
- register allocation;
- function inlining;
- tail-call optimization;
- interprocedural optimization;
- link-time optimization;
- removal or merging of identical code/data.

The C abstract machine does not require a one-to-one mapping between source statements and instructions. Undefined behavior gives the optimizer even broader freedom because the invalid execution is outside the program's required semantics.

### Why variables disappear
A variable can be optimized out when its value is never needed for observable behavior. It can also exist only as a register expression or be represented differently at different instruction ranges. Debug information can describe some of these transitions, but it cannot always reconstruct an intuitive source variable state.

### Optimization versus bugs
A bug that appears only at `-O2` or `-O3` is not evidence that optimization is wrong. Common causes include:

- undefined behavior;
- data races;
- violated aliasing assumptions;
- missing `volatile` for hardware-visible state;
- missing atomic synchronization;
- lifetime errors;
- timing-sensitive hardware interaction;
- uninitialized data.

## Embedded implications
Optimization is essential for code size, performance, power, cache behavior, interrupt latency, and meeting deadlines. Disabling it globally can hide the very failure being investigated.

Prefer targeted techniques:

- use `-Og` when interactive debugging matters and the toolchain supports it;
- preserve symbols in release-like builds when appropriate;
- use function-specific optimization controls sparingly;
- compare assembly and map files between good/bad builds;
- reproduce with the same optimization level as the field image;
- replace halting with tracing when timing is causal.

Do not permanently weaken optimization merely to make the debugger display prettier.

## Example investigation
Suppose:

```c
if (ready && value == expected) {
    handle_event(value);
}
```
The optimized binary may fold `ready`, keep `value` in a register, eliminate the branch under a proven invariant, or inline `handle_event`. The source debugger might appear to skip the `if` even though the generated code is valid under the compiler's assumptions.

When behavior is surprising, disassemble the relevant address and compare the generated assumptions with the C contract. Check whether another thread/ISR/volatile producer can change the state in a way not represented by ordinary C execution assumptions.

## Edge cases and failure modes
- `-O0` hides stack, timing, and register-allocation behavior found in production.
- LTO can move code across translation-unit boundaries.
- Inlining makes function boundaries less obvious.
- Tail calls remove ordinary return frames.
- Debug symbols can be stale even when source files match.
- A debugger watch expression can evaluate an approximation of a source variable.
- `volatile` does not provide inter-thread atomicity or general memory ordering.
- The optimizer may legally remove code whose result is never observable.

## Verification / debugging
Use a build matrix when needed:

```text
same source + same toolchain + different optimization
same optimization + different instrumentation
same image + different observation method
```

Compare disassembly and compiler-generated reports when available. Inspect warnings for strict-aliasing, uninitialized use, control-flow, and undefined-behavior indicators. Reproduce suspicious logic on a host with sanitizers, then return to the production optimization level.

A useful question is: **what compiler assumption would make the observed instruction sequence correct?** Then verify whether the source code actually guarantees that assumption.

## Staff-level takeaway
Optimization bugs are usually contract bugs. Treat an optimized failure as a cross-layer problem involving the C standard, compiler assumptions, ABI, memory model, hardware observation, and timing. The engineer who can explain why the optimizer produced the observed instructions is much closer to root cause than the engineer who simply turns optimization off.

## Related
[[00_Chapter_Index]]
[[01_Source_level_debugging]]
[[04_Call_stacks]]
[[06_Memory_inspection]]
[[../26_C_Lifetime_Aliasing/00_Chapter_Index]]
[[../29_C_Behavior_Categories/00_Chapter_Index]]
[[../37_C_Compiler_Optimization/00_Chapter_Index]]
