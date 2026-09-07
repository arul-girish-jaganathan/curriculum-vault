# Designated Initialization in Practice

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Array_designators|Array designators]]
- [[02_Struct_designators|Struct designators]]
- [[03_Nested_designators|Nested designators]]
- [[04_Override_rules|Override rules]]
- [[05_Sparse_lookup_tables|Sparse lookup tables]]
- [[06_Versioned_configs|Versioned configs]]
- [[07_Default_zero_assumptions|Default-zero assumptions]]
- [[08_Readability|Readability]]
- [[09_Generated_initialization|Generated initialization]]
- [[10_ABI_stability|ABI stability]]
- [[11_Compile_time_validation|Compile-time validation]]
- [[12_Embedded_tables|Embedded tables]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
