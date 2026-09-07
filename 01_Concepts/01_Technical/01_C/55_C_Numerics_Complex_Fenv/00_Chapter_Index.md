# Numerics, Complex Types and Floating Environment

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Complex_types|Complex types]]
- [[02_complex_arithmetic|complex arithmetic]]
- [[03_imaginary_heritage|imaginary heritage]]
- [[04_conj_cabs_carg|conj/cabs/carg]]
- [[05_tgmath_h_concepts|<tgmath.h> concepts]]
- [[06_fenv_environment|fenv environment]]
- [[07_Rounding_modes|Rounding modes]]
- [[08_Floating_exceptions|Floating exceptions]]
- [[09_errno_vs_fenv|errno vs fenv]]
- [[10_Numerical_stability|Numerical stability]]
- [[11_Embedded_DSP_implications|Embedded DSP implications]]
- [[12_Deterministic_numeric_testing|Deterministic numeric testing]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
