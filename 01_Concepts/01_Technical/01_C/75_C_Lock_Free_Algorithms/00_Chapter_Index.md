# Lock-free and Wait-free Algorithms

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Progress_guarantees|Progress guarantees]]
- [[02_CAS_loops|CAS loops]]
- [[03_Fetch_add|Fetch-add]]
- [[04_Exchange|Exchange]]
- [[05_ABA_problem|ABA problem]]
- [[06_Tagged_pointers|Tagged pointers]]
- [[07_Hazard_pointer_concepts|Hazard-pointer concepts]]
- [[08_Epoch_reclamation|Epoch reclamation]]
- [[09_Single_writer_structures|Single-writer structures]]
- [[10_Bounded_lock_free_queues|Bounded lock-free queues]]
- [[11_Memory_reclamation|Memory reclamation]]
- [[12_Validation_strategy|Validation strategy]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
