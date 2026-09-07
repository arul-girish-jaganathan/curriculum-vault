# Dynamic Memory and Allocators

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_malloc|malloc]]
- [[02_calloc|calloc]]
- [[03_realloc|realloc]]
- [[04_free|free]]
- [[05_Alignment_guarantees|Alignment guarantees]]
- [[06_Zero_size_allocation_cases|Zero-size allocation cases]]
- [[07_Allocation_failure|Allocation failure]]
- [[08_Ownership_contracts|Ownership contracts]]
- [[09_Memory_fragmentation|Memory fragmentation]]
- [[10_Custom_allocators|Custom allocators]]
- [[11_Pools_and_arenas|Pools and arenas]]
- [[12_Embedded_allocation_policy|Embedded allocation policy]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
