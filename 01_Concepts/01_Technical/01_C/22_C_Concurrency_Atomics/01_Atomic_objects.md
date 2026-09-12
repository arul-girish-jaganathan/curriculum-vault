# 01: Atomic Objects

## Definition
An atomic object is an object whose access guarantees indivisible read and write operations, preventing data races as defined by ISO C11 §7.17. Declared using the `_Atomic` type qualifier or standard typedefs (`atomic_int`, `atomic_uint32_t`), any read or write to an atomic object is free of data races even when accessed concurrently by multiple threads or interrupt contexts without locks.

## Scope and Boundaries
Covers: `_Atomic` type specifier/qualifier, `<stdatomic.h>` typedefs, alignment requirements, and object representation.
Does not cover: Atomic memory ordering flags (see `05_memory_order_relaxed` through `08_seq_cst`).

## Why Does It Exist
Prior to C11, standard C had no formal multi-threading memory model. Developers relied on `volatile`, compiler barriers, or inline assembly (`LDREX`/`STREX`). `_Atomic` standardizes atomic types at the language level, enabling portable, compiler-optimized, lock-free concurrent programming.

## Mechanism and Language Rules
1. **Declaration Syntax:**
   - As a type qualifier: `_Atomic int counter;` or `_Atomic(int) counter;`
   - Using standard typedefs: `atomic_int counter;`
2. **Alignment Guarantee:** Atomic objects often have stricter alignment requirements than non-atomic equivalents to ensure the CPU can access them with a single bus transaction.
3. **No Struct Bitfield Atomics:** Bitfields cannot be atomic: `_Atomic unsigned int flag : 1;` is a constraint violation.
4. **Initialization:** Must be initialized using `atomic_init(&obj, val)` or constant initialization `ATOMIC_VAR_INIT(val)` before concurrent access.

## Examples
```c
#include <stdatomic.h>
#include <stdint.h>
#include <stdbool.h>
#include <assert.h>

/* Standard atomic scalar definitions */
static atomic_uint_fast32_t g_event_counter;
static atomic_bool          g_system_ready;

static void init_system(void) {
    /* Proper initialization prior to multi-threaded execution */
    atomic_init(&g_event_counter, 0U);
    atomic_init(&g_system_ready, false);
}

static void publish_event(void) {
    /* Atomic operators work directly or via explicit functions */
    g_event_counter++; /* Implicit atomic read-modify-write (seq_cst) */
    atomic_store_explicit(&g_system_ready, true, memory_order_release);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Accessing an atomic object before it has been initialized by `atomic_init()` invokes Undefined Behavior.
- If an atomic type is not lock-free on a target architecture, the compiler generates calls to internal library locks (e.g., `libatomic`), which may deadlock if called from an ISR.

## Edge Cases and Failure Modes
- **Compound Types in `_Atomic`:** Declaring `_Atomic struct LargeData my_data;` where `sizeof(LargeData) > 8` forces the compiler to protect the struct with a hidden software mutex, destroying real-time predictability.
- **Copying Atomic Objects:** Atomic objects cannot be copied with raw `memcpy` or direct struct assignment; doing so bypasses the atomic memory bus protocol.

## Embedded Implications
- **Cortex-M0 vs Cortex-M3/M4:** ARM Cortex-M0 lacks load-exclusive/store-exclusive instructions (`LDREX`/`STREX`), meaning 32-bit atomics require disabling global interrupts, whereas Cortex-M3/M4/M7 execute lock-free hardware atomics.

## Firmware Review Angle
- Confirm that `atomic_init()` is called during single-threaded startup before any threads or interrupts are enabled.
- Verify that large structs are NOT declared `_Atomic`; restrict atomic types to scalar words matching the processor register width.

## Compiler, ABI, and Toolchain Implications
- In Clang and GCC, `_Atomic(T)` may have a larger `sizeof` and stricter `alignof` than `T` to accommodate architecture-specific synchronization requirements.

## Performance, Memory, Timing, and Power
- Naturally aligned 32-bit atomic operations on 32-bit CPUs incur zero extra cycle penalties compared to standard loads and stores.

## Verification / Debugging
- Static analysis: Enable `-Watomic-alignment` to detect when atomic types have alignment mismatches.
- ThreadSanitizer (`-fsanitize=thread`) validates atomic usage in simulated environments.

## Safety, Security, and Reliability
- MISRA C:2012 Amendment 4 provides strict guidelines for `<stdatomic.h>` adoption in safety-critical code.

## Trade-offs and Alternatives
- **Atomics vs OS Mutex:** Atomic objects provide microsecond-level synchronization with zero context-switching overhead, but are limited to small scalar types.

## Staff-Level Takeaway
Declare shared concurrent scalars using standard C11 `_Atomic` types rather than non-standard compiler hacks. Initialize them cleanly with `atomic_init()`, and verify that the target CPU supports hardware lock-freedom for the chosen word size.

## Related Concepts
- `02_Atomic_load_store`
- `11_Lock_free_queries`
- `../23_C_Memory_Model/01_Threads_and_shared_objects`
