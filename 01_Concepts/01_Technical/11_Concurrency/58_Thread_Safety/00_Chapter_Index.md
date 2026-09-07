# 58 Thread Safety

## Chapter map

- [[Definition|01. Definition]]
- [[Safe_by_Immutability|02. Safe by Immutability]]
- [[Safe_by_Ownership|03. Safe by Ownership]]
- [[Safe_by_Locking|04. Safe by Locking]]
- [[Safe_by_Atomics|05. Safe by Atomics]]
- [[Thread_Compatible_APIs|06. Thread-Compatible APIs]]
- [[Thread_Compatible_Objects|07. Thread-Compatible Objects]]
- [[Exception_Safety|08. Exception Safety]]
- [[Cancellation_Safety|09. Cancellation Safety]]
- [[Destruction_Safety|10. Destruction Safety]]
- [[Documentation|11. Documentation]]
- [[Review|12. Review]]

## Chapter purpose
This chapter builds a reusable mental model for **Thread Safety**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
