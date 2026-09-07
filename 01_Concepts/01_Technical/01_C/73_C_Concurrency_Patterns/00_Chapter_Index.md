# Concurrency Patterns in C

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Single_producer_single_consumer|Single-producer single-consumer]]
- [[02_Multi_producer_queues|Multi-producer queues]]
- [[03_Work_stealing_concepts|Work stealing concepts]]
- [[04_Double_buffering|Double buffering]]
- [[05_RCU_like_patterns|RCU-like patterns]]
- [[06_Read_mostly_designs|Read-mostly designs]]
- [[07_Reference_counting|Reference counting]]
- [[08_Epoch_based_reclamation_concepts|Epoch-based reclamation concepts]]
- [[09_Lock_hierarchy|Lock hierarchy]]
- [[10_Message_passing|Message passing]]
- [[11_Interrupt_to_thread_handoff|Interrupt-to-thread handoff]]
- [[12_Backpressure|Backpressure]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
