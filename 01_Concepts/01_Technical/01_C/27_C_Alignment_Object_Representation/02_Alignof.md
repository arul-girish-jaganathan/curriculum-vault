# 02: Alignof

## Definition
`_Alignof` (introduced in C11) is a unary operator that queries the alignment requirement of a specified type. Additionally, including `<stdalign.h>` provides the convenience macro `alignof`, which expands to `_Alignof`. It evaluates to a value of type `size_t` representing the number of bytes between successive valid addresses for objects of that type.

## Scope and Boundaries
- **Covers:** `_Alignof` syntax, `alignof` macro, type alignment querying, and expression restrictions.
- **Does not cover:** Forcing alignment ([[03_Alignas]]), dynamic alignment querying, or object padding calculations ([[06_Padding_bytes]]).

## Why Does It Exist
Writing portable low-level systems code (custom allocators, memory pools, serialization engines) requires knowing type alignment constraints at compile time:
- **Compile-Time Introspection:** Eliminates guesswork and hardcoded magic numbers (e.g., replacing hardcoded `4` or `8` with `alignof(uint64_t)`).
- **Allocator Alignment:** Custom allocators ([[../25_C_Dynamic_Memory/10_Custom_allocators]]) must align returned memory blocks to satisfy the strictest alignment requirement of any object type to be stored within them.

## Mechanism and Language Rules
- **Syntax:** `_Alignof(type-name)` or `alignof(type-name)`.
- **Operand Restriction:** The operand of `_Alignof` must be a type name. Unlike C++ (`alignof(expression)`), ISO C11 `_Alignof` does **not** accept expressions (e.g., `alignof(variable)` is invalid in strict C11 unless using compiler extensions or GNU extensions, though C23 expands support).
- **Constant Expression:** `_Alignof` is a constant expression and can be evaluated at compile time, making it valid in static assertions (`_Static_assert`).

## Examples
```c
#include <stdio.h>
#include <stdalign.h>
#include <stdint.h>

typedef struct {
    char c;
    uint64_t l;
} mixed_t;

int main(void) 
{
    printf("Alignment of char:     %zu\n", alignof(char));
    printf("Alignment of int:      %zu\n", alignof(int));
    printf("Alignment of double:   %zu\n", alignof(double));
    printf("Alignment of uint64_t: %zu\n", alignof(uint64_t));
    printf("Alignment of mixed_t:  %zu\n", alignof(mixed_t));

    /* Compile-time static assertion checking alignment */
    _Static_assert(alignof(mixed_t) >= alignof(uint64_t), "Mixed alignment violation");

    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Implementation-Defined:** The exact numerical values returned by `_Alignof` for types like `long double` or user-defined structures are defined by the target platform ABI.

## Edge Cases and Failure Modes
- **Expression Operand Trap (C11 Limitation):** Writing `alignof(my_variable)` in standard C11 code triggers a compile error because the operand must be a type name (`alignof(typeof(my_variable))` or `alignof(struct my_type)` is required).
- **Incomplete Types:** Querying `_Alignof` on an incomplete type (e.g., a forward-declared struct whose definition is not yet visible) is a constraint violation.

## Embedded Implications
- **DMA Buffer Alignment:** Use `alignof(uint32_t)` or target peripheral buffer requirements to statically verify that buffer alignments match hardware DMA controller specifications.

## Firmware Review Angle
- **Verify Portability:** Ensure code does not assume fixed alignment sizes across architectures (e.g., assuming `long` is always 4 bytes or 8 bytes). Use `alignof()` in assertions and memory calculations.

## Compiler, ABI, and Toolchain Implications
- **Compile-Time Evaluation:** `_Alignof` is fully resolved by the compiler front-end during semantic analysis, generating zero runtime instructions.

## Performance, Memory, Timing, and Power
- **Zero Runtime Cost:** Compile-time evaluation incurs zero CPU cycles or memory overhead at runtime.

## Verification / Debugging
- **Static Assertions:** Combine `_Alignof` with `_Static_assert` to enforce invariant structural constraints across different compiler toolchains.

## Safety, Security, and Reliability
- **Defensive Design:** Using `alignof()` guarantees that custom memory pool allocators never misalign buffers, eliminating subtle architecture-specific faults.

## Trade-offs and Alternatives
- **`alignof` vs. Hardcoded Constants:** Always prefer `alignof(T)` over hardcoding integer alignment values to maintain cross-platform portability.

## Staff-Level Takeaway
`_Alignof` is an essential meta-programming tool in C11 for building type-safe memory managers, allocators, and serialization routines. Treat it as the definitive compile-time authority on memory layout constraints.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Alignment_requirements]]
- [[03_Alignas]]
- [[../25_C_Dynamic_Memory/05_Alignment_guarantees]]
