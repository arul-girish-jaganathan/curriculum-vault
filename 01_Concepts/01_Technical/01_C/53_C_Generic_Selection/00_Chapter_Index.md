# _Generic and Generic Interfaces

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Generic_syntax|_Generic syntax]]
- [[02_Selection_semantics|Selection semantics]]
- [[03_Controlling_expression_type|Controlling expression type]]
- [[04_Macro_wrappers|Macro wrappers]]
- [[05_Type_overloading|Type overloading]]
- [[06_Qualifier_interactions|Qualifier interactions]]
- [[07_Function_like_generic_APIs|Function-like generic APIs]]
- [[08_Generic_math_helpers|Generic math helpers]]
- [[09_Diagnostics_for_unsupported_types|Diagnostics for unsupported types]]
- [[10_C11_portability|C11 portability]]
- [[11_Generic_API_readability|Generic API readability]]
- [[12_When_not_to_use__Generic|When not to use _Generic]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
