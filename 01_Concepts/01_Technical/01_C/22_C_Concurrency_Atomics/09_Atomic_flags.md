# 09: Atomic Flags

## Definition
An atomic flag (`atomic_flag`) is the minimal, guaranteed lock-free boolean atomic primitive in ISO C11. It supports only two states (set and clear) and exactly two fundamental operations: `atomic_flag_test_and_set()` and `atomic_flag_clear()`. Unlike standard `atomic_bool`, `atomic_flag` is guaranteed by the C standard to be completely lock-free on every conforming architecture without exception.

## Scope and Boundaries
Covers: `atomic_flag`, `ATOMIC_FLAG_INIT`, `atomic_flag_test_and_set`, `atomic_flag_clear`, and low-level spinlock implementations.
Does not cover: General multi-valued atomic scalars (see `01_Atomic_objects`).

## Why Does It Exist
On certain simple microcontrollers or DSP architectures, the CPU lacks hardware support for multi-byte atomic operations or general compare-and-swap, forcing compilers to emulate `atomic_int` with hidden software locks. `atomic_flag` was designed as the universal hardware-guaranteed baseline primitive upon which all other lock-free synchronization can be constructed.

## Mechanism and Language Rules
1. **Guaranteed Lock-Free:** `atomic_flag` is the ONLY type guaranteed by ISO C11 §7.17.8 to be lock-free on all platforms.
2. **Mandatory Initialization:** Must be initialized using `ATOMIC_FLAG_INIT`:
   `atomic_flag lock = ATOMIC_FLAG_INIT;`
3. **Atomic Operations:**
   - `atomic_flag_test_and_set(flag)`: Atomically sets the flag to true and returns the *previous* boolean state.
   - `atomic_flag_clear(flag)`: Atomically resets the flag to false.

## Examples
```c
#include <stdatomic.h>
#include <stdbool.h>

/* Guaranteed Lock-Free Spinlock for Multi-Core / RTOS */
typedef struct {
    atomic_flag flag;
} Spinlock_t;

#define SPINLOCK_INIT { .flag = ATOMIC_FLAG_INIT }

static void spinlock_lock(Spinlock_t *lock) {
    /* Spin until test_and_set returns false (meaning we acquired it) */
    while (atomic_flag_test_and_set_explicit(&lock->flag, memory_order_acquire)) {
        /* Architecture-specific pause/yield (e.g., __WFE() or __NOP() on ARM) */
        #if defined(__ARM_ARCH)
        __asm volatile("yield" ::: "memory");
        #endif
    }
}

static void spinlock_unlock(Spinlock_t *lock) {
    /* Clear flag with release ordering: publishes protected critical section */
    atomic_flag_clear_explicit(&lock->flag, memory_order_release);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Reading an `atomic_flag` without test-and-set or initializing it dynamically with anything other than `ATOMIC_FLAG_INIT` produces implementation-defined or undefined behavior.

## Edge Cases and Failure Modes
- **Spinlock Starvation on Single-Core MCU:** Using an `atomic_flag` spinlock on a single-core microcontroller where an interrupt or lower-priority thread holds the lock leads to permanent CPU deadlock. Spinlocks are valid ONLY across multiple CPU cores or between hardware threads.

## Embedded Implications
- **Hardware Test-and-Set:** Microcontroller architectures typically map `atomic_flag_test_and_set` to native single-cycle instructions, such as `SWP` or bit-band operations.

## Firmware Review Angle
- Confirm that `atomic_flag` is initialized strictly with `= ATOMIC_FLAG_INIT`.
- Verify that spinlocks using `atomic_flag` are never used on single-core systems where interrupts could cause deadlock.

## Compiler, ABI, and Toolchain Implications
- Generates pure inline assembly instructions with zero external library helper calls.

## Performance, Memory, Timing, and Power
- Smallest possible atomic memory footprint (typically 1 byte, padded to bus alignment).
- Excessive spinning burns power; integrate low-power wait instructions (`yield` or `WFE` on ARM) into the spin loop.

## Verification / Debugging
- Check lock contention metrics using hardware debug counters.

## Safety, Security, and Reliability
- Eliminates any risk of hidden compiler mutexes in safety-critical code (DO-178C, ISO 26262).

## Trade-offs and Alternatives
- **`atomic_flag` vs `atomic_bool`:** `atomic_bool` allows arbitrary reads (`atomic_load`), whereas `atomic_flag` forces you to test-and-set. Use `atomic_flag` when absolute hardware-level lock-freedom must be guaranteed.

## Staff-Level Takeaway
`atomic_flag` is the bedrock of C concurrency. It is the only type guaranteed by the C standard to be lock-free on every architecture. Use it to build low-level multi-core spinlocks and synchronization tokens, paired with `yield` instructions to conserve energy.

## Related Concepts
- `01_Atomic_objects`
- `04_compare_exchange`
- `11_Lock_free_queries`
