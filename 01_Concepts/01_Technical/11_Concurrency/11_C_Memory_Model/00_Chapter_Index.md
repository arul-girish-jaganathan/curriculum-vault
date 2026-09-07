# 11 C Memory Model

## Chapter map

- [[C11_Threads_Model|01. C11 Threads Model]]
- [[Atomic|02. _Atomic]]
- [[Atomic_Types|03. Atomic Types]]
- [[Memory_Orders|04. Memory Orders]]
- [[Sequenced_Before|05. Sequenced Before]]
- [[Happens_Before|06. Happens Before]]
- [[Data_Race_Undefined_Behavior|07. Data Race Undefined Behavior]]
- [[Volatile|08. Volatile]]
- [[Atomic_Flag|09. Atomic Flag]]
- [[Atomic_Pointer|10. Atomic Pointer]]
- [[Fence_Semantics|11. Fence Semantics]]
- [[C_Memory_Model_Pitfalls|12. C Memory Model Pitfalls]]

## Chapter purpose
This chapter builds a reusable mental model for **C Memory Model**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
