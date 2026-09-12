# 07: Signed Zero

## Definition
Signed zero refers to the IEEE 754 representation of zero in two distinct forms: positive zero ($+0.0$) and negative zero ($-0.0$). Both compare equal under relational operators (`+0.0 == -0.0`), but they preserve directional sign information across specific mathematical operations and library functions.

## Scope and Boundaries
- **Covers:** $+0.0$ and $-0.0$ semantics, `atan2`, division by zero signs, and arithmetic identity preservation.
- **Does not cover:** NaNs and infinities, subnormals, or integer zero.

## Why Does It Exist
Signed zero is essential for maintaining mathematical continuity and correct branch cuts across complex elementary functions:
- **Complex Analysis:** Functions like $\log(z)$ and $\sqrt{z}$ have branch cuts where approaching zero from the upper half-plane versus the lower half-plane yields different imaginary results. Signed zero distinguishes these approaches.
- **Directional Limits:** Preserves the sign of infinitesimally small quantities that underflowed to zero.

## Mechanism and Language Rules
- **Equality Rule:** `+0.0 == -0.0` evaluates to **true**.
- **Bitwise Difference:** Their bit representations differ by the sign bit: `0x00000000` for $+0.0$ and `0x80000000` for $-0.0$ (in binary32).
- **Arithmetic Rules:**
  - $1.0 / (+0.0) = +\infty$
  - $1.0 / (-0.0) = -\infty$
  - $(-0.0) + (-0.0) = -0.0$
  - `atan2(-0.0, -1.0)` yields $-\pi$, whereas `atan2(+0.0, -1.0)` yields $+\pi$.

## Examples
```c
#include <stdio.h>
#include <math.h>

int main(void) 
{
    double pos_zero = 0.0;
    double neg_zero = -0.0;

    if (pos_zero == neg_zero) {
        printf("+0.0 equals -0.0\n");
    }

    printf("1.0 / +0.0 = %f\n", 1.0 / pos_zero);
    printf("1.0 / -0.0 = %f\n", 1.0 / neg_zero);

    printf("signbit(+0.0) = %d\n", signbit(pos_zero));
    printf("signbit(-0.0) = %d\n", signbit(neg_zero));

    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Implementation-Defined:** Whether optimizing compilers collapse `-0.0` into `+0.0` when aggressive floating-point optimizations (`-ffast-math`) are active.

## Edge Cases and Failure Modes
- **Fast-Math Destruction:** Enabling `-ffast-math` often treats `-0.0` and `+0.0` as identical, destroying directional continuity in complex math libraries and control systems relying on quadrant-correct angles (`atan2`).

## Embedded Implications
- **Polar Coordinate Calculations:** Embedded robotics and GNSS navigation algorithms calculating heading angles via `atan2(y, x)` depend on signed zero to correctly resolve quadrants when coordinates approach the origin.

## Firmware Review Angle
- **Verify Fast-Math Settings:** Ensure `-ffast-math` is disabled in navigation and sensor fusion firmware where signed zero continuity is required.

## Compiler, ABI, and Toolchain Implications
- **Sign Bit Preservation:** Standard-conforming compilers preserve the sign bit through arithmetic additions and multiplications.

## Performance, Memory, Timing, and Power
- **Zero Overhead:** Signed zero handling is native to IEEE 754 hardware ALU logic, incurring zero performance penalty.

## Verification / Debugging
- **Sign Inspection:** Use `signbit()` from `<math.h>` to explicitly test whether a zero is positive or negative during debugging.

## Safety, Security, and Reliability
- **Mathematical Integrity:** Prevents branch cut discontinuities and incorrect vector angle calculations in spatial positioning systems.

## Trade-offs and Alternatives
- **Signed Zero vs. Magnitude Thresholds:** For robust sensor processing, explicitly clamping values near zero to absolute magnitude thresholds can avoid unwanted negative zero propagation if directional continuity is unnecessary.

## Staff-Level Takeaway
Signed zero is not a bug; it is a vital IEEE 754 feature for preserving directional limits and complex analysis branch cuts. Beware of compiler optimizations (`-ffast-math`) that strip signed zero semantics.

## Related Concepts
- [[00_Chapter_Index]]
- [[05_IEEE_754_assumptions]]
- [[06_NaN_and_infinity]]
- [[09_Exceptions_and_fenv]]
