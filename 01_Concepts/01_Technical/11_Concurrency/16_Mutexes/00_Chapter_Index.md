# 16 Mutexes

## Chapter map

- [[Mutex_Semantics|01. Mutex Semantics]]
- [[Ownership|02. Ownership]]
- [[Blocking|03. Blocking]]
- [[Recursive_Mutexes|04. Recursive Mutexes]]
- [[Error_Checking_Mutexes|05. Error-Checking Mutexes]]
- [[Priority_Inheritance|06. Priority Inheritance]]
- [[Priority_Ceiling|07. Priority Ceiling]]
- [[Robust_Mutexes|08. Robust Mutexes]]
- [[Lock_Scope|09. Lock Scope]]
- [[Mutex_Contention|10. Mutex Contention]]
- [[Mutex_Deadlocks|11. Mutex Deadlocks]]
- [[Embedded_Usage|12. Embedded Usage]]

## Chapter purpose
This chapter builds a reusable mental model for **Mutexes**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
