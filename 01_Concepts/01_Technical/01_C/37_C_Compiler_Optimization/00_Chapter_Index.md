# Compiler Optimization and Code Generation

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_As_if_rule|As-if rule]]
- [[02_Inlining|Inlining]]
- [[03_Constant_propagation|Constant propagation]]
- [[04_Dead_code_elimination|Dead-code elimination]]
- [[05_Loop_optimization|Loop optimization]]
- [[06_Strict_aliasing_optimization|Strict-aliasing optimization]]
- [[07_LTO|LTO]]
- [[08_Profile_guided_optimization|Profile-guided optimization]]
- [[09_Volatile_barriers|Volatile barriers]]
- [[10_Debug_vs_optimized_builds|Debug vs optimized builds]]
- [[11_Reading_compiler_output|Reading compiler output]]
- [[12_Optimization_safe_C|Optimization-safe C]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
