# 42 Context Switches

## Chapter map

- [[Trigger|01. Trigger]]
- [[Register_Save|02. Register Save]]
- [[Stack_Switch|03. Stack Switch]]
- [[Scheduler_Decision|04. Scheduler Decision]]
- [[Register_Restore|05. Register Restore]]
- [[Cache_Effects|06. Cache Effects]]
- [[TLB_Effects|07. TLB Effects]]
- [[FPU_Context|08. FPU Context]]
- [[Debugging|09. Debugging]]
- [[Switch_Cost|10. Switch Cost]]
- [[RTOS_Context_Switch|11. RTOS Context Switch]]
- [[Optimization|12. Optimization]]

## Chapter purpose
This chapter builds a reusable mental model for **Context Switches**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
