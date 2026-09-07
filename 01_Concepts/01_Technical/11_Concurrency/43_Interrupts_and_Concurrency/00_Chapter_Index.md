# 43 Interrupts and Concurrency

## Chapter map

- [[Interrupt_Context|01. Interrupt Context]]
- [[Thread_Context|02. Thread Context]]
- [[Shared_ISR_State|03. Shared ISR State]]
- [[Atomic_ISR_Updates|04. Atomic ISR Updates]]
- [[IRQ_Locking|05. IRQ Locking]]
- [[Interrupt_Masking|06. Interrupt Masking]]
- [[Nested_Interrupts|07. Nested Interrupts]]
- [[Priority_Levels|08. Priority Levels]]
- [[Deferred_Work|09. Deferred Work]]
- [[Memory_Ordering|10. Memory Ordering]]
- [[Teardown|11. Teardown]]
- [[Safety_Rules|12. Safety Rules]]

## Chapter purpose
This chapter builds a reusable mental model for **Interrupts and Concurrency**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
