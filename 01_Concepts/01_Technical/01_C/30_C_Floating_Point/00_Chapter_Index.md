# 30_C_Floating_Point: Chapter Index

## Overview
C Floating Point arithmetic governs how real numbers are represented, computed, and converted under ISO C (`<float.h>`, `<math.h>`, `<fenv.h>`). While modern architectures predominantly implement IEEE 754, standard C permits non-IEEE representations and historical evaluation behaviors (such as `FLT_EVAL_METHOD`). This chapter provides a rigorous examination of floating-point types, rounding modes, precision limits, IEEE 754 compliance assumptions, special values (NaNs, infinities, signed zeros, subnormals), exception handling, conversion hazards, and deterministic numeric design.

## Chapter Directory
- [[01_Floating_types]] — `float`, `double`, `long double`, range limits, and `<float.h>` introspection
- [[02_Rounding]] — Rounding modes (`FLT_ROUNDS`), directional rounding, and runtime control via `<fenv.h>`
- [[03_Precision]] — Significant digits, machine epsilon (`FLT_EPSILON`), and cumulative rounding errors
- [[04_FLT_EVAL_METHOD_heritage]] — Extended precision evaluation registers (`x87` 80-bit registers) and deterministic casting
- [[05_IEEE_754_assumptions]] — Non-portable assumptions regarding binary representations and bit casting
- [[06_NaN_and_infinity]] — Quiet NaNs, signaling NaNs, infinities, and comparisons (`isnan`, `isinf`)
- [[07_Signed_zero]] — Positive and negative zero semantics, arithmetic identity rules, and `atan2` behavior
- [[08_Subnormals]] — Gradual underflow, subnormal (denormalized) numbers, and performance traps in embedded microcontrollers
- [[09_Exceptions_and_fenv]] — Floating-point exception flags (`FE_INVALID`, `FE_DIVBYZERO`, `FE_OVERFLOW`) and environment control
- [[10_Conversion_hazards]] — Integer-to-float narrowing/widening, undefined behavior on out-of-range casts, and loss of precision
- [[11_Embedded_floating_point_cost]] — Soft-float vs. hard-float ABIs, context-switching overhead, and execution timing jitter
- [[12_Deterministic_numeric_design]] — Fixed-point alternatives, numerical stability, and deterministic control system patterns

## Related Chapters
- [[../00_Complete_Topic_Map]]
- [[../27_C_Alignment_Object_Representation]]
- [[../29_C_Behavior_Categories]]
