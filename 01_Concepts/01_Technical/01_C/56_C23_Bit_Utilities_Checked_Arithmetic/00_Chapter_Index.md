# C23 Bit Utilities and Checked Arithmetic

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_stdbit_h_overview|stdbit.h overview]]
- [[02_Bit_counting|Bit counting]]
- [[03_Bit_rotations|Bit rotations]]
- [[04_Bit_width_helpers|Bit width helpers]]
- [[05_Power_of_two_helpers|Power-of-two helpers]]
- [[06_stdckdint_h|<stdckdint.h>]]
- [[07_Checked_addition|Checked addition]]
- [[08_Checked_subtraction|Checked subtraction]]
- [[09_Checked_multiplication|Checked multiplication]]
- [[10_Overflow_safe_APIs|Overflow-safe APIs]]
- [[11_Compiler_builtins_vs_standard_APIs|Compiler builtins vs standard APIs]]
- [[12_Migration_strategy|Migration strategy]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
