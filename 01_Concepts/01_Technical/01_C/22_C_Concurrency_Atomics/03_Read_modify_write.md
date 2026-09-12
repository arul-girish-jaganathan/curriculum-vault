# 03: Read-Modify-Write (RMW)

## Definition
An atomic Read-Modify-Write (RMW) operation reads the current value of an atomic object, computes a mutation (addition, subtraction, bitwise operation), and stores the new value back into memory as a single, indivisible transaction. No other thread or interrupt can intervene between the read and the write.

## Scope and Boundaries
Covers: `atomic_fetch_add`, `atomic_fetch_sub`, `atomic_fetch_or`, `atomic_fetch_xor`, `atomic_fetch_and`, and their `_explicit` counterparts.
Does not cover: Compare-and-swap operations (see `04_compare_exchange`).

## Why Does It Exist
Operations like `counter++` or `flags |= BIT` consist of three distinct machine steps: load, mutate, store. If an interrupt or context switch occurs between the load and the store, modifications made by the preempting code are permanently lost. Atomic RMW primitives enforce hardware-level atomicity across the entire operation.

## Mechanism and Language Rules
1. **Return Value Rule:** All `atomic_fetch_*` functions return the value the object had *BEFORE* the operation was performed.
2. **Standard RMW Operations:**
   - `atomic_fetch_add(object, operand)`
   - `atomic_fetch_sub(object, operand)`
   - `atomic_fetch_or(object, operand)`
   - `atomic_fetch_xor(object, operand)`
   - `atomic_fetch_and(object, operand)`
3. **Hardware Backing:** On architectures with load-linked/store-conditional (LL/SC) or exclusive monitors (ARM `LDREX`/`STREX`), the compiler generates a lock-free hardware loop.

## Examples
```c
#include <stdatomic.h>
#include <stdint.h>
#include <assert.h>

static atomic_uint_fast32_t g_active_connections;
static atomic_uint_fast32_t g_status_flags;

void connection_opened(void) {
    /* Atomically increment and get previous count */
    uint32_t prev = atomic_fetch_add_explicit(&g_active_connections, 1U, memory_order_relaxed);
    (void)prev;
}

void connection_closed(void) {
    /* Atomically decrement */
    atomic_fetch_sub_explicit(&g_active_connections, 1U, memory_order_relaxed);
}

void set_ready_flag(uint32_t flag_mask) {
    /* Atomic bitwise OR: preserves all other concurrent flag writes */
    atomic_fetch_or_explicit(&g_status_flags, flag_mask, memory_order_release);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Signed integer overflow on `atomic_fetch_add` or `atomic_fetch_sub` with signed atomic types is well-defined as two's complement modulo arithmetic in C11 (§7.17.7.5), unlike standard C signed overflow.

## Edge Cases and Failure Modes
- **Expecting the New Value:** Developers frequently assume `atomic_fetch_add(&c, 1)` returns the *new* incremented value. It returns the *old* value. The new value is `old + 1`.
- **Contention Latency:** High-frequency atomic RMW operations on a single variable across multiple CPU cores cause cache-line bouncing, degrading system throughput.

## Embedded Implications
- **Interrupt Flag Management:** Using `atomic_fetch_or` to set flags from an ISR eliminates the risk of overwriting flags set concurrently by other ISRs or the main thread without needing critical sections (`__disable_irq()`).

## Firmware Review Angle
- Confirm that callers expecting the updated value calculate it from the return value (`prev + 1`) rather than issuing an immediate second `atomic_load` (which creates a race condition).
- Verify appropriate memory ordering: use `memory_order_relaxed` for independent metrics and statistics counters.

## Compiler, ABI, and Toolchain Implications
- On ARM Cortex-M3/M4/M7, `atomic_fetch_add` compiles to a compact `LDREX`/`ADDS`/`STREX` loop. On x86, it compiles directly to a single `LOCK XADD` instruction.

## Performance, Memory, Timing, and Power
- Single-core MCUs execute LL/SC loops in 3-5 CPU cycles without bus locking overhead.

## Verification / Debugging
- Test under heavy interrupt load to verify no dropped events or counter miscounts occur.

## Safety, Security, and Reliability
- Eliminates lost-update concurrency bugs (CWE-362) in multi-threaded task management.

## Trade-offs and Alternatives
- **Atomic RMW vs Mutex:** Atomic RMW operations are wait-free or lock-free and execute in nanoseconds, whereas mutexes involve OS scheduler overhead and risk priority inversion.

## Staff-Level Takeaway
Use `atomic_fetch_*` primitives for shared counters and bitmask flags. Remember that they return the *previous* value, not the new value. Use `relaxed` ordering for independent counters, and enjoy lock-free interrupt-safe mutation without disabling global interrupts.

## Related Concepts
- `02_Atomic_load_store`
- `04_compare_exchange`
- `05_memory_order_relaxed`
