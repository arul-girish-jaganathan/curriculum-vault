# 11: Lifetime Safe APIs

## Definition
Lifetime Safe APIs are architectural design patterns in C that prevent dangling pointers, use-after-free bugs, and double frees by encoding clear ownership, borrowing, and lifecycle contracts directly into function signatures and module structures.

## Scope and Boundaries
- **Covers:** Ownership transfer contracts, opaque handles, reference counting, and destructor patterns.
- **Does not cover:** Automatic garbage collection or compiler-enforced borrow checkers (like Rust).

## Why Does It Exist
C lacks automated memory management and lifetime checking. Without disciplined API design, callers easily mismanage allocations, leading to memory corruption. Lifetime safe APIs establish clear boundaries for who allocates, who uses, and who destroys resources.

## Mechanism and Language Rules
1. **Opaque Pointers (Pimpl Idiom):** Hide implementation structs behind incomplete types to prevent direct client manipulation.
2. **Explicit Creator/Destructor Pairs:** Every `module_create()` must have a corresponding `module_destroy()`.
3. **Ownership Transfer Documentation:** Clearly document whether a function borrows a pointer (caller retains ownership) or consumes a pointer (ownership transfers to the callee).

## Examples
```c
/* ==================== safe_parser.h ==================== */
#ifndef SAFE_PARSER_H
#define SAFE_PARSER_H

typedef struct parser parser_t;

/* Allocates and returns owned parser handle */
parser_t *parser_create(const char *data, size_t len);

/* Consumes parser handle and frees all associated resources */
void parser_destroy(parser_t *parser);

/* Borrows parser handle; does not take ownership */
int parser_next_token(parser_t *parser, char *out_buf, size_t max_len);

#endif
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Passing a destroyed parser handle to `parser_next_token` (use-after-free) or failing to call `parser_destroy` (memory leak).

## Edge Cases and Failure Modes
- **Ownership Ambiguity:** Functions that conditionally take ownership based on return codes lead to double frees or memory leaks if callers misunderstand the contract.

## Embedded Implications
- **Deterministic Resource Limits:** Lifetime safe APIs ensure all buffers and contexts are explicitly allocated at startup and destroyed predictably during shutdown, preventing runtime fragmentation.

## Firmware Review Angle
- **Verify Destructor Coverage:** Every creation function must be paired with an audit-verified destruction path.
- **Check Parameter Documentation:** Enforce comments specifying `[in]`, `[out]`, `[borrowed]`, or `[owned]` ownership semantics on all pointer arguments.

## Compiler, ABI, and Toolchain Implications
- **Opaque Structs:** Incomplete type declarations prevent client code from calculating struct offsets, ensuring complete encapsulation.

## Performance, Memory, Timing, and Power
- **Zero Runtime Cost:** API design patterns introduce zero CPU overhead while eliminating entire classes of memory bugs.

## Verification / Debugging
- **Valgrind / ASan Integration:** Test API suites under memory sanitizers to verify that create/destroy cycles leave zero memory leaks.

## Safety, Security, and Reliability
- **Robustness:** Structured lifecycle contracts prevent memory corruption vulnerabilities in long-running embedded systems.

## Trade-offs and Alternatives
- **Opaque Handles vs. Direct Structs:** Opaque handles improve encapsulation and safety at the cost of requiring function calls for field access.

## Staff-Level Takeaway
In C, safety is an API design choice. Enforce strict ownership transfer rules, opaque handles, and clear creator/destructor pairings to make misuse difficult and correct usage natural.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Object_lifetime]]
- [[04_Use_after_free]]
- [[../24_C_Threads_C11/12_Thread_safe_module_design]]
