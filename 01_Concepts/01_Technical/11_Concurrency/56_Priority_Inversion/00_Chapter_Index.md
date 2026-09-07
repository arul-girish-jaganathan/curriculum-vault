# 56 Priority Inversion

## Chapter map

- [[Basic_Scenario|01. Basic Scenario]]
- [[Unbounded_Inversion|02. Unbounded Inversion]]
- [[Priority_Inheritance|03. Priority Inheritance]]
- [[Priority_Ceiling|04. Priority Ceiling]]
- [[Ceiling_Protocol|05. Ceiling Protocol]]
- [[Nested_Locks|06. Nested Locks]]
- [[Semaphores_vs_Mutexes|07. Semaphores vs Mutexes]]
- [[RTOS_Handling|08. RTOS Handling]]
- [[Linux_PI_Futex|09. Linux PI Futex]]
- [[Timing_Analysis|10. Timing Analysis]]
- [[Debugging|11. Debugging]]
- [[Review|12. Review]]

## Chapter purpose
This chapter builds a reusable mental model for **Priority Inversion**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
