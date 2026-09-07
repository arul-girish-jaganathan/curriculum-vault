# Macro Design and Safety

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Object_like_macros|Object-like macros]]
- [[02_Function_like_macros|Function-like macros]]
- [[03_Parentheses_discipline|Parentheses discipline]]
- [[04_Multiple_evaluation|Multiple evaluation]]
- [[05_Statement_macros|Statement macros]]
- [[06_do_while_0_idiom|do-while(0) idiom]]
- [[07_Variadic_macros|Variadic macros]]
- [[08_Stringification_macros|Stringification macros]]
- [[09_Token_pasting_macros|Token-pasting macros]]
- [[10_Macro_namespaces|Macro namespaces]]
- [[11_When_inline_functions_are_safer|When inline functions are safer]]
- [[12_Macro_review_checklist|Macro review checklist]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
