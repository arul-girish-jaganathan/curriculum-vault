# Security-Critical C Primitives

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Constant_time_comparisons|Constant-time comparisons]]
- [[02_Secure_memory_clearing|Secure memory clearing]]
- [[03_Integer_overflow_defenses|Integer overflow defenses]]
- [[04_Parsing_untrusted_input|Parsing untrusted input]]
- [[05_Length_prefix_protocols|Length-prefix protocols]]
- [[06_Pointer_truncation_hazards|Pointer truncation hazards]]
- [[07_Secret_lifetime|Secret lifetime]]
- [[08_Stack_protection_concepts|Stack protection concepts]]
- [[09_CFI_concepts|CFI concepts]]
- [[10_Memory_tagging_concepts|Memory tagging concepts]]
- [[11_Secure_build_flags|Secure build flags]]
- [[12_Security_review_workflow|Security review workflow]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
