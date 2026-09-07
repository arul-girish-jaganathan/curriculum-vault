# 24 Atomic Operations

## Chapter map

- [[Atomic_Load_Store|01. Atomic Load Store]]
- [[Atomic_RMW|02. Atomic RMW]]
- [[Atomic_Counters|03. Atomic Counters]]
- [[Atomic_Flags|04. Atomic Flags]]
- [[Atomic_Pointers|05. Atomic Pointers]]
- [[Atomic_Enums|06. Atomic Enums]]
- [[Atomic_Struct_Alternatives|07. Atomic Struct Alternatives]]
- [[Atomic_Alignment|08. Atomic Alignment]]
- [[Lock_Free_Query|09. Lock-Free Query]]
- [[Spurious_Failure|10. Spurious Failure]]
- [[Signal_Safety|11. Signal Safety]]
- [[Design_Rules|12. Design Rules]]

## Chapter purpose
This chapter builds a reusable mental model for **Atomic Operations**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
