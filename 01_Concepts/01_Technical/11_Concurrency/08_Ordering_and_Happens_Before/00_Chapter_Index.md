# 08 Ordering and Happens-Before

## Chapter map

- [[Program_Order|01. Program Order]]
- [[Happens_Before|02. Happens-Before]]
- [[Synchronizes_With|03. Synchronizes-With]]
- [[Dependency_Ordering|04. Dependency Ordering]]
- [[Transitive_Ordering|05. Transitive Ordering]]
- [[Publication|06. Publication]]
- [[Consumption|07. Consumption]]
- [[Initialization_Ordering|08. Initialization Ordering]]
- [[Teardown_Ordering|09. Teardown Ordering]]
- [[Cross_CPU_Ordering|10. Cross-CPU Ordering]]
- [[Reasoning_Graphs|11. Reasoning Graphs]]
- [[Ordering_Review|12. Ordering Review]]

## Chapter purpose
This chapter builds a reusable mental model for **Ordering and Happens-Before**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
