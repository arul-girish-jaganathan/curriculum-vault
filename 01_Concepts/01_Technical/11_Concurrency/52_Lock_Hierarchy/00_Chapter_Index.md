# 52 Lock Hierarchy and Ordering

## Chapter map

- [[Global_Lock_Order|01. Global Lock Order]]
- [[Nested_Locking|02. Nested Locking]]
- [[Lock_Classes|03. Lock Classes]]
- [[ABBA_Deadlock|04. ABBA Deadlock]]
- [[Trylock|05. Trylock]]
- [[Hierarchy_Documentation|06. Hierarchy Documentation]]
- [[Dynamic_Lock_Sets|07. Dynamic Lock Sets]]
- [[Interrupt_Lock_Ordering|08. Interrupt Lock Ordering]]
- [[Callback_Under_Lock|09. Callback Under Lock]]
- [[Lockdep_Concepts|10. Lockdep Concepts]]
- [[Refactoring_Locks|11. Refactoring Locks]]
- [[Review_Checklist|12. Review Checklist]]

## Chapter purpose
This chapter builds a reusable mental model for **Lock Hierarchy and Ordering**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
