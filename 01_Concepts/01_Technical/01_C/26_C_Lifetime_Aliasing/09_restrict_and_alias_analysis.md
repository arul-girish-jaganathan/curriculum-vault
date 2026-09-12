# 09: Restrict and Alias Analysis

## Definition
The `restrict` keyword (introduced in C99) is a type qualifier applied to pointer declarations. It promises the compiler that, during the lifetime of the pointer, no other pointer will be used to access the pointed-to object. This enables advanced compiler optimizations, loop vectorization, and alias analysis.

## Scope and Boundaries
- **Covers:** `restrict` qualifier, pointer independence, alias analysis, and loop vectorization.
- **Does not cover:** Strict aliasing rules ([[06_Strict_aliasing]]) or pointer provenance ([[10_Pointer_provenance_concerns]]).

## Why Does It Exist
Aliasing forces compilers to generate conservative code. In functions like `void add(int *a, int *b, int *c)`, the compiler cannot prove `a`, `b`, and `c` do not overlap. Consequently, it must reload values from memory on every iteration. `restrict` lifts this restriction, unlocking peak hardware performance.

## Mechanism and Language Rules
- **Syntax:** `void vector_add(int *restrict dest, const int *restrict src1, const int *restrict src2);`
- **Contract:** The programmer guarantees that the memory regions accessed via restricted pointers do not overlap.
- **Undefined Behavior:** Violating the contract by passing overlapping memory regions to restricted pointers results in undefined behavior.

## Examples
```c
#include <stdio.h>

void saxpy(int n, float a, const float *restrict x, float *restrict y) 
{
    for (int i = 0; i < n; ++i) {
        y[i] += a * x[i];
    }
    /* Compiler can vectorize this loop aggressively because x and y */
    /* are guaranteed not to alias each other. */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Passing overlapping buffers to functions expecting `restrict` pointers (e.g., passing the same array for both `x` and `y` in `saxpy`).

## Edge Cases and Failure Modes
- **Silent Aliasing Violations:** If caller code violates the non-overlap contract, vectorization optimizations will produce corrupted mathematical output without compiler errors.

## Embedded Implications
- **DSP / Math Accelerators:** High-performance digital signal processing (DSP) math kernels (FIR filters, matrix multiplication) rely on `restrict` to achieve maximum SIMD throughput on ARM Neon or DSP cores.

## Firmware Review Angle
- **Verify Non-Overlap:** Always audit callers of functions taking `restrict` pointers to guarantee input and output buffers are distinct and non-overlapping.
- **Compare with `memcpy` vs `memmove`:** `memcpy` requires `restrict` pointers for source and destination; `memmove` supports overlapping buffers.

## Compiler, ABI, and Toolchain Implications
- **Vectorization Reports:** Use compiler flags (`-ftree-vectorize -fopt-info-vec`) to verify whether `restrict` successfully unlocked loop vectorization.

## Performance, Memory, Timing, and Power
- **Dramatic Speedups:** Eliminating alias checks and enabling SIMD/AVX vectorization can yield 2x to 4x performance speedups in numerical code.

## Verification / Debugging
- **UndefinedBehaviorSanitizer:** Does not automatically catch `restrict` violations; requires careful unit testing and buffer overlap assertions.

## Safety, Security, and Reliability
- **Contract Enforcement:** Treat `restrict` as an absolute mathematical contract. Add `assert(dest + n <= src || src + n <= dest);` checks in debug builds.

## Trade-offs and Alternatives
- **`restrict` vs. Standard Pointers:** `restrict` requires strict discipline; if buffer overlap is ever possible, standard pointers or `memmove`-style handling must be used.

## Staff-Level Takeaway
`restrict` is your primary tool for unlocking hardware vectorization in C. Use it liberally on math and data processing pipelines, but treat it as a sacred contract: restricted pointers must never alias.

## Related Concepts
- [[00_Chapter_Index]]
- [[06_Strict_aliasing]]
- [[../25_C_Dynamic_Memory/01_malloc]]
