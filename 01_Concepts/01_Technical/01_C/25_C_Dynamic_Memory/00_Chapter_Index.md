# 25_C_Dynamic_Memory: Chapter Index

## Overview
Dynamic memory management in C provides the mechanisms to allocate, resize, and release memory from the heap at runtime via standard library functions (`malloc`, `calloc`, `realloc`, `free`). This chapter explores standard allocation semantics, strict alignment guarantees, allocation failure handling, zero-size edge cases, memory ownership contracts, fragmentation, custom allocators, arena/pool strategies, and embedded allocation policies.

## Chapter Directory
- [[01_malloc]] — Uninitialized heap allocation, size calculations, and byte-alignment guarantees
- [[02_calloc]] — Zero-initialized allocation, overflow checking, and performance considerations
- [[03_realloc]] — In-place resizing, relocation semantics, and safety preservation on failure
- [[04_free]] — Releasing heap memory, null safety, and double-free hazard prevention
- [[05_Alignment_guarantees]] — Maximum fundamental alignment, `max_align_t`, and strict hardware requirements
- [[06_Zero_size_allocation_cases]] — Allocation of zero bytes, implementation-defined behaviors, and portable handling
- [[07_Allocation_failure]] — Handling `NULL` return values, out-of-memory resilience, and fail-safe designs
- [[08_Ownership_contracts]] — Clear responsibility for allocation, transfer, and teardown across module APIs
- [[09_Memory_fragmentation]] — External/internal fragmentation, heap allocators, and deterministic alternatives
- [[10_Custom_allocators]] — Wrapping standard allocators, debugging hooks, and instrumentation wrappers
- [[11_Pools_and_arenas]] — Fixed-size block allocators, arena allocators, and O(1) bulk deallocation strategies
- [[12_Embedded_allocation_policy]] — Heap prohibition, static memory allocation, and deterministic safety guidelines

## Related Chapters
- [[../00_Complete_Topic_Map]]
- [[../26_C_Lifetime_Aliasing]]
- [[../27_C_Alignment_Object_Representation]]
