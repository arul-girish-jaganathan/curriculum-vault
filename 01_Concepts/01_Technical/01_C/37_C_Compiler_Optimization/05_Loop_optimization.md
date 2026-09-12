# Loop optimization

## Definition
**Loop optimization** transforms repetitive control flow to reduce execution time, code size, memory traffic, or energy while preserving C semantics. Common transformations include induction-variable simplification, invariant-code motion, unrolling, peeling, fusion, distribution, unswitching, vectorization, strength reduction, and branch simplification.

## Scope and boundaries
The compiler may apply a transformation only when it can prove the required semantics. Pointer aliasing, signed overflow, volatile accesses, function calls, possible traps, and observable side effects can prevent transformations. Correct loop structure and defined behavior therefore matter more than manually forcing a particular assembly pattern.

## Mechanism and language rules
Example:

```c
for (size_t i = 0; i < n; ++i)
    sum += a[i] * scale;
```

The compiler may hoist an invariant `scale`, simplify induction variables, unroll iterations, vectorize loads, or use target-specific instructions. The source loop count does not imply a particular instruction count.

### Loop-carried dependencies
A dependency such as `a[i] = a[i - 1] + 1` limits parallelization because iteration `i` depends on the previous iteration. Conversely, independent iterations are strong candidates for vectorization or unrolling.

### Aliasing matters
If `a`, `b`, and `out` may overlap, the compiler must preserve that possibility unless the program contract or `restrict` establishes otherwise. Incorrect alias assumptions can produce wrong optimized results, not merely slower code.

## Embedded implications
Loops dominate many DSP, filtering, packet parsing, checksum, sensor, and control workloads. On MCUs without SIMD, unrolling may trade flash for fewer branch instructions. On cached CPUs, vectorization and memory locality can dominate. On tiny deterministic MCUs, code-size growth and interrupt latency may matter more than average throughput.

MMIO polling loops require special care: the object representing changing hardware state normally needs `volatile`, and waiting for a peripheral should have a timeout or fault policy rather than an accidental infinite loop.

## Edge cases and failure modes
- Signed integer overflow inside induction variables is undefined behavior and can enable surprising transformations.
- Using floating-point reassociation when strict numerical behavior matters.
- Assuming loop unrolling always improves performance.
- Ignoring aliasing between input and output buffers.
- Optimizing a loop that is actually synchronization or hardware polling.
- Creating huge code through manual unrolling when the compiler would make a better target-specific choice.

## Verification / debugging
Measure cycle counts on the target using a hardware timer or trace facility. Inspect generated assembly and compiler optimization/vectorization reports. Compare code size and worst-case latency, not just average benchmark throughput. Test boundary cases such as `n == 0`, one element, maximum supported length, overlapping buffers where allowed, and interrupt preemption.

## Performance, memory, timing and power
Loop transformations can reduce branches and loop-control overhead, improve instruction-level parallelism, and exploit cache or SIMD. They can also increase flash, register pressure, stack spills, or instruction-cache misses. For embedded systems, evaluate energy per operation and worst-case execution time in addition to average throughput.

## Staff-level takeaway
Optimize the **algorithm, data layout, aliasing contract, and measurement method** before hand-writing instruction-shaped C. A loop that is simple, well-defined, and explicit about ownership and concurrency gives the optimizer the greatest freedom.