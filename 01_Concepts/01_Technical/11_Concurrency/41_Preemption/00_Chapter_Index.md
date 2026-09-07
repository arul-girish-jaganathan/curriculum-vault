# 41 Preemption

## Chapter map

- [[Preemptive_Scheduling|01. Preemptive Scheduling]]
- [[Cooperative_Scheduling|02. Cooperative Scheduling]]
- [[Preemption_Disable|03. Preemption Disable]]
- [[Preemption_Windows|04. Preemption Windows]]
- [[Critical_Sections|05. Critical Sections]]
- [[IRQ_Preemption|06. IRQ Preemption]]
- [[Kernel_Preemption|07. Kernel Preemption]]
- [[Latency|08. Latency]]
- [[Reentrancy|09. Reentrancy]]
- [[Nested_Preemption|10. Nested Preemption]]
- [[Real_Time_Consequences|11. Real-Time Consequences]]
- [[Review|12. Review]]

## Chapter purpose
This chapter builds a reusable mental model for **Preemption**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
