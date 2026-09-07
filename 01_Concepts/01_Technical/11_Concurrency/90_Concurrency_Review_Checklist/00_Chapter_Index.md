# 90 Concurrency Review Checklist

## Chapter map

- [[State_Ownership_Checklist|01. State Ownership Checklist]]
- [[Race_Checklist|02. Race Checklist]]
- [[Lock_Checklist|03. Lock Checklist]]
- [[Atomic_Checklist|04. Atomic Checklist]]
- [[Memory_Order_Checklist|05. Memory Order Checklist]]
- [[ISR_Checklist|06. ISR Checklist]]
- [[Lifecycle_Checklist|07. Lifecycle Checklist]]
- [[Shutdown_Checklist|08. Shutdown Checklist]]
- [[Performance_Checklist|09. Performance Checklist]]
- [[Testing_Checklist|10. Testing Checklist]]
- [[Documentation_Checklist|11. Documentation Checklist]]
- [[Staff_Sign_Off_Questions|12. Staff Sign-Off Questions]]

## Chapter purpose
This chapter builds a reusable mental model for **Concurrency Review Checklist**, with emphasis on correctness, timing, memory ordering, lifecycle, debugging, and embedded-system consequences.

## Cross-chapter reasoning
- Start with state ownership.
- Identify execution contexts and possible interleavings.
- State the synchronization edge or ownership transfer.
- Prove safety and liveness separately.
- Then evaluate latency, throughput, power, and maintainability.
