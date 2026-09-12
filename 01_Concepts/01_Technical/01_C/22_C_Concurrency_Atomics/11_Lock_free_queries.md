# 11: Lock-Free Queries

## Definition
Lock-free queries are compile-time macros and runtime introspection functions provided by ISO C11 `<stdatomic.h>` to determine whether an atomic type or object is implemented using native, lock-free hardware instructions (such as LL/SC or CAS) or emulated by the compiler using hidden software locks.

## Scope and Boundaries
Covers: `atomic_is_lock_free()`, `ATOMIC_*_LOCK_FREE` macros, lock-freedom vs. wait-freedom, and hidden software mutex traps.
Does not cover: Operating system thread scheduling.

## Why Does It Exist
The C11 standard allows compilers to conform even if the underlying CPU hardware does not support atomic instructions for a given type, by silently generating internal mutex locks. In embedded systems and real-time firmware, calling an atomic operation that secretly acquires a software mutex can cause priority inversion, deadlocks in Interrupt Service Routines (ISRs), and catastrophic latency spikes.

## Mechanism and Language Rules
1. **Compile-Time Macros:** `<stdatomic.h>` defines macros for standard integer widths:
   - `ATOMIC_BOOL_LOCK_FREE`
   - `ATOMIC_CHAR_LOCK_FREE`
   - `ATOMIC_SHORT_LOCK_FREE`
   - `ATOMIC_INT_LOCK_FREE`
   - `ATOMIC_LONG_LOCK_FREE`
   - `ATOMIC_POINTER_LOCK_FREE`
   Values: `0` = Never lock-free, `1` = Sometimes lock-free (runtime dependent), `2` = Always lock-free.
2. **Runtime Query Function:**
   `bool atomic_is_lock_free(const volatile _Atomic(T)* obj);`
   Returns `true` if operations on the specific object execute without software locks.

## Examples
```c
#include <stdatomic.h>
#include <stdint.h>
#include <stdbool.h>
#include <assert.h>

/* Compile-time architectural assertion */
#if (ATOMIC_INT_LOCK_FREE != 2) || (ATOMIC_POINTER_LOCK_FREE != 2)
    #error "Target CPU does not support hardware lock-free integers/pointers!"
#endif

typedef struct {
    uint32_t a;
    uint32_t b;
    uint32_t c;
} LargeTelemetry_t;

static _Atomic(LargeTelemetry_t) g_large_telemetry;

static void verify_lock_freedom(void) {
    /* Runtime check for custom or large compound types */
    if (!atomic_is_lock_free(&g_large_telemetry)) {
        /*
         * CRITICAL WARNING: Compiler is using a hidden mutex!
         * This object CANNOT be accessed from an ISR or hard real-time loop!
         */
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Accessing an atomic object whose lock-free status is `false` from an Interrupt Service Routine (ISR) invokes Undefined Behavior (deadlock), because the ISR will attempt to acquire a mutex held by the interrupted thread.

## Edge Cases and Failure Modes
- **Hidden Linker Dependency (`libatomic`):** If code uses an atomic type that evaluates to lock-free `0` or `1`, compilation may succeed but linking fails with `undefined reference to __atomic_load_8` unless `-latomic` is passed.
- **Value 1 Ambiguity:** A macro value of `1` means lock-freedom depends on hardware alignment at runtime.

## Embedded Implications
- **ISR Safety Rule:** ONLY atomic types that evaluate to `ATOMIC_*_LOCK_FREE == 2` or return `atomic_is_lock_free() == true` are safe to use inside Interrupt Service Routines.

## Firmware Review Angle
- Enforce static assertions (`_Static_assert(ATOMIC_POINTER_LOCK_FREE == 2, ...);`) in hardware abstraction headers.
- Audit build scripts to ensure `-latomic` is NOT silently hiding software-emulated locks in bare-metal firmware.

## Compiler, ABI, and Toolchain Implications
- When lock-freedom is `2`, compilers emit inline machine instructions (`LDREX`/`STREX`, `CMPXCHG`). When `0`, compilers emit calls to runtime lock tables.

## Performance, Memory, Timing, and Power
- True lock-free atomics execute in single-digit cycles. Software-emulated locks involve function calls, hash table lookups, and OS thread blocking.

## Verification / Debugging
- Check generated assembly disassembly: if function calls to `__atomic_*` appear, the type is NOT lock-free.

## Safety, Security, and Reliability
- Safety standards (ISO 26262, IEC 61508) require deterministic worst-case execution time (WCET), which is violated if atomics secretly acquire software locks.

## Trade-offs and Alternatives
- If a data structure is not lock-free, abandon `_Atomic` on that struct and use an explicit, well-architected OS mutex or double-buffering scheme instead.

## Staff-Level Takeaway
Never assume an atomic type is hardware lock-free. Lock down your architectures with `_Static_assert(ATOMIC_INT_LOCK_FREE == 2)` and never access non-lock-free atomic objects inside Interrupt Service Routines.

## Related Concepts
- `01_Atomic_objects`
- `09_Atomic_flags`
- `12_Atomic_API_design`
