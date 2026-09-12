# C11 Concurrency and Atomics

C11 introduced a language-level concurrency model rather than leaving all synchronization to compiler extensions or operating-system APIs. The key abstraction is the atomic object and the associated memory-ordering rules. This matters in embedded firmware because interrupts, DMA, RTOS tasks and multiple cores create concurrency, but not every form of hardware concurrency is automatically covered by the C memory model.

## Atomic objects
An object declared with `_Atomic` or accessed through `<stdatomic.h>` atomic operations can participate in the C11 atomic model. Atomicity answers one question—whether an operation is indivisible with respect to other participating C threads. It does not by itself establish every ordering relationship a system needs.

Typical operations include load, store, exchange, compare-and-exchange, and read-modify-write operations such as fetch-add. Compare-and-exchange is the primitive behind many lock-free algorithms: observe an expected value and replace it only if the object still contains that value.

## Memory ordering
C11 provides `memory_order_relaxed`, `acquire`, `release`, `acq_rel`, `seq_cst`, and consume in the specification. The important engineering distinction is between atomicity and ordering. A relaxed atomic counter can prevent a data race on that counter without publishing the contents of a separate buffer. A release operation paired with an acquire operation can establish a happens-before relationship for preceding writes.

Example publication pattern:

```c
buffer[0] = value;
atomic_store_explicit(&ready, 1, memory_order_release);
```

A consumer that observes `ready == 1` with an acquire load can then safely observe the earlier buffer write under the C memory model, assuming the objects and algorithm satisfy the required rules.

## Embedded boundary
Do not equate C atomics with MMIO semantics, DMA coherency or interrupt synchronization. A peripheral register is not automatically a C atomic object merely because it is accessed with a volatile-qualified type. Conversely, a C atomic operation does not automatically perform every device-specific barrier required by an MCU bus or peripheral.

For an ISR/task shared variable, ask separately:
1. Is the access atomic at the language level?
2. Is there a C data race?
3. Is the ordering sufficient?
4. Does the CPU need an instruction barrier?
5. Does the peripheral/DMA subsystem require a device or cache-maintenance operation?

## Lock-free is not guaranteed
`atomic_is_lock_free()` allows software to discover whether an atomic type is lock-free for the implementation. “Lock-free” also does not mean wait-free: another thread can still repeatedly lose a compare-exchange loop.

## Common failure modes
- Using `volatile` as a replacement for synchronization.
- Making a flag atomic while leaving the associated buffer unsynchronized.
- Assuming naturally aligned loads/stores are automatically race-free in C.
- Applying a CPU barrier without establishing the corresponding language-level synchronization.
- Building a lock-free algorithm without considering ABA, starvation or progress guarantees.

## Verification
Review the happens-before graph, not just the instruction sequence. Use ThreadSanitizer where the target environment permits it, model-check small algorithms when appropriate, and inspect generated code only as a target-specific validation—not as the definition of the C memory model.

## Staff-level view
Concurrency design starts with an ownership and publication protocol. Choose the weakest ordering that is justified by that protocol, document why it is correct, and separately document hardware/cache/interrupt assumptions that sit outside ISO C.

## Related
- [[22_C_Concurrency_Atomics]]
- [[23_C_Memory_Model]]
- [[73_C_Concurrency_Patterns]]
- [[74_C_Memory_Order_Practice]]
- [[76_C_Atomicity_Embedded]]
