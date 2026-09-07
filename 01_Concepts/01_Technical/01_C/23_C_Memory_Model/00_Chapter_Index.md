# C Memory Model

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Threads_and_shared_objects|Threads and shared objects]]
- [[02_Data_races|Data races]]
- [[03_Happens_before|Happens-before]]
- [[04_Modification_order|Modification order]]
- [[05_Synchronizes_with|Synchronizes-with]]
- [[06_Visible_side_effects|Visible side effects]]
- [[07_Atomic_vs_non_atomic_access|Atomic vs non-atomic access]]
- [[08_Tearing_considerations|Tearing considerations]]
- [[09_Compiler_reordering|Compiler reordering]]
- [[10_Hardware_ordering|Hardware ordering]]
- [[11_Volatile_is_not_synchronization|Volatile is not synchronization]]
- [[12_Memory_model_debugging|Memory-model debugging]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
