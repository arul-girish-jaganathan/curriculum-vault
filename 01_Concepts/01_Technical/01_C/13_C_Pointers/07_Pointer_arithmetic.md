# 07: Pointer Arithmetic

## Definition
Pointer arithmetic is the application of additive operations (addition and subtraction) to pointers to navigate contiguous memory arrays. In ISO C (C99 §6.5.6), adding or subtracting an integer `n` to/from a pointer to type `T` scales `n` by `sizeof(T)` in bytes, advancing or regressing the pointer by exactly `n` elements.

## Scope and Boundaries
*   **Covers:** Addition and subtraction of integers to pointers, compound assignment (`+=`, `-=`), increment/decrement (`++`, `--`), array scaling mechanisms, and array indexing equivalence.
*   **Does not cover:** Pointer comparison and pointer subtraction/difference (see [[09_Pointer_comparison_and_subtraction]]), one-past-the-end boundary rules (see [[08_One_past_the_end]]), or pointer arithmetic on `void *` (see [[Void Pointers]]).

## Why Does It Exist
C was designed for systems programming to map directly to hardware address registers with index offsets:
*   **Efficient Sequential Traversal:** Walking memory using register-indirect addressing with auto-increment instructions.
*   **Buffer Processing:** Stepping through byte streams, communication frames, and sensor data arrays with minimal instruction overhead.
*   **Syntactic Basis for Arrays:** Under ISO C, array subscript notation `a[i]` is defined identically as the pointer arithmetic expression `*(a + i)`.

## Mechanism and Language Rules
1.  **Scaling by Element Size:** If pointer `p` points to element `i` of an array of type `T`, the expression `p + n` points to element `i + n` of the same array. The underlying physical byte address change is `n * sizeof(T)`.
2.  **Array Equivalence Rule:** `a[b]` is strictly defined as `*((a) + (b))`. Commutativity of addition means `a[i] == *(a + i) == *(i + a) == i[a]`.
3.  **Valid Bounds:** When an integer is added to or subtracted from a pointer:
    *   Both the original pointer and the resulting pointer must point to elements of the same array object, or one past the last element of the array object.
    *   Any arithmetic producing a pointer outside these bounds results in undefined behavior, even if the resulting pointer is never dereferenced.
4.  **Single Objects as Arrays:** For the purposes of pointer arithmetic, a pointer to an object that is not an element of an array is treated as if it pointed to the first element of an array of length 1.
5.  **Permitted Operations:**
    *   `pointer + integer` -> `pointer`
    *   `integer + pointer` -> `pointer`
    *   `pointer - integer` -> `pointer`
    *   `pointer++`, `++pointer`, `pointer--`, `--pointer`
    *   (Adding two pointers together is a constraint violation).

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>

static uint32_t example_traversal(const uint32_t *arr, uint32_t len)
{
    uint32_t sum = 0;
    const uint32_t *p = arr;

    /* Scaled stepping: p + 1 advances by 4 bytes (sizeof(uint32_t)) */
    for (uint32_t i = 0; i < len; ++i) {
        sum += *p;
        p++; /* Increment pointer by 1 element */
    }
    return sum;
}

/* Incorrect: Arithmetic on void pointer (ISO C constraint violation) */
static void* invalid_void_math(void *buf, int offset)
{
    /* return buf + offset; */ /* ISO C Constraint violation */
    return (uint8_t *)buf + offset; /* Correct: Cast to 1-byte element */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:**
    *   Producing a pointer that points before the beginning of the array.
    *   Producing a pointer that points beyond one-past-the-last element of the array.
    *   Performing arithmetic on a null pointer or an uninitialized pointer.
    *   Performing pointer arithmetic that causes integer wrap-around on the address space.
*   **Constraint Violation:** Adding two pointers (`p1 + p2`), multiplying/dividing pointers, or applying arithmetic to pointers to incomplete types (`void *` or undeclared `struct Foo *`).
*   **Compiler Extension:** GCC and Clang permit arithmetic on `void *` and function pointers as an extension, treating their size as 1 byte. This is non-standard and non-portable.

## Edge Cases and Failure Modes
*   **Integer Overflow in Offsets:** If `n` is large or signed negative, the calculation `p + n` can mathematically overflow or underflow the pointer's address representation, causing silent out-of-bounds pointer creation and UB.
*   **Struct Padding Traps:** Pointer arithmetic advances by `sizeof(T)`, which includes internal and trailing struct padding. Assuming consecutive struct members in separate structs form a contiguous array and stepping between them is undefined behavior.
*   **Precedence Hazards:** `*p++` reads `*p` and increments `p`. `(*p)++` reads `*p` and increments the value pointed to. Omitting parentheses causes subtle data corruption bugs.

## Embedded Implications
*   **DMA Buffer Descriptors:** Circular DMA ring buffers frequently use pointer arithmetic to advance read/write heads. Wrap-around math must be explicitly bounded to prevent stepping outside the allocated buffer descriptor array.
*   **Hardware Pointer Alignment:** Stepping pointers to packed structures (`__attribute__((packed))`) across unaligned boundaries can cause memory alignment faults on processors lacking hardware unaligned access support (e.g., ARM Cortex-M0).
*   **Physical Address Increment:** MMIO peripheral register maps are arrays of registers. Stepping a pointer to a register struct advances by the exact hardware stride only if struct member padding matches peripheral spacing.

## Firmware Review Angle
1.  **Bounds Guarding:** Verify that every pointer increment is strictly bounded by array length or sentinel checks.
2.  **Explicit Byte Stepping:** Reject arithmetic on `void *`. Insist on explicit casts to `uint8_t *` or `char *` when performing byte-level address offset calculations.
3.  **Wrap-around Math:** For ring buffers, verify modulo arithmetic or index masking is applied before pointer addition.
4.  **Operator Clarity:** Require explicit parentheses when combining indirection and arithmetic (`*(p++)` vs `(*p)++`).

## Compiler, ABI, and Toolchain Implications
*   **Address Mode Utilization:** Compilers fold pointer arithmetic directly into hardware addressing modes (e.g., `LDR R0, [R1, R2, LSL #2]` on ARM, which scales an index by 4 and loads in a single cycle).
*   **Strength Reduction:** Compilers optimize loop-indexed array lookups (`arr[i]`) into post-increment pointer arithmetic (`*p++`) to take advantage of zero-overhead hardware address auto-increments.
*   **Undefined Behavior Exploitation:** Compilers assume pointer arithmetic never overflows. If an offset check relies on pointer wrap-around (`if (p + offset < p)`), modern optimizers will optimize out the entire check as mathematically impossible under ISO C rules.

## Performance, Memory, Timing, and Power
*   **Zero-Cycle Offsetting:** On RISC architectures with indexed addressing modes, pointer arithmetic combined with dereference incurs zero extra instruction cycles.
*   **Cache Line Exploitation:** Sequential pointer arithmetic ensures optimal spatial locality, maximizing L1 cache line hits and DMA burst transfers.
*   **ROM Efficiency:** Compact loops using auto-increment pointers produce smaller machine code than repeated base-plus-scaled-index computations.

## Verification / Debugging
*   **Compiler Flags:** Use `-Wpointer-arith` to flag non-standard arithmetic (such as GNU `void *` math).
*   **Sanitizers:** Compile host unit tests with AddressSanitizer (`-fsanitize=address`) and UndefinedBehaviorSanitizer (`-fsanitize=pointer-overflow`) to catch out-of-bounds pointer creation at runtime.
*   **GDB Inspection:** Use `print p + n` to evaluate scaled addresses directly in the target address space.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 18.1:* A pointer resulting from arithmetic on a pointer operand shall address an element of the same array as that operand (or one past).
    *   *Rule 18.4:* The `+`, `-`, `+=` and `-=` operators should not be applied to an expression of pointer type (MISRA prefers explicit array indexing `a[i]` over raw pointer math).
*   **Security Vulnerabilities:**
    *   CWE-119: Memory Buffer Overflow.
    *   CWE-129: Unchecked Array Indexing.
    *   Manipulating pointers via untrusted integer offsets allows out-of-bounds reading of secrets or writing across return addresses.

## Trade-offs and Alternatives
*   **Pointer Arithmetic vs. Array Indexing:** Array indexing (`arr[i]`) is easier to read, inherently ties the index variable to loop boundary logic, and simplifies static analysis. Pointer arithmetic (`*p++`) can be more concise and historical assembly-friendly, but carries higher safety risks. Prefer array indexing for modern maintainable C.

## Staff-Level Takeaway
Pointer arithmetic is inherently bound to array bounds by ISO C rules. At a staff level, treat raw pointer arithmetic as an exception, not the rule. Where pointer walking is required for performance-critical buffer streaming, enforce strict boundary assertions and compile with `-fsanitize=pointer-overflow`. Never rely on address wrap-around to detect buffer limits.

## Related Concepts
*   [[01_Pointer_declarations]]
*   [[08_One_past_the_end]]
*   [[09_Pointer_comparison_and_subtraction]]
*   [[Memory Alignment and Padding]]
*   [[Void Pointers]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
