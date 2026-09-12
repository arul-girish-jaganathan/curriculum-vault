# 04: limits.h

## Definition
`<limits.h>` defines implementation-specific limits for the ranges of the standard integer types, including `CHAR_BIT`, `CHAR_MIN`, `CHAR_MAX`, `INT_MIN`, `INT_MAX`, and the corresponding limits for other standard integer types. It is the portable source of truth for integer range assumptions.

## Scope and Boundaries
* **Covers:** integer widths/ranges, character bit width, signedness-related limits, and compile-time limit macros.
* **Does not cover:** floating-point limits (`<float.h>`), fixed-width integer typedefs (`<stdint.h>`), or dynamic memory limits.

## Why Does It Exist
The C standard deliberately leaves many integer representation details to the implementation. `limits.h` lets portable code discover those properties instead of assuming that `char` is 8 bits, `int` is 32 bits, or `long` has a particular width.

## Mechanism and Language Rules
1. `CHAR_BIT` gives the number of bits in a byte.
2. `CHAR_MIN`/`CHAR_MAX` describe the range of plain `char`; whether plain `char` is signed or unsigned is implementation-defined.
3. The integer limit macros are integer constant expressions and can be used in `_Static_assert`, conditional compilation, and range checks.
4. The limits describe value ranges, not necessarily object size or ABI calling convention.

## Examples
```c
#include <limits.h>

_Static_assert(CHAR_BIT >= 8, "platform byte is too small for this protocol");

static int clamp_to_int(long long value)
{
    if (value > INT_MAX) {
        return INT_MAX;
    }
    if (value < INT_MIN) {
        return INT_MIN;
    }
    return (int)value;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
* Plain `char` signedness is implementation-defined; portable code must use `signed char` or `unsigned char` when signedness matters.
* Assuming `CHAR_BIT == 8` is non-portable unless the application explicitly establishes that platform requirement.
* Integer overflow for a signed type is undefined behavior; comparing against `INT_MAX` before an addition can prevent the overflow.
* Unsigned arithmetic wraps modulo the corresponding range and is not equivalent to signed overflow.

## Edge Cases and Failure Modes
* `sizeof(char)` is always 1, but one byte can contain more than 8 bits.
* `UINT_MAX` is not necessarily `(1U << 32) - 1`; use the macro instead of shifting based on an assumed width.
* Mixing `char` with character classification APIs can be dangerous when `char` is signed and a negative value reaches an API requiring an `unsigned char` value or EOF.
* Integer promotion can cause a small integer object to participate in an expression as `int`, changing the overflow behavior you expected.

## Embedded Implications
`limits.h` matters when firmware uses native integer types for register math, counters, timers, or resource limits. A bootloader, protocol parser, or driver that assumes 32-bit `unsigned long` can fail on a target with a different data model. `CHAR_BIT` is especially important for byte-oriented protocols and serialization logic.

## Firmware Review Angle
Check assumptions such as `8U`, `32U`, `INT_MAX`, and `sizeof(long)` against the actual target ABI. Prefer standard-width types for externally specified widths and `limits.h` for properties of the native C types.

## Compiler, ABI, and Toolchain Implications
These macros are normally compile-time constants derived from the implementation and ABI. They influence constant folding, diagnostics, conditional compilation, and generated code. Cross-compiling the same source for two targets can therefore produce different constant values without any source change.

## Performance, Memory, Timing, and Power
There is normally no runtime cost: the limits are constants. Correctly sizing computations from their actual ranges can prevent unnecessary wider arithmetic on small MCUs, but safety-critical code should prioritize representable ranges over micro-optimizations.

## Verification / Debugging
* Print or compile-time-check the key limits for every supported target.
* Use compiler predefined macros and generated build reports to record the data model.
* Add boundary tests around `INT_MIN`, `INT_MAX`, `UINT_MAX`, and any application-specific derived limits.
* Inspect warning output for signed/unsigned comparisons.

## Safety, Security, and Reliability
Range assumptions are part of the security boundary of parsers and allocators. Validate before arithmetic that can overflow, and use the limit macros rather than literal constants that silently become wrong on another target. Treat data-model differences as an architecture test, not a build nuisance.

## Trade-offs and Alternatives
* **Use `limits.h`:** to describe native C integer properties.
* **Use `stdint.h`:** when the application requires a particular width.
* **Use explicit application limits:** when a protocol or domain has a narrower valid range than the underlying C type.

## Staff-Level Takeaway
A mature C codebase distinguishes implementation facts from application contracts. `limits.h` exposes the former; `stdint.h` expresses the latter when width matters. Staff-level review should identify every literal width assumption and decide whether it should instead be derived from one of these two interfaces.

## Related Concepts
* [[00_Chapter_Index]]
* [[02_stdint_h]]
* [[05_float_h]]
* [[../10_C_Conversions_Promotions/00_Chapter_Index]]
* [[../29_C_Behavior_Categories/00_Chapter_Index]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*