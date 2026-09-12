# 03: Address-of and Dereference

## Definition
The address-of operator (unary `&`) and the dereference/indirection operator (unary `*`) are inverse operations in C. The unary `&` yields the memory address of its operand (an lvalue designating an object or function). The unary `*` dereferences a pointer expression, producing an lvalue that designates the object or function to which the pointer points.

## Scope and Boundaries
*   **Covers:** Semantics of unary `&` and `*`, lvalue requirements, pointer dereferencing constraints, array decay interactions, structure member indirection (`->` operator), and pointer evaluation.
*   **Does not cover:** Pointer arithmetic stepping rules (see [[07_Pointer_arithmetic]]), alignment fault architectures (see [[Memory Alignment and Padding]]), or null pointer validation (see [[04_Null_pointers]]).

## Why Does It Exist
C operates directly on physical/virtual address spaces. These two operators provide the fundamental link between an abstracted identifier and the underlying memory cell:
*   **`&` (Address-of):** Transforms an existing object into a referenceable pointer, allowing callers to pass references to large structures or enable out-parameters for callee mutation.
*   **`*` (Dereference):** Navigates from an address back to the actual data stored at that address, enabling indirect access, dynamic data structures, and peripheral register manipulation.

## Mechanism and Language Rules
1.  **Address-of (`&`) Constraints:**
    *   Operand must be an lvalue designating an object (not declared with the `register` storage class specifier), or a function designator.
    *   Cannot take the address of a bit-field.
    *   Cannot take the address of a literal or non-lvalue expression (e.g., `&(x + 1)` is a constraint violation).
2.  **Dereference (`*`) Constraints:**
    *   Operand must have a pointer-to-object or pointer-to-function type.
    *   Cannot dereference a pointer to an incomplete type, including `void *` (e.g., `*void_ptr` is illegal).
    *   If the operand points to an object, the result is an lvalue referring to that object.
3.  **Member Dereference (`->`):** The expression `p->m` is syntactically equivalent to `(*p).m`.
4.  **Inverse Identity:** For any lvalue `x` of an object type (excluding bit-fields and `register` objects), `*&x` is identical in evaluation to `x`. In C99 and later, the subexpression `&*p` does not evaluate `*p`; if `p` is a valid pointer (or null), `&*p` simply yields `p` without dereferencing it.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>

struct Point {
    int32_t x;
    int32_t y;
};

static int32_t example_ops(void)
{
    struct Point pt = { .x = 10, .y = 20 };
    struct Point *ptr = &pt; /* Address-of operator */

    /* Dereference via unary * */
    (*ptr).x = 15;

    /* Dereference via arrow operator */
    ptr->y = 25;

    return ptr->x + ptr->y;
}

/* Incorrect: Constraint violations */
static void invalid_operations(void)
{
    int val = 5;
    /* int *p = &(val + 1); */ /* Constraint violation: address of temporary rvalue */

    void *generic = &val;
    /* int x = *generic;   */ /* Constraint violation: cannot dereference void* */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior (Invalid Dereference):** Dereferencing a pointer that is:
    *   Null (`*NULL`).
    *   Unaligned for the pointee type on architectures enforcing alignment.
    *   Dangling (points to an object past its lifetime).
    *   Out of bounds (pointing past the allocated bounds or before the array).
*   **Constraint Violation:** Applying `&` to a variable declared with `register`. Applying `*` to an integer or `void *`.
*   **Implementation-Defined:** Dereferencing an arbitrary platform-specific integer converted to a pointer without verifying physical memory mapping.

## Edge Cases and Failure Modes
*   **Operator Precedence Hazards:** Unary `*` and prefix `++` have the same precedence and associate from right to left.
    *   `*p++`: Increments pointer `p`, but dereferences the old address.
    *   `(*p)++`: Increments the value pointed to by `p`.
    *   `*++p`: Increments pointer `p`, then dereferences the new address.
    *   `++*p`: Increments the value pointed to by `p`.
*   **Side Effects in Subexpressions:** In `&*expr`, ISO C states that neither operator is evaluated if `expr` is a pointer, meaning side effects like `&*p++` will still increment `p`, but `*p` is not dereferenced.
*   **Array Decay Identity:** For an array `int arr[10];`, `arr` decays to `&arr[0]` (type `int *`), whereas `&arr` has type `int (*)[10]` (pointer to an array of 10 integers). Their numerical address is identical, but their pointer arithmetic steps differ entirely.

## Embedded Implications
*   **Hardware MMIO Dereferencing:** Every access to an embedded peripheral involves dereferencing a volatile pointer. If the dereference lacks `volatile`, the compiler may collapse sequential writes or optimize out continuous polling reads:
    ```c
    #define REG_STATUS (*(volatile uint32_t *)0x40001000UL)
    while ((REG_STATUS & 0x01U) == 0U) { /* Spin wait */ }
    ```
*   **Unaligned Access Traps:** Many ARM Cortex-M0/M0+ or RISC-V cores will generate a UsageFault or HardFault if an unaligned pointer is dereferenced (e.g., dereferencing a `uint32_t *` whose address is not a multiple of 4).
*   **Atomic Access Guarantees:** Dereferencing a 32-bit pointer on a 32-bit architecture is generally atomic with respect to interrupts (single `LDR`/`STR` instruction), but dereferencing 64-bit types (`uint64_t *`) generates two separate 32-bit instructions (`LDRD` or two `LDR`s), which is non-atomic and susceptible to interrupt race conditions.

## Firmware Review Angle
1.  **Precedence Clarity:** Flag ambiguous constructs such as `*p++` in reviews. Mandate explicit parentheses `*(p++)` or split into separate statements.
2.  **Missing Volatile on Dereferences:** Ensure pointers referencing hardware or shared ISR memory are dereferenced through `volatile` types.
3.  **Null Guarding:** Verify that every dereference of a pointer passed from an external API or caller is guarded against `NULL` prior to dereferencing.
4.  **Bit-field Address Traps:** Check that code does not attempt to pass individual struct bit-fields to functions expecting pointers.

## Compiler, ABI, and Toolchain Implications
*   **Instruction Selection:** A pointer dereference (`*p`) maps directly to target load/store instructions (`LDR`/`STR` on ARM, `MOV` on x86).
*   **Register Elimination:** If the address of a local variable is taken (`&local_var`), the compiler can no longer keep that variable purely inside a CPU register; it must allocate space for it on the stack frame so it has a physical memory address.
*   **Strict Aliasing:** Compilers use type-based alias analysis (TBAA). Dereferencing pointers of incompatible types that point to the same memory allows the optimizer to assume they do not alias, leading to reordered or eliminated memory accesses.

## Performance, Memory, Timing, and Power
*   **Stack Spill Penalty:** Taking the address of local variables (`&var`) prevents them from living entirely in registers, driving up stack usage and adding memory load/store overhead.
*   **Cache Line Hits/Misses:** Indirection introduces memory latency. Dereferencing fragmented or scattered pointers results in CPU cache misses, increasing bus wait cycles and dynamic power consumption.
*   **Pipelining:** Sequential pointer dereferences create pipeline load-use data hazards, stalling the execution pipeline if the subsequent instruction immediately depends on the loaded value.

## Verification / Debugging
*   **Hardware Watchpoints:** Modern debuggers (via JTAG/SWD) can trap when a specific memory address is dereferenced for write using CPU hardware watchpoint units (e.g., ARM DWT).
*   **Fault Analysis:** When a HardFault or SIGSEGV occurs due to an invalid dereference, inspect the fault address register (e.g., Cortex-M `BFAR` or `MMFAR`) to determine the exact pointer address that caused the fault.
*   **Static Analyzers:** Enforce rules via tools like Clang Static Analyzer or Cppcheck to detect null pointer dereferences and out-of-bounds pointer reads.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 1.3:* There shall be no occurrence of undefined behavior (strictly bans invalid dereferencing).
    *   *Rule 12.1:* The precedence of operators within expressions should be made explicit using parentheses.
*   **Security Vulnerabilities:** Dereferencing invalid pointers is the leading cause of memory corruption exploits:
    *   Null pointer dereference leads to denial of service (system crash/reboot).
    *   Arbitrary pointer write dereference (`*ptr = val`) gives attackers write-what-where primitives, enabling control flow hijacking.

## Trade-offs and Alternatives
*   **Direct Value vs. Indirect Access:** Pass-by-pointer avoids copying large structures, but introduces the hazard of invalid dereferences and kills register optimization for callee locals. Small scalar values (e.g., `uint32_t`, `int`) should always be passed by value.
*   **Array Indexing vs. Pointer Dereferencing:** Prefer array indexing (`arr[i]`) over raw pointer stepping and dereferencing (`*(arr + i)`) for readability and easier boundary verification by static analysis tools.

## Staff-Level Takeaway
Address-of and dereference operations are the execution boundary between CPU registers and memory. Senior engineers must enforce explicit precedence with parentheses, avoid taking the addresses of local variables in time-critical paths (to keep them in registers), and ensure every dereference is backed by guaranteed lifetime, strict alignment, and verified non-null status.

## Related Concepts
*   [[00_Chapter_Index]]
*   [[01_Pointer_declarations]]
*   [[02_Pointer_initialization]]
*   [[04_Null_pointers]]
*   [[07_Pointer_arithmetic]]
*   [[Memory Alignment and Padding]]
*   [[Strict Aliasing and Effective Types]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
