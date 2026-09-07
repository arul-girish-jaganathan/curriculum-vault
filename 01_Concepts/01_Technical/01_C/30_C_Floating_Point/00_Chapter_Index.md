# Floating-point in C

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Floating_types|Floating types]]
- [[02_Rounding|Rounding]]
- [[03_Precision|Precision]]
- [[04_FLT_EVAL_METHOD_heritage|FLT_EVAL_METHOD heritage]]
- [[05_IEEE_754_assumptions|IEEE 754 assumptions]]
- [[06_NaN_and_infinity|NaN and infinity]]
- [[07_Signed_zero|Signed zero]]
- [[08_Subnormals|Subnormals]]
- [[09_Exceptions_and_fenv|Exceptions and fenv]]
- [[10_Conversion_hazards|Conversion hazards]]
- [[11_Embedded_floating_point_cost|Embedded floating-point cost]]
- [[12_Deterministic_numeric_design|Deterministic numeric design]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
