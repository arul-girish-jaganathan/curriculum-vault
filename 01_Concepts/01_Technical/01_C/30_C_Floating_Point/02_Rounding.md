# 02: Rounding

## Definition
Rounding refers to the process of approximating a real mathematical value into a finite representation fitting within a floating-point data type. ISO C allows runtime control over rounding modes via `<fenv.h>` and inspects default behavior via the macro `FLT_ROUNDS`.

## Scope and Boundaries
- **Covers:** Rounding modes (`FE_TONEAREST`, `FE_DOWNWARD`, `FE_UPWARD`, `FE_TOWARDZERO`), `FLT_ROUNDS`, and runtime rounding control (`fesetround`).
- **Does not cover:** Floating-point exceptions, precision limits, or fixed-point quantization.

## Why Does It Exist
Floating-point representations have finite mantissa widths, meaning most real numbers cannot be represented exactly and must be rounded:
- **IEEE 754 Modes:** Different numerical applications require specific rounding behaviors (e.g., financial software requiring round-toward-zero or round-to-nearest-even to eliminate statistical bias).
- **Interval Arithmetic:** Requires upward and downward rounding to rigorously bound truncation and round-off errors.

## Mechanism and Language Rules
- **Standard Rounding Modes (`<fenv.h>`):**
  - `FE_TONEAREST`: Round to nearest, ties to even (default IEEE 754 mode).
  - `FE_DOWNWARD`: Round toward $-\infty$ (floor).
  - `FE_UPWARD`: Round toward $+\infty$ (ceil).
  - `FE_TOWARDZERO`: Round toward zero (truncation).
- **Macro Introspection:** `FLT_ROUNDS` indicates the default rounding mode (-1 for indeterminable, 1 for round to nearest, 2 for toward zero, 3 for upward, 4 for downward).
- **Runtime Control:** `fesetround(FE_UPWARD);` alters the active rounding mode for subsequent floating-point operations.

## Examples
```c
#include <stdio.h>
#include <fenv.h>

int main(void) 
{
    double val = 3.7;

    /* Set rounding toward zero (truncation) */
    fesetround(FE_TOWARDZERO);
    printf("Round toward zero (3.7): %f\n", val);

    fesetround(FE_DOWNWARD);
    printf("Floor of 3.7 under FE_DOWNWARD: %.1f\n", val);

    fesetround(FE_UPWARD);
    printf("Ceil of 3.7 under FE_UPWARD:   %.1f\n", val);

    fesetround(FE_TONEAREST);
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Implementation-Defined:** Whether compile-time constant floating-point expressions respect runtime changes to rounding modes via `fesetround`. Most compilers evaluate constant expressions at compile time using default rounding, ignoring runtime `fesetround` calls.

## Edge Cases and Failure Modes
- **Compiler Optimization Hazards:** Aggressive compiler optimizations (`-ffast-math`) assume default rounding (`FE_TONEAREST`) and ignore dynamic `fesetround` calls, causing silent failures in numerical libraries relying on alternate rounding modes.

## Embedded Implications
- **FPU Control Register:** Changing rounding modes requires modifying hardware FPU control registers (e.g., `FPSCR` on ARM, `FCW` on x86), which incurs pipeline flush overhead on embedded processors.

## Firmware Review Angle
- **Audit `-ffast-math`:** Never enable `-ffast-math` in safety-critical systems or numeric libraries that alter or depend on dynamic floating-point rounding modes.

## Compiler, ABI, and Toolchain Implications
- **FENV_ACCESS Pragma:** ISO C defines `#pragma STDC FENV_ACCESS ON` to inform the compiler that the code accesses or modifies the floating-point environment, disabling optimizations that reorder or eliminate rounding changes.

## Performance, Memory, Timing, and Power
- **Execution Overhead:** Modifying rounding modes dynamically breaks instruction pipelining and forces FPU register synchronizations, degrading performance in inner loops.

## Verification / Debugging
- **Unit Testing:** Write test suites verifying that interval arithmetic and financial calculations maintain strict upper/lower bounds under directional rounding modes.

## Safety, Security, and Reliability
- **Deterministic Numerical Output:** Ensuring correct rounding mode configuration prevents financial accumulation drift and geometric intersection errors in CAD/simulation systems.

## Trade-offs and Alternatives
- **Dynamic Rounding vs. Explicit Functions:** Use explicit library functions (`floor`, `ceil`, `trunc`, `round`) for predictable rounding rather than altering global FPU rounding modes dynamically, avoiding concurrency race conditions in multithreaded environments.

## Staff-Level Takeaway
Floating-point rounding is not just an arithmetic detail; it is a global operational state of the FPU. When altering rounding modes dynamically via `<fenv.h>`, always couple your code with `#pragma STDC FENV_ACCESS ON` and guard against aggressive compiler optimizations like `-ffast-math`.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Floating_types]]
- [[03_Precision]]
- [[09_Exceptions_and_fenv]]
