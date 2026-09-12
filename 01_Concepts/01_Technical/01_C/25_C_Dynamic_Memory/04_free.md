# 04: free

## Definition
`free` is the standard library function declared in `<stdlib.h>` that deallocates a memory block previously allocated by `malloc`, `calloc`, or `realloc`. Once freed, the memory is returned to the heap allocator for reuse, and the pointer referencing it becomes a dangling pointer.

## Scope and Boundaries
- **Covers:** `free()` syntax, null pointer safety, dangling pointer hazards, double-free prevention, and heap metadata corruption.
- **Does not cover:** Allocation functions ([[01_malloc]], [[02_calloc]], [[03_realloc]]) or custom arena deallocations ([[11_Pools_and_arenas]]).

## Why Does It Exist
Dynamic memory is finite:
- **Resource Reclamation:** Prevents memory exhaustion by releasing heap blocks back to the runtime when they are no longer needed.
- **Lifecycle Management:** Establishes clear ownership termination boundaries for dynamic resources.

## Mechanism and Language Rules
- **Function Signature:** `void free(void *ptr);`
- **Parameters:** `ptr` must point to the beginning of a memory block allocated by `malloc`, `calloc`, or `realloc`.
- **Null Pointer Safety:** ISO C explicitly mandates that if `ptr` is `NULL`, `free(ptr)` does nothing and executes successfully. Checking `if (ptr) free(ptr);` is technically redundant but widely practiced.
- **Invalid Pointers:** Passing a pointer that was not allocated on the heap, a pointer to the middle of an allocated block (not the base address returned by the allocator), or an already-freed pointer results in undefined behavior and heap corruption.

## Examples
```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char *name;
    int *scores;
} student_record_t;

void free_student_record(student_record_t *rec) 
{
    if (!rec) {
        return;
    }

    /* Free inner dynamic allocations first */
    free(rec->name);
    free(rec->scores);

    /* Free container struct last */
    free(rec);
}

void safe_cleanup_example(void) 
{
    int *buffer = malloc(1024 * sizeof(int));
    if (!buffer) {
        return;
    }

    /* Use buffer... */

    free(buffer);
    buffer = NULL; /* Good practice: nullify pointer to prevent dangling use */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior (Double Free):** Calling `free()` twice on the exact same pointer causes heap metadata corruption, leading to arbitrary code execution or crashes.
- **Undefined Behavior (Use-After-Free):** Reading or writing through a pointer after calling `free(ptr)` triggers use-after-free undefined behavior.
- **Undefined Behavior (Stack / Static Free):** Calling `free()` on the address of a stack variable or global static variable is undefined behavior.

## Edge Cases and Failure Modes
- **Dangling Pointer Reuse:** Failing to nullify pointers after freeing (`ptr = nullptr;`) leaves dangling references that can corrupt memory if accidentally dereferenced later.
- **Partial Pointer Arithmetic Free:** Passing `ptr + 4` instead of base `ptr` to `free()` corrupts heap header metadata.

## Embedded Implications
- **Heap Corruption Crashes:** In embedded systems without memory protection units (MPUs), heap corruption caused by double-free or invalid free overwrites adjacent task stacks or control blocks, causing silent, catastrophic system failures.
- **No Automatic Garbage Collection:** C has no garbage collector; every allocation requires precise, manual deallocation matching.

## Firmware Review Angle
- **Nullify After Free:** Enforce coding guidelines where pointers are immediately set to `NULL` after `free()` within the same local scope.
- **Audit Ownership Tree:** Verify that deallocation order correctly unwraps nested structures (child allocations freed before parent structs).
- **Check for Free on Stack Variables:** Scan for `free(&local_var)` defects.

## Compiler, ABI, and Toolchain Implications
- **Allocator Metadata Inspection:** `free` inspects hidden metadata headers immediately preceding the passed pointer to determine chunk size and bin placement.

## Performance, Memory, Timing, and Power
- **Deallocation Cost:** Returning a block to the heap involves coalescing adjacent free chunks and updating free-list pointers, taking a varying number of CPU cycles.

## Verification / Debugging
- **AddressSanitizer (ASan):** Immediately traps double-frees, invalid frees (e.g., freeing stack pointers), and use-after-free bugs with detailed stack traces.
- **Valgrind Memcheck:** Reports invalid free errors and tracks un-freed blocks as memory leaks upon process exit.

## Safety, Security, and Reliability
- **Security Exploits:** Heap corruption vulnerabilities stemming from double-free errors are classic vectors for heap exploitation (e.g., fastbin/tcache attacks in glibc).
- **MISRA Compliance:** Banned in strict safety subsets due to non-deterministic timing and vulnerability to human error.

## Trade-offs and Alternatives
- **Manual `free` vs. Arenas:** Manual `free` requires tracking individual lifecycles; arena allocators (`[[11_Pools_and_arenas]]`) eliminate individual `free` calls by freeing entire memory regions at once.

## Staff-Level Takeaway
`free` is the termination of a memory lifecycle. Design your APIs with strict ownership symmetry: the module or function that allocates a resource should be clearly designated as responsible for freeing it. When pointers are freed, nullify them immediately to neutralize dangling pointer bugs.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_malloc]]
- [[02_calloc]]
- [[03_realloc]]
- [[08_Ownership_contracts]]
