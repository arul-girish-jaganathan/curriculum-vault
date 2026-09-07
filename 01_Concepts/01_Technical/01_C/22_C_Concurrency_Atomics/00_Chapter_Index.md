# C Atomics and Concurrent Access

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Atomic_objects|_Atomic objects]]
- [[02_Atomic_load_store|Atomic load/store]]
- [[03_Read_modify_write|Read-modify-write]]
- [[04_compare_exchange|compare_exchange]]
- [[05_memory_order_relaxed|memory_order_relaxed]]
- [[06_acquire_release|acquire/release]]
- [[07_acq_rel|acq_rel]]
- [[08_seq_cst|seq_cst]]
- [[09_Atomic_flags|Atomic flags]]
- [[10_Atomic_pointers|Atomic pointers]]
- [[11_Lock_free_queries|Lock-free queries]]
- [[12_Atomic_API_design|Atomic API design]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
