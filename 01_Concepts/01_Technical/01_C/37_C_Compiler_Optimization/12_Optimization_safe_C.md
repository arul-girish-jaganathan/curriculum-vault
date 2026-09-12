# Optimization-safe C

> Canonical C topic note — chapter 37.

## Definition
Optimization-safe C is code whose correctness follows from the language, documented implementation contracts, and explicit hardware/concurrency contracts rather than from a particular optimizer's current behavior.

## Mechanism and language rules
Core practices are: eliminate undefined behavior; respect object lifetime, bounds, alignment and aliasing; use correct integer types; establish sequencing; distinguish `volatile` from atomics; and document implementation extensions.

```c
bool ready = atomic_load_explicit(&state, memory_order_acquire);
```

A correct synchronization primitive gives the compiler and hardware the information needed for concurrent correctness. Replacing it with “the compiler probably won't reorder this” is not a contract.

## Embedded implications
Use volatile for genuine externally observable objects such as MMIO, atomics/RTOS primitives for shared state, explicit barriers for hardware ordering, and fixed-width types where representation matters. Keep timing-critical requirements measurable rather than encoded as accidental instruction counts.

## Edge cases and failure modes
Common symptoms include release-only crashes, infinite polling loops, stale shared data, incorrect peripheral sequencing, and optimized-away diagnostics. Disabling optimization is generally a diagnostic experiment, not a fix.

## Verification / debugging
Run aggressive warnings, static analysis, sanitizers, and tests on host builds. Build target firmware at production optimization. Inspect assembly for hardware-sensitive functions and measure cycle counts, stack, image size, and interrupt latency.

## Staff-level takeaway
The goal is not to write code that survives one compiler. The goal is to write code whose assumptions are explicit enough that multiple conforming compilers, optimization levels, and target configurations preserve the intended behavior.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
