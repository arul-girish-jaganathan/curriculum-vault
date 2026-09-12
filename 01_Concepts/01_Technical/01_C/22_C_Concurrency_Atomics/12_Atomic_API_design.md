# 12: Atomic API Design

## Definition
Atomic API design is the architectural discipline of constructing thread-safe, lock-free, and reentrant interfaces using C11 atomic primitives. It focuses on encapsulating synchronization mechanics inside clean module boundaries, ensuring wait-free execution for real-time threads and Interrupt Service Routines (ISRs) while preventing concurrency bugs.

## Scope and Boundaries
Covers: Single-Producer Single-Consumer (SPSC) lock-free ring buffers, interrupt-to-thread queues, memory barrier containment, and MISRA C concurrency rules.
Does not cover: Multi-Producer Multi-Consumer (MPMC) lock-free algorithms (which require complex CAS hazard pointer schemes).

## Why Does It Exist
In embedded firmware, ISRs cannot wait on OS mutexes, and disabling global interrupts (`__disable_irq()`) introduces unacceptable interrupt latency for motor control, audio, or high-speed communication. Well-designed lock-free atomic APIs enable instantaneous, zero-lock data exchange between interrupt contexts and worker threads.

## Mechanism and Language Rules
1. **Separation of Concerns:** Keep synchronization variables private; expose only clean, semantic functions (`push()`, `pop()`) to callers.
2. **SPSC Invariance:** In a Single-Producer Single-Consumer queue:
   - Only the producer modifies the `head` index.
   - Only the consumer modifies the `tail` index.
   - Full acquire-release synchronization ensures that payload data is fully written before `head` advances.

## Examples
```c
/* ================= LOCK-FREE SPSC RING BUFFER API ================= */
#include <stdatomic.h>
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#define RING_BUFFER_CAPACITY 64U /* Power of 2 for fast modulo masking */
#define RING_BUFFER_MASK     (RING_BUFFER_CAPACITY - 1U)

typedef struct {
    uint8_t              storage[RING_BUFFER_CAPACITY];
    atomic_uint_fast32_t head; /* Written by Producer only */
    atomic_uint_fast32_t tail; /* Written by Consumer only */
} LockFreeSpsc_t;

void spsc_init(LockFreeSpsc_t *q) {
    atomic_init(&q->head, 0U);
    atomic_init(&q->tail, 0U);
}

/* Producer (e.g., UART RX ISR) - Wait-Free */
bool spsc_push(LockFreeSpsc_t *q, uint8_t byte) {
    uint32_t current_head = atomic_load_explicit(&q->head, memory_order_relaxed);
    uint32_t current_tail = atomic_load_explicit(&q->tail, memory_order_acquire);

    if (((current_head + 1U) & RING_BUFFER_MASK) == current_tail) {
        return false; /* Buffer full */
    }

    q->storage[current_head] = byte; /* Non-atomic write to exclusive slot */
    
    /* Release store publishes data byte to consumer */
    atomic_store_explicit(&q->head, (current_head + 1U) & RING_BUFFER_MASK, memory_order_release);
    return true;
}

/* Consumer (e.g., Background Application Task) - Wait-Free */
bool spsc_pop(LockFreeSpsc_t *q, uint8_t *out_byte) {
    uint32_t current_tail = atomic_load_explicit(&q->tail, memory_order_relaxed);
    uint32_t current_head = atomic_load_explicit(&q->head, memory_order_acquire);

    if (current_head == current_tail) {
        return false; /* Buffer empty */
    }

    *out_byte = q->storage[current_tail]; /* Read exclusive slot */
    
    /* Release store updates tail, freeing slot for producer */
    atomic_store_explicit(&q->tail, (current_tail + 1U) & RING_BUFFER_MASK, memory_order_release);
    return true;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Allowing multiple threads to call `spsc_push()` concurrently without a mutex breaks SPSC assumptions and results in data corruption.

## Edge Cases and Failure Modes
- **Power-of-Two Sizing:** If buffer capacity is not a power of 2, the bitwise mask `& (CAPACITY - 1)` fails, causing buffer over-reads. Always enforce power-of-two sizing with `static_assert`.

## Embedded Implications
- **Zero Interrupt Latency:** An ISR pushing to this queue executes in ~15 CPU cycles with zero interrupt disabling, guaranteeing deterministic real-time responsiveness.

## Firmware Review Angle
- Confirm that the ring buffer capacity is locked to a power of 2 via compile-time assertions:
  `_Static_assert((CAPACITY & (CAPACITY - 1)) == 0, "Capacity must be power of 2");`.
- Verify that SPSC queues are NEVER accessed by more than one producer thread.

## Compiler, ABI, and Toolchain Implications
- Generates optimal machine code on ARM Cortex-M: load-exclusive, bitwise mask, store-release.

## Performance, Memory, Timing, and Power
- True wait-free progress: both push and pop operations execute in deterministic $O(1)$ time with zero loops or locks.

## Verification / Debugging
- Unit-test under stress tests passing millions of packets between high-rate timer ISRs and main thread consumers.

## Safety, Security, and Reliability
- Complies with MISRA C:2012 Amendment 4 concurrency requirements by providing strict encapsulation of atomic variables.

## Trade-offs and Alternatives
- **Lock-Free SPSC vs RTOS Queue:** An SPSC atomic queue is 50x faster than an RTOS message queue, but supports only one consumer and one producer.

## Staff-Level Takeaway
Design concurrent embedded APIs using SPSC lock-free queues with acquire-release ordering. This provides wait-free, deterministic $O(1)$ communication between interrupts and threads without disabling global interrupts or risking priority inversion.

## Related Concepts
- `02_Atomic_load_store`
- `06_acquire_release`
- `11_Lock_free_queries`
- `../21_C_Headers_APIs_TU/12_Embedded_module_boundaries`
