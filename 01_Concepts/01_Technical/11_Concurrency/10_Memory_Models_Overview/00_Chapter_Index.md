# 10 Memory Models Overview

## Chapter map

- [[Why_Memory_Models_Exist|01. Why Memory Models Exist]]
- [[Abstract_Machine|02. Abstract Machine]]
- [[Compiler_Reordering|03. Compiler Reordering]]
- [[CPU_Reordering|04. CPU Reordering]]
- [[Atomicity_Guarantees|05. Atomicity Guarantees]]
- [[Ordering_Guarantees|06. Ordering Guarantees]]
- [[Coherence_Guarantees|07. Coherence Guarantees]]
- [[Data_Race_Rules|08. Data Race Rules]]
- [[Sequential_Consistency|09. Sequential Consistency]]
- [[Weak_Memory|10. Weak Memory]]
- [[Language_vs_Hardware|11. Language vs Hardware]]
- [[Model_Selection|12. Model Selection]]

## Chapter purpose
This chapter builds a reusable mental model for **Memory Models Overview**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
