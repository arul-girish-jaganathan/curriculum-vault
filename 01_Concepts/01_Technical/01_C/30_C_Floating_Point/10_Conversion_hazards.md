# 10: Conversion Hazards

## Definition
Conversion hazards refer to the precision loss, narrowing overflow, and undefined behavior that occur when converting between floating-point types, or between floating-point types and integers, when values exceed target representation boundaries.

## Scope and Boundaries
- **Covers:** Float-to-int narrowing casts, out-of-range undefined behavior, implicit promotion/demotion hazards, and precision loss.
- **Does not cover:** Standard floating types ranges or rounding modes.

## Why Does It Exist
Converting numbers across disparate type systems involves fundamental representation shifts:
- **Range Disparity:** A 64-bit `double` can represent numbers up to $1.7 	imes 10^{308}$, whereas a 32-bit `int` maxes out at $2.1 	imes 10^9$. Casting a large float to an int overflows the integer range.
- **Undefined Behavior:** Under ISO C, converting a floating-point value to an integer type when the floating value cannot fit within the integer range results in **undefined behavior**.

## Mechanism and Language Rules
- **Out-of-Range Cast UB:** `float f = 1e10f; int x = (int)f;` invokes undefined behavior in ISO C because `1e10` exceeds `INT_MAX`.
- **Precision Loss on Narrowing:** Converting `double` to `float` discards lower bits, introducing rounding errors.

## Examples
```c
#include <stdio.h>
#include <limits.h>

int main(void) 
{
    double large_val = 5.0e15;

    if (large_val > INT_MAX || large_val < INT_MIN) {
        printf("Value out of range for integer conversion!\n");
    } else {
        int x = (int)large_val;
        printf("Converted int: %d\n", x);
    }

    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Casting a floating-point number to an integer type when the value is outside the representable range of the integer type.
- **Implementation-Defined:** The exact result of converting a floating-point fractional value to an integer.

## Edge Cases and Failure Modes
- **NaN / Infinity Integer Casts:** Casting `NaN` or `Infinity` to an integer type results in undefined behavior under ISO C.

## Embedded Implications
- **Sensor Scaled Conversions:** Embedded control systems converting raw floating-point sensor telemetry into fixed-scale integer registers must perform strict range clamping before casting.

## Firmware Review Angle
- **Audit Float-to-Int Casts:** Flag all casts from floating-point types to integers; enforce explicit bounds clamping (`fmin`/`fmax`) prior to casting.

## Compiler, ABI, and Toolchain Implications
- **Hardware Conversion Instructions:** Modern CPUs provide hardware instructions for float-to-int conversion, but invalid ranges trigger hardware invalid operation exceptions.

## Performance, Memory, Timing, and Power
- **Conversion Latency:** Floating-point to integer conversions incur pipeline latency and mode switches on execution units.

## Verification / Debugging
- **UndefinedBehaviorSanitizer:** UBSan detects float-to-int saturation overflows and undefined casting behavior at runtime.

## Safety, Security, and Reliability
- **Robustness:** Clamping floating-point values before integer conversion eliminates a major source of undefined behavior and numerical vulnerability.

## Trade-offs and Alternatives
- **Safe Clamping vs. Direct Cast:** Always write explicit range validation helpers rather than relying on direct casts.

## Staff-Level Takeaway
Casting an out-of-range float to an integer is undefined behavior in ISO C. Always validate and clamp floating-point values against `INT_MIN` and `INT_MAX` before casting them to integer types.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Floating_types]]
- [[06_NaN_and_infinity]]
- [[09_Exceptions_and_fenv]]
