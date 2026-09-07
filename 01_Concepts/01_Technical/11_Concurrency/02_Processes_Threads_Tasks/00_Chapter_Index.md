# 02 Processes Threads and Tasks

## Chapter map

- [[Process_Isolation|01. Process Isolation]]
- [[Threads|02. Threads]]
- [[RTOS_Tasks|03. RTOS Tasks]]
- [[Kernel_Threads|04. Kernel Threads]]
- [[User_Threads|05. User Threads]]
- [[Execution_Context|06. Execution Context]]
- [[Stacks|07. Stacks]]
- [[Thread_IDs|08. Thread IDs]]
- [[Lifecycle_Ownership|09. Lifecycle Ownership]]
- [[Shared_Address_Space|10. Shared Address Space]]
- [[Thread_to_Task_Mapping|11. Thread-to-Task Mapping]]
- [[Design_Trade_offs|12. Design Trade-offs]]

## Chapter purpose
This chapter builds a reusable mental model for **Processes Threads and Tasks**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
