# 10: Pointer to Pointer

## Definition
A pointer to a pointer (double indirection, denoted by `**`) is a pointer object whose pointee type is itself another pointer. In ISO C (C99 §6.7.5.1), declaring `T **p;` creates an object `p` that holds the memory address of an object of type `T *`, which in turn holds the memory address of an object of type `T`.

## Scope and Boundaries
*   **Covers:** Double indirection syntax, pass-by-reference for pointer variables (out-parameters), dynamically allocated 2D arrays, arrays of pointers, and pointer reallocation patterns.
*   **Does not cover:** Pointer to array types (see [[11_Pointer_to_array]]), generic void double pointers (see [[Void Pointers]]), or function pointer tables (see [[12_Function_pointers]]).

## Why Does It Exist
C passes all function arguments strictly by value:
*   **Mutating Caller Pointers:** To modify a caller's pointer variable inside a function (e.g., allocating memory, advancing a parse head, or modifying a list root), the caller must pass the address of that pointer (`&ptr`), received as `**ptr`.
*   **Ragged Arrays:** Representing collections of strings or dynamically sized multi-dimensional arrays where each row has a different length (e.g., `argv`).
*   **Handle-based Systems:** Enabling indirect handles that allow underlying memory blocks to be relocated without invalidating client handles.

## Mechanism and Language Rules
1.  **Indirection Levels:**
    *   `p`: Holds the address of the pointer variable (type `T **`).
    *   `*p`: Evaluates to the pointer variable itself (type `T *`).
    *   `**p`: Evaluates to the underlying data object (type `T`).
2.  **No Implicit `void **` Conversion:** A `T **` does **not** implicitly convert to `void **`. While `T *` converts to `void *`, `T **` and `void **` are pointers to different types, and implicit conversion violates constraint rules.
3.  **Const Qualification Levels:**
    *   `const T **p`: Pointer to a pointer to const data (the underlying data is immutable).
    *   `T * const *p`: Pointer to a const pointer to mutable data (the intermediate pointer is immutable).
    *   `T ** const p`: Const pointer to a pointer to mutable data (the outer pointer is immutable).

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

/* Correct: Out-parameter modifying caller's pointer */
static bool allocate_buffer(uint8_t **out_ptr, size_t size)
{
    static uint8_t pool[256]; /* Fixed pool for minimal demonstration */
    if (out_ptr == NULL || size > sizeof(pool)) {
        return false;
    }
    *out_ptr = pool; /* Directly modifies the pointer in caller scope */
    return true;
}

/* Correct: Safe handle-based deallocation */
static void safe_release(int32_t **ref_ptr)
{
    if (ref_ptr != NULL && *ref_ptr != NULL) {
        /* perform deallocation if dynamic */
        *ref_ptr = NULL; /* Sets caller's pointer to NULL */
    }
}

static void example_usage(void)
{
    uint8_t *buf = NULL;
    if (allocate_buffer(&buf, 64)) {
        /* buf now points to pool */
        buf[0] = 0xAA;
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:**
    *   Dereferencing a null or uninitialized pointer at either level (`*p` or `**p`).
    *   Passing a pointer to an automatic variable and storing it beyond its scope.
*   **Constraint Violation:** Implicitly converting between `T **` and `void **`, or passing `T **` into an API expecting `const T **` without explicit casts.
*   **Implementation-Defined:** Representation of pointers. While all standard object pointers share representation on common architectures, multi-level pointers are strictly governed by type compatibility rules.

## Edge Cases and Failure Modes
*   **The Inadvertent Local Update:** Writing `ptr = NULL;` inside a cleanup function instead of `*ptr = NULL;` modifies only the local function parameter copy, leaving the caller's pointer dangling.
*   **Double-Free Prevention Failure:** Failing to pass a double pointer to free/teardown functions means caller pointers cannot be set to `NULL`, leading to use-after-free bugs.
*   **`void **` Aliasing Violations:** Forcing `(void **)&my_typed_ptr` violates strict aliasing rules. If the compiler reorders writes, changes through the `void **` may not be seen through `my_typed_ptr`.

## Embedded Implications
*   **Zero-Copy Queue Management:** FreeRTOS and other RTOS kernels use double pointers in queue management to transfer buffer pointers between tasks without copying payload data.
*   **Buffer Head Tracking:** Communication drivers (e.g., packet parsers) pass `uint8_t **stream` to packet decoders. The decoder consumes bytes and increments `*stream`, directly updating the driver's read pointer.
*   **Linked List Sentinel Nodes:** Managing head nodes of linked lists (e.g., timer queues) requires `Node **head` so insertion at the beginning modifies the root list pointer cleanly.

## Firmware Review Angle
1.  **Double Null Check:** Verify that functions taking `Type **out` check both `out != NULL` and, before dereferencing the data, `*out != NULL`.
2.  **Aliasing Casts:** Reject casts of concrete pointer addresses to `(void **)` (e.g., `func((void **)&my_ptr)`). Use a temporary `void *` variable instead.
3.  **Indirection Clarity:** Check that expressions like `*p++` vs `(*p)++` match design intent.

## Compiler, ABI, and Toolchain Implications
*   **Double Memory Load:** Accessing `**p` requires two sequential memory load operations: first loading the address from `p`, then loading the data from that address (`LDR R0, [R1]; LDR R0, [R0]`). This doubles memory access latency.
*   **Optimization Barrier:** Double pointers severely limit compiler optimization because the compiler must assume that writes to `**p` can potentially alias the pointer `*p` itself unless proved otherwise.

## Performance, Memory, Timing, and Power
*   **Latency Cost:** Sequential pointer chases (`p -> *p -> **p`) cause CPU stalls and cache misses, disrupting execution pipelines.
*   **Memory Footprint:** Each layer of indirection adds 4 bytes (on 32-bit MCUs) or 8 bytes (on 64-bit systems) of pointer storage.
*   **Power Consumption:** Frequent dereferences of fragmented memory structures cause continuous L1/SRAM cache line fills, increasing dynamic power draw.

## Verification / Debugging
*   **Static Analysis:** Static analysis tools verify that pointer out-parameters are initialized across all function return paths.
*   **GDB Inspection:** Inspect double pointers using `print p`, `print *p`, and `print **p` to verify each layer of indirection independently.
*   **Sanitizers:** Compile with `-fsanitize=address` to catch double-indirection use-after-free or dangling reference bugs.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 17.5:* The declaration of an array parameter shall not contain more than two levels of indirection.
*   **Security Vulnerabilities:**
    *   CWE-416: Use After Free.
    *   CWE-476: NULL Pointer Dereference.
    *   Corrupted pointer-to-pointer variables allow arbitrary write primitives, allowing attackers to hijack control flow or overwrite function pointers.

## Trade-offs and Alternatives
*   **Double Pointers vs. Struct Envelopes:** Instead of passing `Type **`, wrap the pointer in a management struct (e.g., `struct BufferManager { uint8_t *head; size_t len; }`) and pass a pointer to the struct (`struct BufferManager *`). This improves readability, reduces indirection syntax errors, and simplifies API extension.

## Staff-Level Takeaway
Double pointers are C's idiom for mutable reference parameters and dynamic array management. A Staff engineer should enforce safe wrapper idioms: always validate both levels of indirection against `NULL`, never use `(void **)` casts that break strict aliasing, and wrap complex multi-level pointers into domain-specific structures to maintain readability and compiler optimization opportunities.

## Related Concepts
*   [[01_Pointer_declarations]]
*   [[02_Pointer_initialization]]
*   [[03_Address_of_and_dereference]]
*   [[11_Pointer_to_array]]
*   [[Strict Aliasing and Effective Types]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
