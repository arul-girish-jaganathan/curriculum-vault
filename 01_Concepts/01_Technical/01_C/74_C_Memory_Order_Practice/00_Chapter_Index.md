# Practical Memory Ordering

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Relaxed_counters|Relaxed counters]]
- [[02_Acquire_loads|Acquire loads]]
- [[03_Release_stores|Release stores]]
- [[04_Acquire_release_RMW|Acquire-release RMW]]
- [[05_Seq_cst_design|Seq-cst design]]
- [[06_Release_sequences|Release sequences]]
- [[07_Atomic_fences|Atomic fences]]
- [[08_Compiler_barriers|Compiler barriers]]
- [[09_CPU_barriers|CPU barriers]]
- [[10_Device_ordering|Device ordering]]
- [[11_Lock_implementation_reasoning|Lock implementation reasoning]]
- [[12_Litmus_test_thinking|Litmus-test thinking]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
