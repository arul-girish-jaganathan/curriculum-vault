# 23: C Memory Model — Chapter Index

## Definition
The C Memory Model (formalized in ISO C11 §5.1.2.4) defines the semantic rules governing how multiple threads of execution interact through shared computer memory. It specifies the formal definitions of memory locations, data races, the modification order of objects, compiler instruction reordering boundaries, CPU hardware memory hierarchies, and the mathematical "happens-before" relationship required to guarantee predictable concurrent execution.

## Scope and Boundaries
Covers: Shared objects, data race definitions, happens-before relationships, modification order, synchronizes-with contracts, visible side effects, atomic vs. non-atomic accesses, memory tearing, compiler optimization reordering, hardware CPU pipeline reordering, the true semantics of `volatile`, and memory model debugging tools (TSan).
Does not cover: OS virtual memory management or cache hardware coherency bus protocols (MESI/MOESI) in silicon design.

## Topics in This Chapter
1. `01_Threads_and_shared_objects.md`: Memory locations, scalar objects, maximal contiguous bitfields, and shared state boundaries.
2. `02_Data_races.md`: The ISO C definition of a data race, unsequenced concurrent access, and why data races trigger Undefined Behavior.
3. `03_Happens_before.md`: Program order, dependency chains, strict partial ordering, and transitively visible operations.
4. `04_Modification_order.md`: Coherence per atomic object, total store ordering per variable, and read-read/write-write consistency.
5. `05_Synchronizes_with.md`: Inter-thread coordination, release sequences, and formal bridge-building between thread timelines.
6. `06_Visible_side_effects.md`: Determination of which write is visible to a given read, memory freshness, and visibility graphs.
7. `07_Atomic_vs_non_atomic_access.md`: Conflicting access rules, synchronization barriers, and the boundaries between raw and atomic memory.
8. `08_Tearing_considerations.md`: Word tearing, bus width limits, multi-instruction split loads/stores, and 64-bit risks on 32-bit MCUs.
9. `09_Compiler_reordering.md`: Compiler optimization passes, instruction hoisting/sinking, register caching, and compiler memory clobbers.
10. `10_Hardware_ordering.md`: Weakly ordered CPUs (ARM, RISC-V), out-of-order execution pipelines, store buffers, and CPU memory barriers.
11. `11_Volatile_is_not_synchronization.md`: The volatile myth, MMIO vs concurrency, lack of memory barriers, and compiler-only ordering.
12. `12_Memory_model_debugging.md`: Diagnosing race conditions, ThreadSanitizer (`-fsanitize=thread`), memory barrier validation, and hardware trace.

## Staff-Level Takeaway
The C memory model is a contract between software and hardware. Any concurrent read and write to the same memory location without synchronization is a Data Race that invites catastrophic Undefined Behavior. Never rely on `volatile` for inter-thread synchronization; `volatile` prevents only compiler register caching, not hardware instruction reordering. Master the formal "happens-before" relationship to build rock-solid concurrent systems.

## Related Concepts
- `../22_C_Concurrency_Atomics/01_Atomic_objects`
- `../22_C_Concurrency_Atomics/06_acquire_release`
- `../22_C_Concurrency_Atomics/11_Lock_free_queries`
- `../00_Complete_Topic_Map`
