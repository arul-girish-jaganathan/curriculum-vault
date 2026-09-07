# 67 C++ Atomics

## Chapter map

- [[std_atomic|01. std::atomic]]
- [[atomic_flag|02. atomic_flag]]
- [[atomic_ref|03. atomic_ref]]
- [[fetch_Operations|04. fetch Operations]]
- [[exchange|05. exchange]]
- [[compare_exchange|06. compare_exchange]]
- [[wait|07. wait]]
- [[notify_one|08. notify_one]]
- [[notify_all|09. notify_all]]
- [[is_lock_free|10. is_lock_free]]
- [[Atomic_Smart_Pointer|11. Atomic Smart Pointer]]
- [[Memory_Orders|12. Memory Orders]]

## Chapter purpose
This chapter builds a reusable mental model for **C++ Atomics**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
