# 40 Priority and Scheduling

## Chapter map

- [[Priority_Semantics|01. Priority Semantics]]
- [[Static_Priority|02. Static Priority]]
- [[Dynamic_Priority|03. Dynamic Priority]]
- [[Priority_Inversion|04. Priority Inversion]]
- [[Priority_Inheritance|05. Priority Inheritance]]
- [[Priority_Ceiling|06. Priority Ceiling]]
- [[Aging|07. Aging]]
- [[Fairness|08. Fairness]]
- [[Deadline_Scheduling|09. Deadline Scheduling]]
- [[Priority_Mapping|10. Priority Mapping]]
- [[Cross_OS_Differences|11. Cross-OS Differences]]
- [[Design_Rules|12. Design Rules]]

## Chapter purpose
This chapter builds a reusable mental model for **Priority and Scheduling**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
