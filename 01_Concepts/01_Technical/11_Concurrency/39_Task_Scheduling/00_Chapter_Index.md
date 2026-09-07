# 39 Task Scheduling

## Chapter map

- [[Runnable_Queues|01. Runnable Queues]]
- [[Dispatch|02. Dispatch]]
- [[Scheduler_Tick|03. Scheduler Tick]]
- [[Preemption_Points|04. Preemption Points]]
- [[Latency|05. Latency]]
- [[Fairness|06. Fairness]]
- [[Priority|07. Priority]]
- [[Affinity|08. Affinity]]
- [[Load_Balancing|09. Load Balancing]]
- [[Deadlines|10. Deadlines]]
- [[Blocking|11. Blocking]]
- [[Scheduling_Review|12. Scheduling Review]]

## Chapter purpose
This chapter builds a reusable mental model for **Task Scheduling**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
