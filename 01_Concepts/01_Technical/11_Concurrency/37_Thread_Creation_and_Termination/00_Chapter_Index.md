# 37 Thread Creation and Termination

## Chapter map

- [[pthread_create|01. pthread_create]]
- [[pthread_join|02. pthread_join]]
- [[pthread_detach|03. pthread_detach]]
- [[Attributes|04. Attributes]]
- [[Start_Routine|05. Start Routine]]
- [[Argument_Passing|06. Argument Passing]]
- [[Return_Values|07. Return Values]]
- [[Thread_Exit|08. Thread Exit]]
- [[Cancellation_Points|09. Cancellation Points]]
- [[Cleanup_Handlers|10. Cleanup Handlers]]
- [[C_Thread_Destruction|11. C++ Thread Destruction]]
- [[RTOS_Task_Delete|12. RTOS Task Delete]]

## Chapter purpose
This chapter builds a reusable mental model for **Thread Creation and Termination**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
