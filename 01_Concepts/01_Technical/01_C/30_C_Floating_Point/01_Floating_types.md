# 01: Floating Types

## Definition
C provides three standard floating-point types: `float` (single precision), `double` (double precision), and `long double` (extended or quadruple precision). Their ranges, precision limits, and characteristics are defined by the `<float.h>` header.

## Scope and Boundaries
- **Covers:** `float`, `double`, `long double` specifications, size variations, `<float.h>` macros (`FLT_MIN`, `DBL_MAX`, `FLT_DIG`), and standard layout limits.
- **Does not cover:** IEEE 754 bit-level layouts, rounding modes, or fixed-point arithmetic alternatives.

## Why Does It Exist
Real-world numbers span vastly different scales and fractional granularities that integer types cannot represent directly:
- **Dynamic Range:** Floating types use a sign-exponent-mantissa representation to cover extremely large and microscopically small values within fixed storage sizes.
- **Precision Scaling:** `float` provides fast execution and compact storage for sensor data and graphics; `double` provides standard engineering precision; `long double` provides high-precision accumulation for scientific calculations.

## Mechanism and Language Rules
- **Type Specifiers:** `float`, `double`, `long double`. Literals default to `double` (e.g., `3.14`), while `float` literals require an `f` or `F` suffix (e.g., `3.14f`).
- **Standard Sizes:** ISO C mandates `sizeof(float) <= sizeof(double) <= sizeof(long double)`. Typically, `float` is 32 bits, `double` is 64 bits, and `long double` is either 64 bits (MSVC), 80 bits (x87 extended precision on x86/x86_64 GCC), or 128 bits (PowerPC/ARM quadruple precision).
- **Arithmetic Conversions:** Usual arithmetic conversions promote `float` to `double` in mixed expressions unless explicit casting is used.

## Examples
```c
#include <stdio.h>
#include <float.h>

int main(void) 
{
    printf("--- C Floating-Point Type Limits ---\n");
    printf("sizeof(float) = %zu bytes, FLT_DIG = %d, FLT_EPSILON = %e\n", 
           sizeof(float), FLT_DIG, FLT_EPSILON);
    printf("sizeof(double) = %zu bytes, DBL_DIG = %d, DBL_EPSILON = %e\n", 
           sizeof(double), DBL_DIG, DBL_EPSILON);
    printf("sizeof(long double) = %zu bytes, LDBL_DIG = %d\n", 
           sizeof(long double), LDBL_DIG);

    float f_val = 1.23456789f;
    double d_val = 1.234567890123456789;

    printf("Float value:  %.9f\n", f_val);
    printf("Double value: %.17lf\n", d_val);

    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Implementation-Defined:** The exact representation format, radix, base, and bit widths of `long double` are implementation-defined (e.g., 80-bit x87 vs. 128-bit IEEE binary128).
- **Undefined Behavior:** Dividing a floating-point value by zero where traps are enabled or evaluating expressions containing uninitialized floating-point variables.

## Edge Cases and Failure Modes
- **Precision Loss on Assignment:** Assigning a high-precision `long double` literal directly to a `float` without an `f` suffix incurs an implicit conversion warning or silent truncation.
- **Platform Divergence:** Code relying on `long double` having 80 bits of precision on x86 Linux will lose precision and fail unit tests when compiled on ARM or Windows where `long double` is identical to `double` (64 bits).

## Embedded Implications
- **FPU Availability:** Microcontrollers without hardware floating-point units (e.g., Cortex-M0+, AVR) emulate `float` and `double` in software, turning simple math operations into thousands of slow CPU cycles. `long double` software emulation is prohibitively expensive.

## Firmware Review Angle
- **Audit `long double` Usage:** Flag all uses of `long double` in embedded firmware; verify whether target hardware actually supports 80/128-bit hardware floating point or if it forces heavy runtime library emulation.
- **Check Literals:** Ensure `float` literals carry the `f` suffix to prevent unintended double-precision promotions.

## Compiler, ABI, and Toolchain Implications
- **ABI Passing:** Passing `float` and `double` arguments follows strict ABI register allocation rules (e.g., hardware FPU vector registers `s0-s15` or `d0-d7` on ARM AAPCS).

## Performance, Memory, Timing, and Power
- **Storage Cost:** `float` consumes 4 bytes, `double` consumes 8 bytes, and `long double` consumes 8, 12, or 16 bytes depending on the platform ABI.

## Verification / Debugging
- **Compiler Flags:** Enable `-Wfloat-conversion` and `-Wdouble-promotion` to catch unintended precision promotions and narrowing conversions.

## Safety, Security, and Reliability
- **Numerical Stability:** Assuming `float` has sufficient precision for long-term iterative accumulation algorithms leads to catastrophic numerical drift and control system instability.

## Trade-offs and Alternatives
- **`float` vs. `double` vs. Fixed-Point:** Use `float` for memory-constrained sensor arrays and graphics; use `double` for general engineering calculations; use fixed-point arithmetic (`int32_t` scaled) for deterministic, high-speed embedded control loops without an FPU.

## Staff-Level Takeaway
Never treat floating-point types as abstract mathematical real numbers. They are finite binary approximations with strict precision boundaries and platform-dependent representations. Always audit type sizes and suffixes across toolchain migrations.

## Related Concepts
- [[00_Chapter_Index]]
- [[03_Precision]]
- [[04_FLT_EVAL_METHOD_heritage]]
- [[11_Embedded_floating_point_cost]]
