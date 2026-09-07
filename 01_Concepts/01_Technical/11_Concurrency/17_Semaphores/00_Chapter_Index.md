# 17 Semaphores

## Chapter map

- [[Counting_Semaphore|01. Counting Semaphore]]
- [[Binary_Semaphore|02. Binary Semaphore]]
- [[Resource_Counting|03. Resource Counting]]
- [[Event_Style_Usage|04. Event Style Usage]]
- [[Blocking_Semantics|05. Blocking Semantics]]
- [[Initial_Count|06. Initial Count]]
- [[Producer_Consumer|07. Producer Consumer]]
- [[ISR_Restrictions|08. ISR Restrictions]]
- [[Fairness|09. Fairness]]
- [[Semaphore_vs_Mutex|10. Semaphore vs Mutex]]
- [[Priority_Effects|11. Priority Effects]]
- [[Failure_Modes|12. Failure Modes]]

## Chapter purpose
This chapter builds a reusable mental model for **Semaphores**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
