# 32 Compiler vs CPU Reordering

## Chapter map

- [[As_If_Rule|01. As-If Rule]]
- [[Compiler_Reordering|02. Compiler Reordering]]
- [[CPU_Reordering|03. CPU Reordering]]
- [[Out_of_Order_Execution|04. Out-of-Order Execution]]
- [[Speculation|05. Speculation]]
- [[Store_Buffering|06. Store Buffering]]
- [[Load_Buffering|07. Load Buffering]]
- [[Dependency_Effects|08. Dependency Effects]]
- [[Barriers|09. Barriers]]
- [[Volatile|10. Volatile]]
- [[Atomics|11. Atomics]]
- [[Disassembly_Analysis|12. Disassembly Analysis]]

## Chapter purpose
This chapter builds a reusable mental model for **Compiler vs CPU Reordering**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
