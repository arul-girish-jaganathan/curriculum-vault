# 24_C_Threads_C11: Chapter Index

## Overview
C11 introduced standard multi-threading support into ISO C (`<threads.h>`), providing a portable threading model across platforms without requiring POSIX Threads (pthreads) or Windows Win32 thread APIs. This chapter comprehensively explores the C11 threading model, synchronization primitives, thread-local storage, memory visibility boundaries, freestanding implementation constraints, and resilient thread-safe module architecture.

## Chapter Directory
- [[01_thrd_create]] — Thread creation, entry-point semantics, and parameter passing
- [[02_thrd_join]] — Thread synchronization, rendezvous semantics, and resource reclamation
- [[03_thrd_detach]] — Background execution, detached lifecycle, and leak prevention
- [[04_Thread_return_values]] — Passing results from thread routines and status code handling
- [[05_Mutexes]] — `mtx_t` types, recursive/timed locks, and priority inversion prevention
- [[06_Condition_variables]] — `cnd_t` signaling, spurious wakeups, and predicate loops
- [[07_Thread_local_storage]] — `thread_local` / `_Thread_local`, storage duration, and link-time cost
- [[08_Call_once]] — `once_flag` and `call_once()` idempotent initialization
- [[09_Thread_cancellation_boundaries]] — Graceful termination, cooperative cancellation, and cleanup guarantees
- [[10_C11_thread_portability]] — Compatibility across Linux, POSIX, Windows, and RTOS targets
- [[11_Freestanding_limitations]] — Thread support in bare-metal, embedded freestanding environments (`__STDC_NO_THREADS__`)
- [[12_Thread_safe_module_design]] — Reentrancy, module state encapsulation, lock ordering, and deadlock prevention

## Related Chapters
- [[../00_Complete_Topic_Map]]
- [[../23_C11_Atomics]]
- [[../22_Concurrency_and_Memory_Models]]
