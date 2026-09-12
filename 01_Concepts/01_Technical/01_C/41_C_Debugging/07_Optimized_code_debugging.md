# Optimized-code debugging

> Canonical C topic note — Chapter 41. Debugging optimized C requires accepting that source-level control flow and object representation may differ substantially from generated machine code while remaining semantically valid.

## Definition
Optimized-code debugging means diagnosing a binary built with compiler optimizations enabled. The optimizer can inline functions, eliminate dead code, fold constants, reorder independent operations, merge control flow, reuse stack slots, keep values in registers, and transform loops.

The goal is not to force optimized code to look like source code; it is to understand the generated program and determine whether its behavior matches the language and system contract.

## Mechanism and language rules
The as-if rule permits transformations that preserve required observable behavior. Debug information attempts to describe the transformed program but cannot always provide a simple one-to-one source mapping.

### What to reason about
- Which optimization level and target flags produced the binary?
- Is an apparent ordering requirement actually guaranteed by C?
- Is `volatile`, atomicity, or an external hardware effect involved?
- Could UB give the optimizer freedom to produce surprising code?
- Did inlining or tail calls remove source-level frames?
- Are debug values represented by location lists or unavailable in some instruction ranges?

Never fix an optimization-sensitive symptom by randomly adding `volatile`, disabling optimization globally, or inserting logging. First identify the semantic contract that was missing or violated.

## Embedded implications
Optimization affects timing, code size, flash placement, power, stack usage, and interrupt latency. `-O0` can make a timing bug disappear or create one through larger code and different memory traffic. `-Os` and `-O2` may produce materially different layouts.

### Firmware review angle
Maintain a production-equivalent debug configuration that retains useful symbols while preserving release optimization. For safety-critical diagnosis, archive exact ELF/map artifacts so field PCs can be symbolized later.

## Edge cases and failure modes
- **“Line skipped”:** generated control flow does not map linearly to source.
- **“Variable changed by itself”:** another thread/ISR/DMA changed it, or the displayed value is reconstructed.
- **“Adding a print fixes it”:** timing/layout changed.
- **Undefined behavior:** optimizer assumptions are no longer constrained by the programmer's intuitive execution model.
- **Link-time effects:** LTO can remove boundaries across translation units.

## Example pattern
```c
static int square(int x)
{
    return x * x;
}

int compute(int x)
{
    return square(x) + 1;
}
```
An optimized compiler may emit no call to `square`; the multiply can be directly integrated into `compute`.

## Verification / debugging
Reproduce with the exact optimization flags. Inspect assembly around the failing PC and use compiler optimization reports when available. Compare `-O0`, `-Og`, and production optimization only to isolate the transformation that matters—not to declare one build “correct.”

Check compiler warnings and sanitizers on suitable host/debug builds, but remember that sanitizer instrumentation changes code generation. For timing defects, use hardware trace, cycle counters, GPIO instrumentation, or statistical measurements.

Staff-level questions: What semantic assumption is the optimizer exploiting? Which instruction sequence actually executes? What evidence distinguishes a compiler transformation from undefined behavior or a race?

## Staff-level takeaway
Optimized-code debugging is **machine-level reasoning under language semantics**. Preserve production optimization, inspect generated code, and fix the underlying contract rather than suppressing the optimizer.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
