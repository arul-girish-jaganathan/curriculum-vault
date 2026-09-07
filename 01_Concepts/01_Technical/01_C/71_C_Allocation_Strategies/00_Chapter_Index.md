# Allocation Strategies for Embedded C

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_First_fit|First fit]]
- [[02_Best_fit|Best fit]]
- [[03_Segregated_free_lists|Segregated free lists]]
- [[04_Buddy_concepts|Buddy concepts]]
- [[05_Slab_pool_allocators|Slab/pool allocators]]
- [[06_Arenas|Arenas]]
- [[07_Region_allocation|Region allocation]]
- [[08_Object_caches|Object caches]]
- [[09_Fragmentation_measurement|Fragmentation measurement]]
- [[10_Worst_case_allocation_time|Worst-case allocation time]]
- [[11_Failure_containment|Failure containment]]
- [[12_Allocator_selection|Allocator selection]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
