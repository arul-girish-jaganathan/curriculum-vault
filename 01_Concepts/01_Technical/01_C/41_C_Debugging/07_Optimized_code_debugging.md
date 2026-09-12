# Optimized-code debugging

> Canonical C topic note — Chapter 41. Debugging optimized C requires accepting that the compiler may legally transform the implementation while preserving the observable behavior required by the language.

## Definition
Optimized-code debugging means diagnosing a program built with optimization enabled. C source constructs may be inlined, reordered, folded, eliminated, merged, vectorized, or represented only transiently in registers. Debug information attempts to describe these transformations but cannot restore a simple source-to-instruction correspondence.

## Mechanism and language rules
The as-if rule permits any transformation that preserves required observable behavior. A debugger's expectation that “execution reaches this line and then changes this variable” is not a C requirement. Undefined behavior also removes the guarantees needed to reason about optimized execution.

### What to reason about
- Is the source variable still materialized?
- Was the function inlined or tail-called?
- Did constant propagation eliminate a branch?
- Was an expression reordered because the C semantics permit it?
- Is the observed behavior actually synchronization-sensitive or undefined?
- Does `volatile`, atomic access, or another observable side effect constrain optimization?

Never add `volatile` merely to make a debugger display a variable. It changes program semantics and can hide a design defect rather than solve it.

## Embedded implications
Optimization is essential for code size, execution time, power, and real-time behavior. Debugging only `-O0` can miss register pressure, instruction scheduling, race windows, stack differences, and timing-sensitive defects present in production.

For MCU firmware, compare a reproducible release-equivalent binary with a diagnostic build that changes as little as possible. Optimization level itself can alter flash footprint enough to change placement, cache behavior, interrupt timing, or stack usage.

### Firmware review angle
Preserve symbols and debug information separately from production code when policy permits. Use trace/logging or targeted compiler options instead of globally disabling optimization. If changing optimization makes a bug disappear, treat that as evidence of timing/layout/UB sensitivity, not proof that the optimizer is broken.

## Edge cases and failure modes
- **“Next line” jumps backward/forward:** line tables map instruction ranges, not a step-by-step abstract execution trace.
- **Variable unavailable:** optimized away or represented in a location range.
- **Breakpoint changes bug:** stopping changes timing.
- **Adding logging fixes defect:** instrumentation changes scheduling and memory layout.
- **Different optimization changes fault address:** UB, race, stack layout, or timing may be involved.

## Example pattern
```c
static uint32_t compute(uint32_t x)
{
    uint32_t y = x * 10U;
    if (y > 100U) {
        return 100U;
    }
    return y;
}
```
The compiler may fold constants, use conditional instructions, inline the function, and keep `y` only in a register. The debugger may show no stable storage location for `y`.

## Verification / debugging
Reproduce with the exact production compiler and flags. Inspect disassembly and generated maps. Use breakpoints sparingly and prefer trace or persistent diagnostics for timing-sensitive failures. Compare behavior across `-O0`, `-Og`, and release optimization only as an experiment to isolate sensitivity.

Staff-level questions:
- What transformation explains the source-level surprise?
- Does the C standard actually require the observed sequence?
- Is there UB or a data race?
- Can a binary-level invariant be measured without perturbing timing?

## Staff-level takeaway
A production debugger must be treated as a **compiler-output debugger**, not merely a source debugger. Understand the language guarantees, inspect generated instructions, and choose evidence that preserves the real timing and concurrency characteristics of the system.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
