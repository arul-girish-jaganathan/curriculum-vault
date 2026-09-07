# 54 Starvation

## Chapter map

- [[Definition|01. Definition]]
- [[Lock_Starvation|02. Lock Starvation]]
- [[Scheduler_Starvation|03. Scheduler Starvation]]
- [[Writer_Starvation|04. Writer Starvation]]
- [[Priority_Starvation|05. Priority Starvation]]
- [[Fairness|06. Fairness]]
- [[Aging|07. Aging]]
- [[Backoff|08. Backoff]]
- [[Queueing|09. Queueing]]
- [[Timeouts|10. Timeouts]]
- [[Mitigation|11. Mitigation]]
- [[Measurement|12. Measurement]]

## Chapter purpose
This chapter builds a reusable mental model for **Starvation**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
