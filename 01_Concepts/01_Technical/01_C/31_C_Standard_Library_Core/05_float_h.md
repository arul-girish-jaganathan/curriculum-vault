# 05: float.h

## Definition
`<float.h>` describes the implementation's floating-point model: radix, precision, exponent range, rounding characteristics, and evaluation-related properties. Macros such as `FLT_EPSILON`, `FLT_MAX`, `DBL_MANT_DIG`, `DBL_MAX_EXP`, and `FLT_ROUNDS` expose properties needed to reason about numerical reliability without assuming IEEE-754 details blindly.

## Scope and Boundaries
* **Covers:** floating-point representation limits, precision, range, rounding metadata, and implementation characteristics.
* **Does not cover:** complex arithmetic, `<fenv.h>` floating environment control, or the full IEEE-754 standard.

## Why Does It Exist
C permits implementations with different floating-point formats, radices, precisions, exponent ranges, and evaluation methods. Numerical code needs a portable way to discover those properties and set tolerances or storage decisions appropriately.

## Mechanism and Language Rules
1. `FLT_EPSILON`, `DBL_EPSILON`, and `LDBL_EPSILON` describe the gap from 1 to the next representable value in the corresponding type.
2. `*_MANT_DIG` gives the precision in radix digits; it is not necessarily “decimal digits.”
3. `*_MIN` is the smallest positive normalized value, while `*_TRUE_MIN` may be available on implementations that support subnormals.
4. `*_MAX` gives the largest finite value.
5. `DECIMAL_DIG` and `*_DECIMAL_DIG` describe decimal round-trip precision requirements.

## Examples
```c
#include <float.h>

static int nearly_equal(double a, double b)
{
    double scale = (a > 0.0) ? a : -a;
    double diff = a - b;
    if (diff < 0.0) {
        diff = -diff;
    }

    return diff <= DBL_EPSILON * ((scale > 1.0) ? scale : 1.0);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
* Comparing floating-point values with `==` is well-defined but often unsuitable for approximate numerical equality.
* Floating-point overflow, underflow, NaNs, signed zeros, and infinities depend on the implementation's supported model and compiler options; do not equate ISO C with a full IEEE-754 guarantee.
* Excess precision and evaluation behavior can make intermediate results differ from the nominal storage type.
* Assuming `FLT_EPSILON` is a universal absolute error tolerance is incorrect; it describes local spacing near 1.

## Edge Cases and Failure Modes
* Catastrophic cancellation can destroy significant digits even when the format itself is correct.
* `0.1` is usually not represented exactly in binary floating-point.
* NaN comparisons have special behavior: a NaN is not equal to itself.
* Using `FLT_MIN` as a tiny epsilon is a common mistake; `FLT_MIN` concerns range, not precision near zero.

## Embedded Implications
Floating-point support can impose substantial code-size, latency, and energy costs on MCUs without hardware FPUs. `float` may be faster and smaller than `double` on some embedded ABIs, while on others both may use the same hardware format. Sensor filtering, control loops, and calibration code must be reviewed for numerical stability and deterministic timing.

## Firmware Review Angle
Check compiler options such as `-ffast-math`, FPU ABI settings, hard/soft floating-point calling conventions, and whether debug/release builds change evaluation or contraction behavior. Validate numerical assumptions on the exact production MCU.

## Compiler, ABI, and Toolchain Implications
The floating-point ABI determines parameter passing and return conventions, register use, and interoperability between compilation units. Optimization can fuse multiply-add operations or reassociate expressions under permitted modes, changing last-bit results. Link-time optimization can expose additional constant-folding opportunities.

## Performance, Memory, Timing, and Power
Floating-point cost is highly target-dependent. Hardware FPU instructions can make arithmetic cheap while conversions, division, transcendental functions, and context save/restore remain expensive. On small MCUs, a fixed-point formulation may provide better deterministic timing and lower energy if the numerical range can be bounded safely.

## Verification / Debugging
* Record all relevant `<float.h>` macros for each supported target.
* Use ulp-aware or domain-specific error metrics rather than only decimal comparisons.
* Run numerical tests at normal, boundary, NaN, infinity, and subnormal inputs where applicable.
* Inspect disassembly to confirm whether the compiler uses hardware floating-point or library calls.

## Safety, Security, and Reliability
Numerical instability can create false safety decisions even without undefined behavior. Define tolerances from the algorithm's error budget, not arbitrary epsilon constants. For safety-critical control loops, bound accumulated error, saturation behavior, and exceptional inputs explicitly.

## Trade-offs and Alternatives
* **Floating point:** convenient dynamic range and expressive algorithms.
* **Fixed point:** deterministic and efficient on hardware without an FPU, but requires explicit scaling/range management.
* **Integer/scaled integer:** appropriate for bounded physical quantities and exact protocol values.

## Staff-Level Takeaway
A Staff engineer should treat floating-point behavior as part of the system contract. `float.h` provides the facts needed to reason about the target, but correctness comes from algorithmic error budgets, compiler/ABI configuration, and measured performance—not from assuming “float means IEEE single precision everywhere.”

## Related Concepts
* [[00_Chapter_Index]]
* [[../30_C_Floating_Point/00_Chapter_Index]]
* [[../55_C_Numerics_Complex_Fenv/00_Chapter_Index]]
* [[../50_C_Performance/00_Chapter_Index]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*