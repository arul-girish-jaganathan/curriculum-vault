# Flexible Array Members and Variable Objects

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_FAM_syntax|FAM syntax]]
- [[02_sizeof_struct_with_FAM|sizeof struct with FAM]]
- [[03_Allocation_formulas|Allocation formulas]]
- [[04_Alignment_after_FAM|Alignment after FAM]]
- [[05_Deep_copy_semantics|Deep-copy semantics]]
- [[06_Reallocation|Reallocation]]
- [[07_Serialization|Serialization]]
- [[08_Ownership|Ownership]]
- [[09_Bounds_metadata|Bounds metadata]]
- [[10_Container_patterns|Container patterns]]
- [[11_Security_pitfalls|Security pitfalls]]
- [[12_Testing_FAM_code|Testing FAM code]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
