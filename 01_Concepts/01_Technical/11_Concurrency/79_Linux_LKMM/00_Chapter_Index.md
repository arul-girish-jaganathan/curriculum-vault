# 79 Linux Kernel Concurrency Model

## Chapter map

- [[Context_Classes|01. Context Classes]]
- [[Sleep_Rules|02. Sleep Rules]]
- [[Locking_Rules|03. Locking Rules]]
- [[IRQ_Safety|04. IRQ Safety]]
- [[Preemption_Safety|05. Preemption Safety]]
- [[Atomic_Context|06. Atomic Context]]
- [[RCU|07. RCU]]
- [[LKMM|08. LKMM]]
- [[Lockdep|09. Lockdep]]
- [[Debug_Configs|10. Debug Configs]]
- [[Subsystem_Patterns|11. Subsystem Patterns]]
- [[Review_Method|12. Review Method]]

## Chapter purpose
This chapter builds a reusable mental model for **Linux Kernel Concurrency Model**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
