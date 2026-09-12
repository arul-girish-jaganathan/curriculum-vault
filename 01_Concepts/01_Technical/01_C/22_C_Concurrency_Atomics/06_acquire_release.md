# 06: Acquire-Release Semantics

## Definition
Acquire-release synchronization is a directional memory ordering model in ISO C11 that establishes a formal "synchronizes-with" relationship between threads. A store operation executed with `memory_order_release` synchronizes with a load operation executed with `memory_order_acquire` that reads the stored value, guaranteeing that all memory writes made prior to the release store become visible to the acquiring thread after the acquire load.

## Scope and Boundaries
Covers: `memory_order_acquire`, `memory_order_release`, one-way memory barriers, message passing, and producer-consumer synchronization.
Does not cover: Full sequential consistency (see `08_seq_cst`).

## Why Does It Exist
Lock-free data structures (e.g., ring buffers) require publishing data: a producer writes data to a buffer and then sets a flag; a consumer checks the flag and then reads the data. Without acquire-release semantics, CPUs and compilers reorder reads and writes, causing the consumer to read uninitialized buffer memory before the producer finished writing it.

## Mechanism and Language Rules
1. **Release Store (`memory_order_release`):** Acts as a one-way barrier preventing preceding memory reads and writes from being reordered *after* the atomic store.
2. **Acquire Load (`memory_order_acquire`):** Acts as a one-way barrier preventing subsequent memory reads and writes from being reordered *before* the atomic load.
3. **Synchronizes-With Contract:**
   $$\text{Thread A (Release Store)} \xrightarrow{\text{reads value}} \text{Thread B (Acquire Load)}$$
   All operations sequenced before the release in Thread A "happen-before" operations sequenced after the acquire in Thread B.

## Examples
```c
#include <stdatomic.h>
#include <stdint.h>
#include <stdbool.h>
#include <assert.h>

/* Lock-Free Message Passing / Producer-Consumer */
typedef struct {
    uint8_t payload[64];
} Packet_t;

static Packet_t    g_packet_buffer;
static atomic_bool g_packet_ready = false;

/* Producer (e.g., DMA Completion ISR or High-Priority Task) */
void producer_send(const uint8_t *data, size_t len) {
    /* 1. Fill non-atomic payload */
    for (size_t i = 0; i < len; ++i) {
        g_packet_buffer.payload[i] = data[i];
    }

    /* 2. Release store: Guarantees payload writes complete BEFORE ready flag is set */
    atomic_store_explicit(&g_packet_ready, true, memory_order_release);
}

/* Consumer (e.g., Background Worker Task) */
bool consumer_receive(uint8_t *out_data) {
    /* 1. Acquire load: Pairs with release store */
    if (atomic_load_explicit(&g_packet_ready, memory_order_acquire)) {
        /* 2. Guaranteed to read fully populated payload safely! */
        for (size_t i = 0; i < 64; ++i) {
            out_data[i] = g_packet_buffer.payload[i];
        }
        
        atomic_store_explicit(&g_packet_ready, false, memory_order_relaxed);
        return true;
    }
    return false;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Applying `memory_order_acquire` to an atomic store or `memory_order_release` to an atomic load is a language violation and triggers compile-time errors or Undefined Behavior.

## Edge Cases and Failure Modes
- **Failed CAS with Release:** If `atomic_compare_exchange_weak` fails, the release ordering does not synchronize; the failure order must handle synchronization or use `relaxed`.

## Embedded Implications
- **Hardware Barrier Emission:** On ARMv7-M (Cortex-M3/M4/M7), an acquire-release pair emits a Data Memory Barrier (`DMB`) instruction on the release store, ensuring hardware bus write buffers drain before setting the flag.

## Firmware Review Angle
- Check that every `release` store has an explicit matching `acquire` load in the consuming thread.
- Verify that non-atomic data is fully written before the release store occurs.

## Compiler, ABI, and Toolchain Implications
- Compilers forbid hoisting memory operations below a release store or sinking memory operations above an acquire load during optimization passes.

## Performance, Memory, Timing, and Power
- Significantly faster than `memory_order_seq_cst` because it enforces only one-way ordering constraints, avoiding full bidirectional pipeline flushes.

## Verification / Debugging
- ThreadSanitizer mathematically validates acquire-release happens-before relationships.

## Safety, Security, and Reliability
- Forms the architectural foundation for deterministic, lock-free inter-thread communication in high-reliability RTOS applications.

## Trade-offs and Alternatives
- **Acquire-Release vs Full Mutex:** Acquire-release provides wait-free, zero-lock synchronization for single-producer single-consumer (SPSC) patterns with zero scheduling latency.

## Staff-Level Takeaway
Acquire-release is the gold standard for high-performance concurrent C. Use release stores to publish shared data and acquire loads to consume it. This enforces strict synchronization with minimal memory barrier instructions on modern weakly ordered processors.

## Related Concepts
- `05_memory_order_relaxed`
- `07_acq_rel`
- `08_seq_cst`
- `../23_C_Memory_Model/05_Synchronizes_with`
