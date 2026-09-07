# 21 Condition Variables

## Chapter map

- [[Wait_Predicate_Pattern|01. Wait-Predicate Pattern]]
- [[Mutex_Association|02. Mutex Association]]
- [[Spurious_Wakeups|03. Spurious Wakeups]]
- [[Signal_vs_Broadcast|04. Signal vs Broadcast]]
- [[Lost_Wakeups|05. Lost Wakeups]]
- [[Condition_State|06. Condition State]]
- [[Timed_Waits|07. Timed Waits]]
- [[Cancellation|08. Cancellation]]
- [[Producer_Consumer|09. Producer Consumer]]
- [[Multiple_Predicates|10. Multiple Predicates]]
- [[C_Mapping|11. C++ Mapping]]
- [[POSIX_Mapping|12. POSIX Mapping]]

## Chapter purpose
This chapter builds a reusable mental model for **Condition Variables**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
