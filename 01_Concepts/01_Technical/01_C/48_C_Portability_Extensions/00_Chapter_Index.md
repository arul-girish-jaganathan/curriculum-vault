# Portability and Compiler Extensions

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Compiler_specific_keywords|Compiler-specific keywords]]
- [[02_Pragmas|Pragmas]]
- [[03_Builtins|Builtins]]
- [[04_Inline_assembly|Inline assembly]]
- [[05_Section_placement|Section placement]]
- [[06_Packing_attributes|Packing attributes]]
- [[07_Weak_attributes|Weak attributes]]
- [[08_Likely_unlikely_hints|Likely/unlikely hints]]
- [[09_Target_intrinsics|Target intrinsics]]
- [[10_Feature_detection|Feature detection]]
- [[11_Extension_isolation|Extension isolation]]
- [[12_Portability_wrappers|Portability wrappers]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
