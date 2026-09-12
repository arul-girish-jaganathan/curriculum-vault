# 08: Ownership Contracts

## Definition
Ownership contracts represent the explicit architectural agreements within a C codebase defining which module, function, or thread is responsible for freeing dynamically allocated memory and managing its lifecycle.

## Scope and Boundaries
- **Covers:** Transfer of ownership, caller-frees vs. callee-frees contracts, API documentation standards, and lifetime boundary enforcement.
- **Does not cover:** Garbage collection or automatic scope-based lifetime management (`[[../26_C_Lifetime_Aliasing/01_Object_lifetime]]`).

## Why Does It Exist
C has no compiler-enforced ownership model (unlike Rust's borrow checker):
- **Memory Leak Prevention:** Without clear ownership contracts, developers either leak memory (neither side frees it) or corrupt the heap (both sides attempt to free it).
- **API Clarity:** Explicitly documenting whether a function takes ownership of an incoming pointer or returns a newly owned pointer is vital for maintainable software architecture.

## Mechanism and Language Rules
- **Caller-Frees Contract:** The function receives a pointer or returns data pointing to caller-owned storage; the caller retains full responsibility for deallocation.
- **Callee-Frees (Transfer of Ownership) Contract:** The function takes ownership of an incoming pointer (e.g., inserting it into a data structure) and becomes responsible for eventually freeing it. Alternatively, a function allocates and returns a new heap object, transferring ownership to the caller.
- **Documentation Conventions:** Explicitly state ownership transfer semantics in header file comments (e.g., `/* Caller must free returned pointer */`).

## Examples
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char *config_string;
} parser_t;

/* CONTRACT: Returns a newly allocated string. 
   OWNERSHIP TRANSFER: Caller assumes full ownership and must free the returned pointer. */
char *parser_extract_version(const char *raw_data) 
{
    char *version = malloc(16);
    if (!version) {
        return NULL;
    }
    snprintf(version, 16, "v1.4.2");
    return version; /* Ownership transferred to caller */
}

/* CONTRACT: Takes ownership of 'config' pointer. 
   The parser now owns it and will free it during parser_destroy(). */
void parser_set_config(parser_t *parser, char *config) 
{
    free(parser->config_string); /* Free previous if any */
    parser->config_string = config; /* Ownership transferred to parser */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior (Double Ownership / Double Free):** When two modules assume they both own and must free the same pointer, a double-free bug occurs.
- **Undefined Behavior (Orphaned Memory):** When neither module frees a pointer under the mistaken assumption the other owned it, a permanent memory leak occurs.

## Edge Cases and Failure Modes
- **Partial Failure Ownership Loss:** If a compound initialization function allocates three sub-buffers and fails on the fourth, its cleanup routine must correctly free the prior three. If ownership was prematurely transferred during allocation, cleanup becomes ambiguous.

## Embedded Implications
- **Firmware Module Boundaries:** Device drivers and middleware layers must establish strict ownership contracts for packet buffers passed across interrupt-to-task queues to prevent buffer leaks.

## Firmware Review Angle
- **Audit API Headers:** Inspect all header files for clear comment annotations detailing ownership contracts on pointer parameters and return values.
- **Trace Pointer Lifecycles:** Follow dynamic pointers across module boundaries to verify single, unambiguous ownership at all times.

## Compiler, ABI, and Toolchain Implications
- **Static Analysis Annotations:** Use compiler attributes (e.g., `__attribute__((malloc))`, `__attribute__((cleanup(...)))`) to help static analyzers verify ownership and scope-based cleanup.

## Performance, Memory, Timing, and Power
- **Zero Runtime Overhead:** Ownership contracts are purely conceptual and architectural guidelines enforced through discipline and tooling; they add zero CPU instructions at runtime.

## Verification / Debugging
- **Memory Leak Detectors:** Tools like ASan, LeakSanitizer (LSan), and Valgrind verify whether allocated objects are eventually reclaimed by their designated owners.

## Safety, Security, and Reliability
- **Architectural Integrity:** Clear ownership boundaries eliminate entire classes of memory leaks, use-after-free bugs, and double-free vulnerabilities in complex systems.

## Trade-offs and Alternatives
- **Manual Ownership Contracts vs. Reference Counting:** Manual contracts are lightweight and standard in C; reference counting adds metadata overhead and atomic synchronization costs.

## Staff-Level Takeaway
In C, memory safety is entirely a function of architectural discipline. Every pointer passed across an API boundary must have an unambiguous, documented ownership contract. If you allocate it, explicitly define who owns it and who kills it.

## Related Concepts
- [[00_Chapter_Index]]
- [[04_free]]
- [[07_Allocation_failure]]
- [[../26_C_Lifetime_Aliasing/01_Object_lifetime]]
- [[../26_C_Lifetime_Aliasing/11_Lifetime_safe_API]]
