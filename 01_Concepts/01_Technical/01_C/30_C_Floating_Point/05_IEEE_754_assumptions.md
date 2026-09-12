# 05: IEEE 754 Assumptions

## Definition
IEEE 754 assumptions refer to the common developer practices of assuming that all C compiler toolchains target IEEE 754 floating-point representations (binary32 / binary64) and permitting bit-level type punning between integers and floats. ISO C does **not** strictly mandate IEEE 754 compliance for `float` and `double`, making such assumptions technically non-portable.

## Scope and Boundaries
- **Covers:** IEEE 754 binary32/binary64 standards, bit-level casting assumptions, union type punning, and strict aliasing rules.
- **Does not cover:** Floating types specifications, precision limits, or math library functions.

## Why Does It Exist
Virtually all modern consumer and enterprise hardware (x86, ARM, RISC-V) implements IEEE 754 floating-point arithmetic natively:
- **Performance Shortcuts:** Developers frequently exploit IEEE 754 bit layouts to perform fast inverse square roots, bitwise absolute values, or rapid exponent extractions.
- **Portability Illusion:** Because IEEE 754 is ubiquitous, programmers assume C guarantees it, leading to subtle breakages on specialized DSPs or mainframes with non-IEEE floating-point formats.

## Mechanism and Language Rules
- **Standard Stance:** ISO C permits non-IEEE 754 floating-point formats.
- **Strict Aliasing Violation:** Casting an `int *` to a `float *` or using union type-punning to inspect float bits violates strict aliasing or union rules in strict ISO C, though compiler extensions or `memcpy` provide standard-compliant workarounds.

## Examples
```c
#include <stdio.h>
#include <string.h>
#include <stdint.h>

uint32_t float_to_bits(float f) 
{
    uint32_t u;
    memcpy(&u, &f, sizeof(f));
    return u;
}

int main(void) 
{
    float val = -5.0f;
    uint32_t bits = float_to_bits(val);

    printf("Float: %f, Hex Bits: 0x%08X\n", val, bits);
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Using direct pointer casting (`*(uint32_t *)&my_float`) to inspect floating-point bit representations violates strict aliasing rules and triggers undefined behavior.
- **Implementation-Defined:** Whether the target architecture adheres to IEEE 754 sign-exponent-mantissa bit layouts.

## Edge Cases and Failure Modes
- **Mainframe Portability Failures:** Compiling code that relies on IEEE 754 bit-shifting hacks for fast math on IBM Z mainframes or older DSPs results in complete calculation corruption.

## Embedded Implications
- **Specialized DSPs:** Certain digital signal processors use non-standard floating-point formats or custom fractional widths where IEEE 754 bit masks fail entirely.

## Firmware Review Angle
- **Ban Pointer Type Punning:** Flag all direct pointer casts between integers and floats; enforce `memcpy` for bit-level reinterpretation to comply with strict aliasing rules.

## Compiler, ABI, and Toolchain Implications
- **Optimizer Assumptions:** Compilers optimize floating-point code assuming standard IEEE 754 behavior unless strict conformance flags are enabled.

## Performance, Memory, Timing, and Power
- **Zero-Cost `memcpy`:** Compilers optimize `memcpy(&u, &f, 4)` into a single register move instruction, achieving bit-level reinterpretation with zero performance penalty and 100% standards compliance.

## Verification / Debugging
- **Sanitizers:** UndefinedBehaviorSanitizer catches strict aliasing violations resulting from illegal float-to-integer pointer casts.

## Safety, Security, and Reliability
- **Portability Assurance:** Restricting low-level bit hacks to explicit `memcpy` wrappers ensures code compiles and executes correctly across diverse CPU architectures.

## Trade-offs and Alternatives
- **Bit Hacks vs. Standard Math:** Use standard math library functions (`fabsf`, `frexp`, `ldexp`) instead of raw bit manipulation whenever possible to maintain platform independence.

## Staff-Level Takeaway
While 99% of modern hardware implements IEEE 754, ISO C does not require it. Never use direct pointer casting to inspect float bits; always use `memcpy` to satisfy strict aliasing rules and ensure maximum cross-platform robustness.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Floating_types]]
- [[06_NaN_and_infinity]]
- [[../26_C_Lifetime_Aliasing/06_Strict_aliasing]]
