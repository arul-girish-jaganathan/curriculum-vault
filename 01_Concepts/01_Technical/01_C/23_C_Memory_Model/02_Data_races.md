# 02: Data Races

## Definition
In ISO C11 §5.1.2.4, a data race is formally defined as two or more concurrent memory accesses to the same memory location by different threads, where at least one of the accesses is a modification (write), and the accesses are not coordinated by atomic operations or synchronized by mutual exclusion locks. A program containing a data race exhibits Undefined Behavior.

## Scope and Boundaries
Covers: Formal definition of data races, undefined behavior consequences, compiler assumptions under race-free guarantees, and race conditions vs data races.
Does not cover: High-level race conditions in business logic (e.g., time-of-check to time-of-use).

## Why Does It Exist
Modern optimizing compilers assume that valid C programs are entirely free of data races ("Catch-Fire Semantics"). If a program has a data race, the compiler's mathematical optimization proofs collapse, allowing the optimizer to reorder code, invent phantom reads, or delete entire code blocks.

## Mechanism and Language Rules
1. **The Three Conditions:** A data race occurs if and only if:
   - Two or more threads access the *same* memory location concurrently.
   - At least one access is a *write*.
   - At least one access is *non-atomic* and not ordered by a happens-before relationship.
2. **Undefined Behavior:** A single data race invalidates the entire program's execution under ISO C.

## Examples
```c
#include <stdbool.h>

/* DATA RACE BUG: Non-atomic shared state */
static int  g_telemetry_val = 0;
static bool g_data_ready = false;

/* Worker Thread */
void worker_thread(void) {
    g_telemetry_val = 100; /* Write */
    g_data_ready = true;   /* Write */
}

/* Reader Thread / ISR */
void reader_thread(void) {
    /* 
     * DATA RACE: Concurrent non-atomic read and write!
     * The compiler optimizer may assume g_data_ready never changes
     * and hoist the read outside the loop, resulting in an infinite loop!
     */
    while (!g_data_ready) {
        /* Busy wait */
    }
    
    int val = g_telemetry_val; /* May read uninitialized or torn data */
    (void)val;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Under ISO C11, the consequence of a data race is Undefined Behavior. The program is not merely guaranteed to read stale data; the compiler is permitted to generate entirely unpredictable machine code.

## Edge Cases and Failure Modes
- **Dead-Code Elimination of Polling Loops:** If a variable in a polling loop is not declared `_Atomic` or `volatile`, the compiler proves that the current thread does not mutate it, assumes no other thread mutates it (since races are UB), and optimizes the loop into `while(1);`.
- **Invented Writes:** Under aggressive optimization, compilers may spill registers to non-atomic shared variables, creating "invented writes" that corrupt concurrent data.

## Embedded Implications
- **Interrupts Are Concurrent Threads:** In bare-metal firmware, an Interrupt Service Routine (ISR) is effectively a high-priority concurrent thread. Accessing non-atomic global variables from both an ISR and main thread without atomics or critical sections is a data race.

## Firmware Review Angle
- Search for any global or static variable accessed by both thread code and an ISR: is it declared `_Atomic` or protected by a critical section? If not, flag as a critical defect.

## Compiler, ABI, and Toolchain Implications
- Compilers exploit the absence of data races to perform loop vectorization, common subexpression elimination (CSE), and aggressive register caching.

## Performance, Memory, Timing, and Power
- Data races cause intermittent, irreproducible bugs ("heisenbugs") that consume hundreds of engineering hours to diagnose.

## Verification / Debugging
- Compile with `-fsanitize=thread` (TSan) in simulator builds. TSan mathematically instruments memory accesses and reports the exact source lines of conflicting accesses.

## Safety, Security, and Reliability
- Banned by all safety-critical standards: MISRA C:2012 Amendment 4, ISO 26262 Part 6, and IEC 61508.

## Trade-offs and Alternatives
- **Data Race vs Mutex/Atomics:** Atomics eliminate data races with zero context-switch overhead; mutexes eliminate data races for complex multi-variable state updates.

## Staff-Level Takeaway
A data race is not a minor timing glitch; it is an immediate descent into Undefined Behavior. Modern compilers will aggressively optimize code assuming data races cannot exist, silently breaking your firmware. Synchronize every shared access using C11 atomics or critical sections.

## Related Concepts
- `01_Threads_and_shared_objects`
- `03_Happens_before`
- `../22_C_Concurrency_Atomics/01_Atomic_objects`
