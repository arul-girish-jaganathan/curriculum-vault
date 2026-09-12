# 12: Embedded Allocation Policy

## Definition
Embedded Allocation Policy is the strict architectural governance defining how memory is acquired, managed, and released in resource-constrained embedded systems, bare-metal firmware, and safety-critical microcontrollers.

## Scope and Boundaries
- **Covers:** Prohibition of dynamic heap allocation (`malloc`/`free`), static memory pre-allocation, stack-size budgeting, link-time memory partitioning, and deterministic safety guidelines.
- **Does not cover:** Hosted OS heap management or dynamic desktop memory models.

## Why Does It Exist
Embedded systems (automotive, aerospace, medical devices) require absolute reliability and determinism:
- **Elimination of Failure Modes:** General heap allocation (`malloc`) can fail due to fragmentation or exhaustion, leading to unhandled null-pointer crashes or unpredictable behavior.
- **Hard Real-Time Determinism:** `malloc` and `free` have non-deterministic execution times depending on heap free-list traversal, violating hard real-time deadlines.
- **Safety Standard Compliance:** Coding standards (MISRA C, JSF AV, NASA C) heavily restrict or outright ban dynamic heap allocation in safety-critical systems.

## Mechanism and Language Rules
1. **Total Prohibition of Runtime Heaps:** Ban `malloc`, `calloc`, `realloc`, and `free` entirely from production firmware.
2. **Static Pre-Allocation:** All tasks, buffers, message queues, and communication channels must be statically allocated at compile time as global or static variables.
3. **Linker Script Partitioning:** Explicitly define memory regions (`.text`, `.data`, `.bss`, stack, and static pools) in the linker script (`linker.ld`) to guarantee memory boundaries and prevent stack-heap collisions.
4. **Static Analysis & Stack High-Water Marking:** Enforce strict stack size limits and analyze call graphs statically to prove stack exhaustion is mathematically impossible.

## Examples
```c
/* ==================== embedded_policy.c ==================== */
#include <stdint.h>
#include <stdbool.h>

#if defined(__STDC_HOSTED__) && __STDC_HOSTED__ == 1
    #error "This firmware adheres to strict embedded freestanding allocation policy!"
#endif

/* STATIC PRE-ALLOCATION: Zero runtime malloc/free */
#define MAX_SENSORS 8
#define SENSOR_QUEUE_LEN 32

typedef struct {
    uint32_t sensor_id;
    float reading;
    uint32_t timestamp;
} sensor_msg_t;

static sensor_msg_t g_sensor_pool[SENSOR_QUEUE_LEN];
static size_t g_pool_head = 0;
static size_t g_pool_tail = 0;
static bool g_pool_full = false;

bool static_queue_push(uint32_t id, float reading, uint32_t timestamp) 
{
    if (g_pool_full) {
        return false; /* Handle capacity limits deterministically without dynamic growth */
    }

    g_sensor_pool[g_pool_tail].sensor_id = id;
    g_sensor_pool[g_pool_tail].reading = reading;
    g_sensor_pool[g_pool_tail].timestamp = timestamp;

    g_pool_tail = (g_pool_tail + 1) % SENSOR_QUEUE_LEN;
    if (g_pool_tail == g_pool_head) {
        g_pool_full = true;
    }
    return true;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Linker Script Violations:** Placing initialized data in uninitialized sections or overflowing stack boundaries into static `.bss` space triggers hard faults.

## Edge Cases and Failure Modes
- **Fixed-Capacity Limits:** Static pre-allocation means maximum bounds must be chosen at compile time. If peak runtime load exceeds static buffer capacity, the system must handle overflow gracefully rather than dynamically expanding.

## Embedded Implications
- **MCU RAM Budgets:** Forces engineers to calculate exact RAM requirements down to the byte during system design, eliminating hidden memory waste.
- **Predictable Power & Performance:** Deterministic memory access ensures consistent CPU timing and predictable low-power sleep state transitions.

## Firmware Review Angle
- **Ban `malloc` / `free`:** Configure static analyzers and compiler flags (`-Werror=implicit-function-declaration` or custom AST rules) to reject any inclusion or call to standard heap allocators.
- **Audit Static Buffer Sizing:** Verify that statically allocated buffers provide sufficient margin for worst-case operational scenarios.

## Compiler, ABI, and Toolchain Implications
- **Linker Map Analysis:** Review `.map` files generated during compilation to verify exact RAM and Flash utilization percentages across all sections.

## Performance, Memory, Timing, and Power
- **Zero Allocation Overhead:** Static allocation incurs zero runtime CPU cycles for memory management, achieving maximum execution speed and minimum power consumption.

## Verification / Debugging
- **Stack High-Water Marks:** Fill stack memory regions with a known magic pattern (e.g., `0xDEADBEEF`) at startup and inspect remaining untouched patterns post-execution to measure precise stack consumption.

## Safety, Security, and Reliability
- **Certification Readiness:** Static allocation policies are mandatory for achieving certification under ISO 26262 (ASIL-D), IEC 61508, and DO-178C (DAL-A).

## Trade-offs and Alternatives
- **Static Allocation vs. Dynamic Heaps:** Static allocation is 100% deterministic, safe, and robust but requires upfront sizing and prevents flexible memory sharing across disparate modules.

## Staff-Level Takeaway
In mission-critical embedded systems, the heap is your enemy. Adopt a zero-malloc allocation policy: pre-allocate all resources statically at compile time, use fixed-size pools or arenas for structured concurrency, and prove memory safety mathematically. Determinism is the hallmark of professional firmware engineering.

## Related Concepts
- [[00_Chapter_Index]]
- [[07_Allocation_failure]]
- [[09_Memory_fragmentation]]
- [[11_Pools_and_arenas]]
- [[../24_C_Threads_C11/11_Freestanding_limitations]]
