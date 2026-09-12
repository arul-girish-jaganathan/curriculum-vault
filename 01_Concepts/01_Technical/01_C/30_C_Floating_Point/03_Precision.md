# 03: Precision

## Definition
Precision in floating-point arithmetic refers to the number of significant digits (base 10) or bits (base 2) that can be reliably stored and manipulated without loss. Machine epsilon (`FLT_EPSILON`, `DBL_EPSILON`) represents the difference between 1.0 and the next representable floating-point value.

## Scope and Boundaries
- **Covers:** Significant bits, machine epsilon, catastrophic cancellation, accumulation error, and precision limits.
- **Does not cover:** Rounding modes, floating types ranges, or arbitrary-precision math libraries.

## Why Does It Exist
Because floating-point numbers occupy fixed storage, they represent a discrete subset of real numbers:
- **Machine Epsilon:** Quantifies the granularity of representational precision. For `float`, `FLT_EPSILON` is approximately $1.19 	imes 10^{-7}$; for `double`, `DBL_EPSILON` is approximately $2.22 	imes 10^{-16}$.
- **Cumulative Error:** Repeated arithmetic operations accumulate rounding errors, leading to significant drift in iterative algorithms.

## Mechanism and Language Rules
- **Equality Comparison Hazard:** Comparing floating-point numbers for exact equality (`a == b`) is a major anti-pattern due to precision limitations. Numbers must be compared using an epsilon threshold (`fabs(a - b) < EPSILON`).
- **Catastrophic Cancellation:** Subtracting two nearly equal floating-point numbers discards almost all significant value bits, leaving a result dominated by rounding noise.

## Examples
```c
#include <stdio.h>
#include <math.h>
#include <float.h>

int main(void) 
{
    double a = 1.0000000000000001;
    double b = 1.0000000000000002;

    /* Unsafe exact comparison */
    if (a == b) {
        printf("a equals b\n");
    } else {
        printf("a does not equal b\n");
    }

    /* Safe epsilon comparison */
    if (fabs(a - b) < DBL_EPSILON) {
        printf("a approximately equals b within DBL_EPSILON\n");
    } else {
        printf("a and b differ significantly\n");
    }

    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Implementation-Defined:** Exact epsilon values and mantissa bit widths depend on the underlying floating-point format.

## Edge Cases and Failure Modes
- **Loop Termination Failure:** Using a floating-point variable as a loop counter can result in an infinite loop because fractional increments cannot be represented exactly in binary floating-point.

## Embedded Implications
- **Control System Drift:** In PID controllers and digital filters implemented in `float`, cumulative precision loss over millions of iterations causes integrator windup or filter divergence.

## Firmware Review Angle
- **Ban Floating-Point Loop Counters:** Flag and reject any loops using floating-point variables as control counters; enforce integer loop indices.
- **Audit Equality Checks:** Flag direct `==` or `!=` comparisons on floating-point variables and require epsilon threshold comparisons.

## Compiler, ABI, and Toolchain Implications
- **FMA Instructions:** Fused Multiply-Add (`fma`, `fmaf`) computes $a 	imes b + c$ with a single rounding step, significantly improving precision and performance in matrix and DSP algorithms.

## Performance, Memory, Timing, and Power
- **Precision vs. Speed:** Using `float` instead of `double` doubles memory bandwidth efficiency and SIMD packing density on vector architectures, at the cost of reduced precision.

## Verification / Debugging
- **Static Analysis:** Modern static analyzers flag direct floating-point equality comparisons and floating-point loop induction variables.

## Safety, Security, and Reliability
- **Safety Compliance:** Numerical instability resulting from poor precision management violates aerospace and automotive control software reliability standards.

## Trade-offs and Alternatives
- **Floating-Point vs. Kahan Summation:** For large numerical summations, standard summation accumulates massive rounding error; Kahan summation algorithm compensates for lost low-order bits, preserving precision.

## Staff-Level Takeaway
Precision is finite and degrades with every arithmetic operation. Never use exact equality comparisons for floating-point numbers, never use floats as loop counters, and be acutely aware of catastrophic cancellation when subtracting close values.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Floating_types]]
- [[04_FLT_EVAL_METHOD_heritage]]
- [[12_Deterministic_numeric_design]]
