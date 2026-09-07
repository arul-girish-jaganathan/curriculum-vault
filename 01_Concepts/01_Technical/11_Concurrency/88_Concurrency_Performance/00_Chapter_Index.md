# 88 Concurrency Performance Engineering

## Chapter map

- [[Contention|01. Contention]]
- [[Lock_Hold_Time|02. Lock Hold Time]]
- [[Wakeup_Cost|03. Wakeup Cost]]
- [[Context_Switch_Cost|04. Context Switch Cost]]
- [[Cache_Misses|05. Cache Misses]]
- [[False_Sharing|06. False Sharing]]
- [[Scalability|07. Scalability]]
- [[Amdahl|08. Amdahl]]
- [[Tail_Latency|09. Tail Latency]]
- [[CPU_Utilization|10. CPU Utilization]]
- [[Perf_Counters|11. Perf Counters]]
- [[Measurement_Method|12. Measurement Method]]

## Chapter purpose
This chapter builds a reusable mental model for **Concurrency Performance Engineering**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
