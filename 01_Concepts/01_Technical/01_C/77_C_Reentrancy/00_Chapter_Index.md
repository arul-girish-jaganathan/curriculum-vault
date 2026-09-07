# Reentrancy and Thread Safety in C APIs

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Reentrant_functions|Reentrant functions]]
- [[02_Static_state_hazards|Static state hazards]]
- [[03_errno_style_per_thread_state|errno-style per-thread state]]
- [[04_Context_passing_APIs|Context-passing APIs]]
- [[05_Nested_callbacks|Nested callbacks]]
- [[06_Signal_reentrancy|Signal reentrancy]]
- [[07_ISR_reentrancy|ISR reentrancy]]
- [[08_Locking_around_libraries|Locking around libraries]]
- [[09_Thread_safe_vs_reentrant|Thread-safe vs reentrant]]
- [[10_Documentation_patterns|Documentation patterns]]
- [[11_Testing_reentrancy|Testing reentrancy]]
- [[12_Designing_pure_helpers|Designing pure helpers]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
