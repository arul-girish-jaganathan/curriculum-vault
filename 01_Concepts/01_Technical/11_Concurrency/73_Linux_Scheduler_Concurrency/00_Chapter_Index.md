# 73 Linux Scheduler Concurrency

## Chapter map

- [[CFS_Concepts|01. CFS Concepts]]
- [[Realtime_Classes|02. Realtime Classes]]
- [[Runqueue_Locking|03. Runqueue Locking]]
- [[Load_Balancing|04. Load Balancing]]
- [[CPU_Affinity|05. CPU Affinity]]
- [[Preemption|06. Preemption]]
- [[Wakeup_Paths|07. Wakeup Paths]]
- [[Scheduler_Tick|08. Scheduler Tick]]
- [[NOHZ|09. NOHZ]]
- [[Priority|10. Priority]]
- [[Context_Switch_Metrics|11. Context Switch Metrics]]
- [[Scheduler_Debugging|12. Scheduler Debugging]]

## Chapter purpose
This chapter builds a reusable mental model for **Linux Scheduler Concurrency**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
