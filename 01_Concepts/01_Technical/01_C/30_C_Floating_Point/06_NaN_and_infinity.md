# 06: NaN and Infinity

## Definition
NaN (Not-a-Number) and Infinity ($+\infty$, $-\infty$) are special floating-point values defined by IEEE 754 and supported in ISO C via `<math.h>` macros and classification functions (`isnan`, `isinf`, `isfinite`). They represent invalid arithmetic results and overflow conditions.

## Scope and Boundaries
- **Covers:** Quiet NaNs, signaling NaNs, infinities, classification functions (`isnan`, `isinf`), and arithmetic propagation rules.
- **Does not cover:** Floating-point exceptions, signed zeros, or subnormal numbers.

## Why Does It Exist
Robust numerical software must handle exceptional mathematical states without crashing the application:
- **Graceful Propagation:** Arithmetic operations involving NaNs propagate NaNs, allowing computations to continue and reporting failure at the end of a pipeline rather than aborting midway.
- **Overflow Representation:** Representing division by zero or number overflow as Infinity prevents immediate core dumps and enables bounded limit checks.

## Mechanism and Language Rules
- **Generation:**
  - Division by zero ($1.0 / 0.0$) yields $+\infty$.
  - Square root of a negative number ($\sqrt{-1.0}$) yields `NaN`.
- **Comparison Rule:** Any comparison involving a NaN (except `!=`) evaluates to **false**. Specifically, `nan == nan` is **false**. You must use `isnan(x)` to test for NaN.
- **Classification Macros (`<math.h>`):**
  - `isnan(x)`: Returns non-zero if `x` is a NaN.
  - `isinf(x)`: Returns non-zero if `x` is $+\infty$ or $-\infty$.
  - `isfinite(x)`: Returns non-zero if `x` is neither NaN nor Infinity.

## Examples
```c
#include <stdio.h>
#include <math.h>

int main(void) 
{
    double zero = 0.0;
    double inf_val = 1.0 / zero;
    double nan_val = 0.0 / zero;

    printf("1.0 / 0.0 = %f (isinf: %d)\n", inf_val, isinf(inf_val));
    printf("0.0 / 0.0 = %f (isnan: %d)\n", nan_val, isnan(nan_val));

    if (nan_val == nan_val) {
        printf("NaN equals NaN\n");
    } else {
        printf("NaN does not equal NaN\n");
    }

    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Implementation-Defined:** The exact bit patterns distinguishing quiet NaNs from signaling NaNs and the sign bit of generated NaNs are implementation-defined.

## Edge Cases and Failure Modes
- **Failed Error Checks:** Writing `if (result == NAN)` always evaluates to false because `NAN != NAN`. Developers must use `isnan(result)`.
- **Control Flow Corruption:** Unchecked NaNs entering control loops or conditional branches can cause infinite loops or corrupt downstream physical actuator commands.

## Embedded Implications
- **Safety Critical Systems:** In automotive and aerospace control systems, uncontrolled NaNs or infinities entering actuator feedback loops can lead to physical system damage. Input telemetry must be validated using `isfinite()`.

## Firmware Review Angle
- **Audit NaN Comparisons:** Flag any code checking `x == NAN` or `x != NAN`; require `isnan(x)` or `isfinite(x)`.
- **Validate Telemetry:** Ensure all incoming sensor data streams are checked for `isfinite()` before being processed by control algorithms.

## Compiler, ABI, and Toolchain Implications
- **Fast-Math Hazard:** Enabling `-ffast-math` instructs the compiler to assume NaNs and infinities never occur, disabling NaN checks and breaking `isnan()` function reliability.

## Performance, Memory, Timing, and Power
- **Arithmetic Propagation:** Floating-point pipelines handle NaNs and infinities in hardware without software traps, incurring negligible performance overhead during propagation.

## Verification / Debugging
- **FPU Traps:** Enable invalid operation exception traps (`FE_INVALID`) to catch NaN generation at the exact instruction that produced it.

## Safety, Security, and Reliability
- **Robustness:** Explicitly checking for `isfinite()` prevents mathematical exceptions and numerical collapse in safety-critical loops.

## Trade-offs and Alternatives
- **NaN Propagation vs. Explicit Assertions:** Relying solely on NaN propagation simplifies code structure, but explicit `isfinite()` validation provides fail-safe boundary stops in critical control loops.

## Staff-Level Takeaway
NaNs and infinities are powerful features of IEEE 754 arithmetic, but they are silent killers if ignored. Remember that `NAN != NAN` is always true, always use `isnan()` and `isfinite()`, and never enable `-ffast-math` when NaN safety is required.

## Related Concepts
- [[00_Chapter_Index]]
- [[05_IEEE_754_assumptions]]
- [[07_Signed_zero]]
- [[09_Exceptions_and_fenv]]
