# 02: Storage Duration

## Definition
Storage duration in ISO C defines the temporal lifespan of the storage associated with an identifier. C recognizes four distinct storage durations: static, thread, automatic, and allocated.

## Scope and Boundaries
- **Covers:** Static, thread, automatic, and allocated storage durations, initialization timing, and linkage.
- **Does not cover:** Object lifetime boundaries ([[01_Object_lifetime]]) or dynamic memory APIs ([[../25_C_Dynamic_Memory/01_malloc]]).

## Why Does It Exist
Different program variables require different lifecycle management models:
- **Persistence:** Global and configuration settings require data to persist throughout the entire program run (Static).
- **Isolation:** Multi-threaded contexts require per-thread private states (Thread).
- **Efficiency:** Temporary function variables require automatic allocation and instant cleanup upon scope exit (Automatic).
- **Flexibility:** Large or dynamically sized structures require runtime heap allocation (Allocated).

## Mechanism and Language Rules
1. **Static Storage Duration:**
   - Objects declared with `static` keyword or at file scope.
   - Lifetime spans the entire execution of the program.
   - Initialized once prior to `main()`. Zero-initialized by default.
2. **Thread Storage Duration:**
   - Objects declared with `_Thread_local` or `thread_local`.
   - Lifetime spans the entire execution of the thread.
3. **Automatic Storage Duration:**
   - Ordinary local variables inside block scopes without `static`.
   - Lifetime spans the block execution. Created upon entry, destroyed upon exit.
4. **Allocated Storage Duration:**
   - Created via `malloc`, `calloc`, or `realloc`.
   - Lifetime spans from allocation until explicit `free()`.

## Examples
/* Keep examples minimal */
#include <stdio.h>

static int global_static_counter = 0; /* Static storage */

void process_data(void) 
{
    int auto_counter = 0; /* Automatic storage */
    static int persistent_local = 0; /* Static storage with block scope */
    
    auto_counter++;
    persistent_local++;
    global_static_counter++;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Using automatic variables without explicit initialization yields indeterminate values, leading to UB if read.
- **Uninitialized Static:** Uninitialized static and thread-duration objects are guaranteed to be initialized to zero or null pointer.

## Edge Cases and Failure Modes
- **Static Reentrancy Hazards:** Using `static` variables inside functions makes those functions non-reentrant and unsafe for multi-threaded invocation unless protected by mutexes.
- **Stack Overflow:** Excessive automatic storage allocation (e.g., large local arrays) causes stack overflow.

## Embedded Implications
- **RAM Footprint:** Static and global variables consume fixed SRAM space (`.data` and `.bss` sections), accounting for a major portion of embedded memory budgets.
- **ROM Constants:** `const` file-scope variables reside in flash memory, preserving RAM.

## Firmware Review Angle
- **Audit Static Usage:** Flag mutable static variables inside functions as thread-safety risks.
- **Examine Stack Sizing:** Verify that automatic allocation sizes are bounded and safe against stack collisions.

## Compiler, ABI, and Toolchain Implications
- **Linker Sections:** Static objects map to `.data` (initialized) and `.bss` (uninitialized). Automatic objects map to the stack frame pointer (`SP`).

## Performance, Memory, Timing, and Power
- **Access Speed:** Static variables use absolute or relative addressing; automatic variables use stack pointer offsets. Both are extremely fast.

## Verification / Debugging
- **Map File Analysis:** Inspect linker `.map` files to audit static storage distribution across RAM sections.

## Safety, Security, and Reliability
- **MISRA C Compliance:** Restrictions on dynamic memory often force reliance on static storage duration for predictable, deterministic real-time embedded systems.

## Trade-offs and Alternatives
- **Static vs. Allocated:** Static storage guarantees zero fragmentation and instant availability at the cost of permanent RAM retention.

## Staff-Level Takeaway
Choosing the correct storage duration is an architectural decision. Default to automatic storage for localized transient data, static storage for fixed configuration state, and allocated storage strictly for runtime-sized data structures under rigorous ownership protocols.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Object_lifetime]]
- [[../25_C_Dynamic_Memory/01_malloc]]
