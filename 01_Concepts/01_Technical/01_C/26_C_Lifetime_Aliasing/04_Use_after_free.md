# 04: Use After Free

## Definition
A use-after-free (UAF) vulnerability occurs when a program continues to use a pointer after the dynamic memory allocation it references has been deallocated via `free()`. UAF is one of the most dangerous memory corruption flaws in C.

## Scope and Boundaries
- **Covers:** Heap deallocation, dangling heap pointers, double frees, and security exploitation vectors.
- **Does not cover:** Stack-based dangling pointers ([[03_Dangling_pointers]]) or memory leaks.

## Why Does It Exist
Dynamic memory management in C requires manual synchronization between allocation and deallocation. When `free(ptr)` is called, the memory allocator reclaims the block, but the variable `ptr` still holds the raw memory address, leading to UAF if accessed.

## Mechanism and Language Rules
- **Heap Reclamation:** `free(ptr)` ends the lifetime of the allocated object.
- **Stale Reference:** `ptr` remains non-null (unless explicitly cleared), pointing to memory that may now be allocated to a completely different data structure.
- **Undefined Behavior:** Any read, write, or pointer arithmetic on a freed pointer is undefined behavior.

## Examples
```c
#include <stdlib.h>
#include <string.h>

int main(void) 
{
    char *buf = malloc(64);
    if (!buf) return 1;

    strcpy(buf, "Important Data");
    free(buf); /* buf lifetime ends here */

    /* Undefined Behavior: Use-after-free */
    /* buf[0] = 'X'; */

    /* Safe practice: nullify pointer immediately */
    buf = NULL;
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Dereferencing a pointer after `free()`. If the allocator has reassigned the memory block, writing to it corrupts unrelated structures, causing subtle, catastrophic bugs.

## Edge Cases and Failure Modes
- **Double Free:** Calling `free()` twice on the same pointer without intervening allocation corrupts heap allocator metadata, often leading to immediate exploitation or crashes.
- **Heap Exploitation:** Attackers allocate crafted payloads into recycled heap chunks to hijack function pointers stored in adjacent structures.

## Embedded Implications
- **RTOS Heap Corruption:** In real-time operating systems using custom heap managers, UAF corrupts memory control blocks, crashing kernel tasks unpredictably.

## Firmware Review Angle
- **Nullify After Free:** Enforce macro wrappers or coding rules (e.g., `SAFE_FREE(ptr)` which calls `free(ptr)` and sets `ptr = NULL`).
- **Audit Ownership:** Ensure clear single-owner contracts for every heap allocation.

## Compiler, IBIs, and Toolchain Implications
- **Sanitizer Instrumentation:** AddressSanitizer (ASan) replaces standard allocator functions with instrumented routines that poison freed memory blocks.

## Performance, Memory, Timing, and Power
- **Debugging Cost:** ASan introduces runtime memory and CPU overhead, making it invaluable during testing but disabled in production firmware builds.

## Verification / Debugging
- **Valgrind Memcheck:** Detects use-after-free errors and invalid free calls in hosted environments.
- **ASan:** Flags exact line numbers where use-after-free occurs.

## Safety, Security, and Reliability
- **Remote Code Execution (RCE):** UAF is a primary vector for high-severity CVEs in systems software, allowing attackers to overwrite sensitive application logic.

## Trade-offs and Alternatives
- **Smart Pointers (C++ / Custom C Wrappers):** Adopting reference counting or arena allocators avoids individual `free()` calls, eliminating UAF risks.

## Staff-Level Takeaway
Never leave a pointer dangling after calling `free()`. Adopt defensive nullification (`ptr = NULL;`) as an absolute dogma. Better yet, design architectures around arena or pool allocators where individual `free()` operations are eliminated entirely.

## Related Concepts
- [[00_Chapter_Index]]
- [[../25_C_Dynamic_Memory/04_free]]
- [[03_Dangling_pointers]]
