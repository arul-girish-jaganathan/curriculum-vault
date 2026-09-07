# Variadic Functions and APIs

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_va_list|va_list]]
- [[02_va_start|va_start]]
- [[03_va_arg|va_arg]]
- [[04_va_end|va_end]]
- [[05_Default_argument_promotions|Default argument promotions]]
- [[06_Format_strings|Format strings]]
- [[07_printf_like_APIs|printf-like APIs]]
- [[08_Variadic_macros|Variadic macros]]
- [[09_ABI_details|ABI details]]
- [[10_Type_safety_limitations|Type-safety limitations]]
- [[11_Logging_interfaces|Logging interfaces]]
- [[12_Embedded_diagnostics_APIs|Embedded diagnostics APIs]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
