# Incomplete Types and Opaque Data Structures

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Incomplete_structs|Incomplete structs]]
- [[02_Opaque_handles|Opaque handles]]
- [[03_Forward_declarations|Forward declarations]]
- [[04_Mutually_recursive_types|Mutually recursive types]]
- [[05_API_encapsulation|API encapsulation]]
- [[06_Private_implementation|Private implementation]]
- [[07_Flexible_array_relation|Flexible array relation]]
- [[08_Allocation_patterns|Allocation patterns]]
- [[09_ABI_stability|ABI stability]]
- [[10_Dependency_reduction|Dependency reduction]]
- [[11_Debug_visibility|Debug visibility]]
- [[12_Module_ownership|Module ownership]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
