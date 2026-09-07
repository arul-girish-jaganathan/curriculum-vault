# 36 Thread Lifecycle

## Chapter map

- [[Creation|01. Creation]]
- [[Runnable_State|02. Runnable State]]
- [[Running_State|03. Running State]]
- [[Blocked_State|04. Blocked State]]
- [[Joinable_State|05. Joinable State]]
- [[Detached_State|06. Detached State]]
- [[Cancellation|07. Cancellation]]
- [[Exit_Paths|08. Exit Paths]]
- [[Cleanup|09. Cleanup]]
- [[Thread_Death_Races|10. Thread Death Races]]
- [[Lifecycle_Ownership|11. Lifecycle Ownership]]
- [[Shutdown_Design|12. Shutdown Design]]

## Chapter purpose
This chapter builds a reusable mental model for **Thread Lifecycle**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
