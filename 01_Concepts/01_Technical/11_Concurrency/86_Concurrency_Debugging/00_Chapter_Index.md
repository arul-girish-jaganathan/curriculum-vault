# 86 Concurrency Debugging

## Chapter map

- [[Reproduction|01. Reproduction]]
- [[Logging_Pitfalls|02. Logging Pitfalls]]
- [[Thread_Sanitizer|03. Thread Sanitizer]]
- [[Kernel_Lockdep|04. Kernel Lockdep]]
- [[KCSAN|05. KCSAN]]
- [[Helgrind_Alternatives|06. Helgrind Alternatives]]
- [[GDB_Thread_Debugging|07. GDB Thread Debugging]]
- [[Core_Dumps|08. Core Dumps]]
- [[Tracepoints|09. Tracepoints]]
- [[ftrace|10. ftrace]]
- [[perf|11. perf]]
- [[Systematic_Triage|12. Systematic Triage]]

## Chapter purpose
This chapter builds a reusable mental model for **Concurrency Debugging**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
