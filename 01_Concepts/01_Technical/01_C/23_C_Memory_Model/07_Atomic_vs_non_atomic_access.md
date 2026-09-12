# 07: Atomic vs Non-Atomic Access

## Definition
Atomic and non-atomic accesses represent two fundamentally distinct memory interaction tiers in ISO C11. Non-atomic accesses assume exclusive, single-threaded access and permit aggressive compiler optimization and reordering. Atomic accesses follow strict hardware memory models, enforce bus synchronization, and forbid data races. Mixing atomic and non-atomic accesses to the same memory location without synchronization destroys all concurrency guarantees.

## Scope and Boundaries
Covers: Architectural differences between atomic and non-atomic variables, synchronization boundaries, memory access pairing, and cast hazards.
Does not cover: Operating system file I/O operations.

## Why Does It Exist
If all memory accesses were atomic, programs would suffer severe performance degradation from constant bus locking and barrier instructions. By separating memory into fast non-atomic data and precise atomic synchronization primitives, C provides optimal execution speed while maintaining safety.

## Comparison Matrix
| Characteristic | Non-Atomic Access (`int`) | Atomic Access (`_Atomic int`) |
| :--- | :--- | :--- |
| **Data Race Consequence** | Undefined Behavior | Well-defined, race-free |
| **Compiler Optimization** | Aggressive (CSE, hoisting, vectorization) | Restricted by memory order semantics |
| **Hardware Bus Execution**| May tear across bus boundaries | Guaranteed indivisible transaction |
| **Register Caching** | Cached indefinitely across loops | Loaded/stored according to memory order |
| **Alignment Constraints**| Standard natural alignment | Stricter alignment often enforced |

## Examples
```c
#include <stdatomic.h>
#include <stdint.h>
#include <assert.h>

/* THE MIXED-ACCESS HAZARD */
static int g_shared_variable = 0;

void thread_writer(void) {
    /* ILLEGAL: Casting non-atomic variable to atomic pointer */
    atomic_int *atomic_alias = (atomic_int *)&g_shared_variable;
    atomic_store_explicit(atomic_alias, 42, memory_order_relaxed); /* UNDEFINED BEHAVIOR! */
}

void thread_reader(void) {
    /* Normal non-atomic read */
    int val = g_shared_variable; /* DATA RACE with thread_writer! */
    (void)val;
}

/* CORRECT ARCHITECTURAL SEPARATION */
typedef struct {
    uint8_t     raw_data[128];     /* Non-atomic payload */
    atomic_bool is_payload_valid;  /* Atomic synchronization guard */
} SafeChannel_t;
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Casting a non-atomic object pointer to an atomic object pointer (`(atomic_int *)&x`) and dereferencing it invokes Undefined Behavior (§7.17.7). Atomic types may have different alignments and representations.

## Edge Cases and Failure Modes
- **Aliasing Non-Atomic Data:** If an atomic pointer points to a non-atomic buffer, modifying the buffer concurrently while another thread reads it via the pointer without an acquire-release barrier causes a data race.

## Embedded Implications
- **DMA Buffer Management:** DMA memory buffers must remain completely non-atomic for high-throughput hardware transfer, but the completion flag signaling the application must be `_Atomic`.

## Firmware Review Angle
- Reject any code that attempts to cast between non-atomic and atomic types.
- Ensure non-atomic payloads are protected by clear atomic release/acquire barriers.

## Compiler, ABI, and Toolchain Implications
- Compilers may place atomic objects in distinct memory sections or assign them larger alignments to avoid crossing hardware bus cache line boundaries.

## Performance, Memory, Timing, and Power
- Non-atomic accesses run at full silicon wire speed; atomic accesses incur synchronization overhead only where explicitly requested.

## Verification / Debugging
- Static analysis catches illegal pointer casts between atomic and non-atomic types.

## Safety, Security, and Reliability
- Maintaining a clean boundary between data payloads (non-atomic) and synchronization tokens (atomic) is a mandatory architectural principle for safe real-time code.

## Trade-offs and Alternatives
- **Everything Atomic vs Guarded Payloads:** Making entire structs atomic wastes memory and slows execution. Keep data buffers non-atomic and guard them with scalar atomic tokens.

## Staff-Level Takeaway
Never cast non-atomic pointers to atomic types. Keep data payloads non-atomic for maximum performance, and synchronize access to them using dedicated, scalar atomic variables governed by acquire-release semantics.

## Related Concepts
- `01_Threads_and_shared_objects`
- `02_Data_races`
- `08_Tearing_considerations`
