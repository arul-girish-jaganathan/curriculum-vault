# 80 RTOS Concurrency

## Chapter map

- [[Task_Synchronization|01. Task Synchronization]]
- [[Task_Priorities|02. Task Priorities]]
- [[Critical_Sections|03. Critical Sections]]
- [[Mutexes|04. Mutexes]]
- [[Semaphores|05. Semaphores]]
- [[Queues|06. Queues]]
- [[Event_Groups|07. Event Groups]]
- [[Notifications|08. Notifications]]
- [[ISR_APIs|09. ISR APIs]]
- [[Tick_and_Timeout|10. Tick and Timeout]]
- [[SMP_RTOS|11. SMP RTOS]]
- [[Deterministic_Design|12. Deterministic Design]]

## Chapter purpose
This chapter builds a reusable mental model for **RTOS Concurrency**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
