# 04: Modification Order

## Definition
In ISO C11 §5.1.2.4, the modification order of an atomic object is the single, total order of all writes (stores and read-modify-write operations) performed on that specific atomic object across the entire execution of the program. All threads in the system are guaranteed to observe the modifications to that particular object in this exact same sequence.

## Scope and Boundaries
Covers: Per-object coherence, write-write consistency, read-read coherence, and store serialization.
Does not cover: Global ordering across *different* atomic objects (see `08_seq_cst`).

## Why Does It Exist
Even when memory operations are relaxed (`memory_order_relaxed`), the hardware must guarantee that a single variable does not fluctuate backwards in time. Modification order guarantees that once a thread observes a newer value of an atomic variable, it can never subsequently observe an older value of that same variable.

## Mechanism and Language Rules
1. **Four Coherence Axioms:**
   - **Write-Write Coherence:** If write $A$ precedes write $B$ in modification order, no thread can see $B$ and then $A$.
   - **Read-Read Coherence:** If read $R_1$ reads value from write $A$, and read $R_2$ occurs later in the same thread, $R_2$ cannot read a value that preceded $A$ in modification order.
   - **Read-Write Coherence:** A read cannot read a value overwritten by a write that happened-before it.
   - **Write-Read Coherence:** A write cannot overwrite a value after a read that happened-after it.
2. **Per-Object Scope:** Modification order applies to *individual* atomic objects independently.

## Examples
```c
#include <stdatomic.h>
#include <stdint.h>
#include <assert.h>

static atomic_uint_fast32_t g_state_counter;

/* Thread 1: Drives State Forward */
void thread_producer(void) {
    /* Sequence of writes: establishes Modification Order (1 -> 2 -> 3) */
    atomic_store_explicit(&g_state_counter, 1U, memory_order_relaxed);
    atomic_store_explicit(&g_state_counter, 2U, memory_order_relaxed);
    atomic_store_explicit(&g_state_counter, 3U, memory_order_relaxed);
}

/* Thread 2: Consumer */
void thread_consumer(void) {
    uint32_t first = atomic_load_explicit(&g_state_counter, memory_order_relaxed);
    uint32_t second = atomic_load_explicit(&g_state_counter, memory_order_relaxed);

    /* 
     * READ-READ COHERENCE:
     * If first observed 2, second can NEVER observe 1!
     * It can only observe 2 or 3. The variable never travels backwards in time.
     */
    if (first == 2U) {
        assert(second >= 2U);
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Non-atomic variables have NO modification order. Concurrently writing to a non-atomic variable violates coherence and causes Undefined Behavior (Data Race).

## Edge Cases and Failure Modes
- **The Multi-Object Fallacy:** Developers often assume modification order applies across multiple variables: "If variable $X$ advanced to 2, then variable $Y$ must have advanced to 2." Modification order applies ONLY to a single variable in isolation. Cross-variable ordering requires acquire-release or `seq_cst`.

## Embedded Implications
- **Hardware Coherence Controllers:** Even on multi-core microcontrollers with weakly ordered memory (e.g., dual-core ARM Cortex-A or Cortex-M55/M7 with AXI buses), hardware cache-coherency protocols (SCU / ACE) enforce a single modification order for every cache line.

## Firmware Review Angle
- Ensure developers understand that relaxed atomics provide coherence for *one* variable, but cannot be used to deduce the state of *other* variables.

## Compiler, ABI, and Toolchain Implications
- Compilers are strictly forbidden from reordering two stores to the same atomic object, as doing so would violate its modification order.

## Performance, Memory, Timing, and Power
- Enforced at the silicon level by hardware cache coherence protocols without requiring CPU software barrier instructions.

## Verification / Debugging
- Formal memory model tools verify modification order consistency by asserting write-serialization acyclicity.

## Safety, Security, and Reliability
- Ensures basic temporal sanity across multi-threaded state machines.

## Trade-offs and Alternatives
- **Single Object Coherence vs Multi-Object Synchronization:** If multiple state variables must advance in lockstep, group them into a single atomic struct or synchronize them using acquire-release atomics.

## Staff-Level Takeaway
Modification order guarantees that individual atomic objects never travel backwards in time. While relaxed atomics guarantee coherence for a single variable, never extrapolate that ordering to neighboring variables without explicit acquire-release barriers.

## Related Concepts
- `03_Happens_before`
- `05_Synchronizes_with`
- `../22_C_Concurrency_Atomics/05_memory_order_relaxed`
