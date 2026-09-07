# 31 Relaxed Atomics

## Chapter map

- [[What_Relaxed_Means|01. What Relaxed Means]]
- [[Atomicity_Without_Ordering|02. Atomicity Without Ordering]]
- [[Counters|03. Counters]]
- [[Statistics|04. Statistics]]
- [[Flags_That_Need_No_Data_Publication|05. Flags That Need No Data Publication]]
- [[Reference_Counts|06. Reference Counts]]
- [[Memory_Reclamation_Caveats|07. Memory Reclamation Caveats]]
- [[Compiler_Effects|08. Compiler Effects]]
- [[CPU_Effects|09. CPU Effects]]
- [[Litmus_Tests|10. Litmus Tests]]
- [[Performance|11. Performance]]
- [[Misuse_Patterns|12. Misuse Patterns]]

## Chapter purpose
This chapter builds a reusable mental model for **Relaxed Atomics**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
