# 22: C Concurrency Atomics — Chapter Index

## Definition
Concurrency atomicity in C (formalized in ISO C11 `<stdatomic.h>`) provides language-level primitives for performing lock-free synchronization, memory ordering, and thread-safe data access without invoking undefined data races. In embedded systems, multi-core microcontrollers, and real-time operating systems (RTOS), atomic operations provide the foundational machinery for lock-free queues, interrupt-to-thread communication, spinlocks, and hardware synchronization barriers.

## Scope and Boundaries
Covers: C11 `<stdatomic.h>`, `_Atomic` type qualifier, atomic load and store operations, read-modify-write (RMW) primitives, compare-exchange (weak vs strong), memory ordering semantics (`memory_order_relaxed`, `acquire`, `release`, `acq_rel`, `seq_cst`), atomic flags, atomic pointers, lock-free queries, and lock-free data structure design.
Does not cover: OS-level kernel mutexes, POSIX pthread lifecycle APIs, or C++ std::atomic extensions.

## Topics in This Chapter
1. `01_Atomic_objects.md`: `_Atomic` qualifier, atomic types (`atomic_int`, `atomic_uintptr_t`), and memory layout.
2. `02_Atomic_load_store.md`: Explicit load/store operations, torn-read prevention, and baseline thread safety.
3. `03_Read_modify_write.md`: Fetch-and-add, fetch-and-sub, bitwise atomic RMW, and single-cycle ALU execution.
4. `04_compare_exchange.md`: CAS primitives, `atomic_compare_exchange_weak` vs `strong`, and spurious failure loops.
5. `05_memory_order_relaxed.md`: Relaxed ordering, atomicity without synchronization, hardware counter patterns, and hazards.
6. `06_acquire_release.md`: Acquire-release semantics, one-way barriers, message passing, and producer-consumer synchronization.
7. `07_acq_rel.md`: Bidirectional barriers, read-modify-write synchronization, and atomic counter rendezvous.
8. `08_seq_cst.md`: Sequential consistency, total global store order, SC costs on weakly ordered CPUs, and default pitfalls.
9. `09_Atomic_flags.md`: `atomic_flag`, test-and-set operations, lock-free guarantees across all platforms, and spinlocks.
10. `10_Atomic_pointers.md`: Lock-free pointer manipulation, ABA mitigation, and memory publishing patterns.
11. `11_Lock_free_queries.md`: `atomic_is_lock_free`, lock-freedom vs wait-freedom, and software-emulated mutex traps.
12. `12_Atomic_API_design.md`: Lock-free ring buffers, RTOS/ISR synchronization, memory barriers, and MISRA C concurrency rules.

## Staff-Level Takeaway
Atomics in C11 provide precise hardware synchronization contracts. Never default blindly to `memory_order_seq_cst` on weakly ordered processors (ARM, RISC-V), as it emits expensive memory barrier instructions (`DMB ISH`). Master `acquire-release` semantics for lock-free ring buffers, verify lock-freedom via `atomic_is_lock_free()`, and remember that `volatile` is NOT atomic.

## Related Concepts
- `../23_C_Memory_Model/01_Threads_and_shared_objects`
- `../23_C_Memory_Model/05_Synchronizes_with`
- `../23_C_Memory_Model/11_Volatile_is_not_synchronization`
- `../00_Complete_Topic_Map`
