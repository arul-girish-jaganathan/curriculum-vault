# 29 Release Acquire

## Chapter map

- [[Publication_Pattern|01. Publication Pattern]]
- [[Producer_Consumer|02. Producer Consumer]]
- [[Pointer_Publication|03. Pointer Publication]]
- [[Initialization_Safety|04. Initialization Safety]]
- [[Acquire_Load|05. Acquire Load]]
- [[Release_Store|06. Release Store]]
- [[RMW_Acq_Rel|07. RMW Acq Rel]]
- [[Transitive_Synchronization|08. Transitive Synchronization]]
- [[Fence_Variants|09. Fence Variants]]
- [[C_Example|10. C++ Example]]
- [[C_Example|11. C Example]]
- [[Common_Misproofs|12. Common Misproofs]]

## Chapter purpose
This chapter builds a reusable mental model for **Release Acquire**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
