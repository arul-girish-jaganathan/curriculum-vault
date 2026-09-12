# 01: Threads and Shared Objects

## Definition
In ISO C11 §3.14, a "memory location" is formally defined as either an object of scalar type or a maximal sequence of adjacent bitfields with non-zero width. Threads of execution access shared objects by performing loads and stores to these specific memory locations. Understanding the exact boundary of a memory location is essential for preventing silent concurrency corruption.

## Scope and Boundaries
Covers: ISO C memory location definition, scalar object boundaries, adjacent bitfield hazards, and multi-threaded shared state.
Does not cover: OS thread creation APIs (`thrd_create` or `pthread_create`).

## Why Does It Exist
Processors execute memory transactions in chunks (bytes, words, cache lines). If two threads modify separate fields in the same struct, whether those modifications collide depends entirely on whether the compiler and architecture treat them as distinct memory locations.

## Mechanism and Language Rules
1. **Scalar Object = Distinct Location:** Two independent scalar variables (e.g., two `int` variables or an `int` and a pointer) are distinct memory locations, even if adjacent in a struct.
2. **Adjacent Bitfields = Single Location:** Two or more consecutive bitfields within the same structure form a SINGLE memory location. They cannot be modified concurrently by different threads without synchronization.
3. **Zero-Width Bitfield Boundary:** A zero-width bitfield (`unsigned int : 0;`) explicitly forces the termination of the current memory location, establishing a new memory location for subsequent bitfields.

## Examples
```c
#include <stdint.h>
#include <stdbool.h>

struct SystemState {
    uint32_t sensor_reading; /* Memory Location 1 */
    uint32_t battery_mv;      /* Memory Location 2 */

    /* CONCURRENCY TRAP: Adjacent bitfields form a SINGLE memory location! */
    unsigned int task_ready  : 1; /* Location 3 (shared) */
    unsigned int isr_active  : 1; /* Location 3 (shared) */

    unsigned int : 0; /* Forces new memory location */
    unsigned int isolated_flag : 1; /* Memory Location 4 */
};

/* Safe concurrent access: distinct memory locations */
void thread_update_sensor(struct SystemState *s, uint32_t val) {
    s->sensor_reading = val; /* Completely safe: Location 1 */
}

void thread_update_battery(struct SystemState *s, uint32_t mv) {
    s->battery_mv = mv;      /* Completely safe: Location 2 */
}

/* DATA RACE: Modifying adjacent bitfields concurrently without locks */
void thread_a(struct SystemState *s) {
    s->task_ready = 1; /* Modifies Location 3 */
}

void isr_handler(struct SystemState *s) {
    s->isr_active = 1; /* CONCURRENT RACE on Location 3! Permanent data loss! */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Concurrently modifying adjacent bitfields without synchronization is a Data Race under ISO C11 §5.1.2.4, provoking Undefined Behavior.

## Edge Cases and Failure Modes
- **Phantom Overwrite:** The CPU loads the 32-bit word containing `task_ready` and `isr_active`, modifies `task_ready`, and writes back the word. If `isr_handler` fires in between and writes `isr_active`, the thread's write-back overwrites and erases the ISR's change.

## Embedded Implications
- **Hardware Status Structs:** Microcontroller drivers that map status flags to adjacent bitfields suffer intermittent, un-reproducible race conditions when updated from both thread and ISR contexts.

## Firmware Review Angle
- Audit all structures accessed by multiple threads or ISRs: verify that no adjacent bitfields are mutated across different execution contexts.
- Replace concurrent bitfields with separate `uint8_t` or atomic scalar types.

## Compiler, ABI, and Toolchain Implications
- Compilers generate word-sized read-modify-write instructions (`LDR`/`ORR`/`STR`) for bitfields, making sub-word isolation impossible at the hardware level.

## Performance, Memory, Timing, and Power
- Separating bitfields into individual bytes or words costs a few bytes of RAM, but completely eliminates race conditions and locking latency.

## Verification / Debugging
- ThreadSanitizer flags concurrent bitfield mutations as data races during host testing.

## Safety, Security, and Reliability
- Complies with MISRA C:2012 Rule 1.3 (no undefined behavior) and prevents race condition vulnerabilities (CWE-362).

## Trade-offs and Alternatives
- **Bitfields vs Independent Scalars:** Bitfields save RAM in single-threaded code; independent scalars guarantee thread safety in concurrent systems.

## Staff-Level Takeaway
A scalar object is an independent memory location, but adjacent bitfields share a single memory location. Never allow multiple threads or interrupt routines to mutate adjacent bitfields in the same struct without synchronization.

## Related Concepts
- `02_Data_races`
- `08_Tearing_considerations`
- `../17_C_Bit_Fields/10_Atomicity_limitations`
