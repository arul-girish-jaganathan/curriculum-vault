# 70 Linux POSIX Threads

## Chapter map

- [[pthread_create|01. pthread_create]]
- [[Attributes|02. Attributes]]
- [[Join_and_Detach|03. Join and Detach]]
- [[Scheduling_Attributes|04. Scheduling Attributes]]
- [[Affinity|05. Affinity]]
- [[TLS|06. TLS]]
- [[Cancellation|07. Cancellation]]
- [[Robust_Mutex|08. Robust Mutex]]
- [[Condition_Variables|09. Condition Variables]]
- [[Semaphores|10. Semaphores]]
- [[Signals|11. Signals]]
- [[Debugging|12. Debugging]]

## Chapter purpose
This chapter builds a reusable mental model for **Linux POSIX Threads**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
