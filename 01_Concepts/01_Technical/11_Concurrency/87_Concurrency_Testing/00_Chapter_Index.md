# 87 Concurrency Testing

## Chapter map

- [[Stress_Testing|01. Stress Testing]]
- [[Randomized_Scheduling|02. Randomized Scheduling]]
- [[Fault_Injection|03. Fault Injection]]
- [[Thread_Sanitizer_CI|04. Thread Sanitizer CI]]
- [[Litmus_Tests|05. Litmus Tests]]
- [[Model_Checking|06. Model Checking]]
- [[Property_Testing|07. Property Testing]]
- [[Race_Detection|08. Race Detection]]
- [[Timeout_Testing|09. Timeout Testing]]
- [[Shutdown_Testing|10. Shutdown Testing]]
- [[Soak_Testing|11. Soak Testing]]
- [[Testability_Design|12. Testability Design]]

## Chapter purpose
This chapter builds a reusable mental model for **Concurrency Testing**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
