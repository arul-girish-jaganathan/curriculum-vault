# C11 Threads and Thread Lifecycle

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_thrd_create|thrd_create]]
- [[02_thrd_join|thrd_join]]
- [[03_thrd_detach|thrd_detach]]
- [[04_Thread_return_values|Thread return values]]
- [[05_Mutexes|Mutexes]]
- [[06_Condition_variables|Condition variables]]
- [[07_Thread_local_storage|Thread-local storage]]
- [[08_Call_once|Call_once]]
- [[09_Thread_cancellation_boundaries|Thread cancellation boundaries]]
- [[10_C11_thread_portability|C11 thread portability]]
- [[11_Freestanding_limitations|Freestanding limitations]]
- [[12_Thread_safe_module_design|Thread-safe module design]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
