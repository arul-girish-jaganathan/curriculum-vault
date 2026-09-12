# 26_C_Lifetime_Aliasing: Chapter Index

## Overview
Chapter 26 explores the foundational rules governing memory lifetimes, storage durations, and type-based aliasing in ISO C. In low-level C programming, understanding object lifetimes and alias analysis is vital for preventing undefined behavior (UB), avoiding security vulnerabilities like use-after-free, and allowing advanced compiler optimizations without breaking memory invariants.

## Chapter Directory
- [[01_Object_lifetime]] — Creation, storage activation, lifetime boundaries, and end-of-life destruction
- [[02_Storage_duration]] — Automatic, static, thread, and allocated storage durations
- [[03_Dangling_pointers]] — Pointer validity beyond object destruction and stack frame invalidation
- [[04_Use_after_free]] — Heap-based dangling references and catastrophic security implications
- [[05_Effective_type]] — ISO C dynamic type assignment rules and inspection constraints
- [[06_Strict_aliasing]] — The Type-Based Alias Analysis (TBAA) rule and type compatibility constraints
- [[07_Character_type_access]] — The universal alias exception for `char *`, `signed char *`, and `unsigned char *`
- [[08_Union_aliasing_nuances]] — Type punning via unions under ISO C vs POSIX / GNU C extensions
- [[09_restrict_and_alias_analysis]] — The `restrict` keyword, pointer independence, and loop vectorization
- [[10_Pointer_provenance_concerns]] — Address integers, pointer arithmetic wraparound, and provenance tracking
- [[11_Lifetime_safe_APIs]] — Design patterns for encapsulation, ownership transfer, and robust lifecycle contracts
- [[12_Sanitizer_backed_review]] — Leveraging AddressSanitizer (ASan) and UndefinedBehaviorSanitizer (UBSan) for validation

## Related Chapters
- [[../00_Complete_Topic_Map]]
- [[../25_C_Dynamic_Memory]]
- [[../27_C_Alignment_Object_Representation]]
