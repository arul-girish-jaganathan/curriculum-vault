# 04: Null Pointers

## Definition
A null pointer is an address value that is guaranteed not to point to any valid object or function. In ISO C, an integer constant expression with the value 0, or such an expression cast to type `void *`, is called a *null pointer constant*. If a null pointer constant is converted to or compared with a pointer type, it produces a *null pointer* of that specific type.

## Scope and Boundaries
*   **Covers:** Definition of null pointer constants, the `NULL` macro, nullptr semantics (C23), internal representation vs. source representation, zero-pointer conversions, and defensive null checking.
*   **Does not cover:** Invalid but non-null pointers / dangling pointers (see [[Storage Duration and Lifetime]]), uninitialized pointer values (see [[02_Pointer_initialization]]), or dynamic heap recovery strategies (see [[Dynamic Memory Allocation]]).

## Why Does It Exist
Pointers must have a distinct sentinel state that unambiguously conveys "absence of an object":
*   **Error Reporting:** Functions returning memory or handles (e.g., `malloc`, `lookup_device`) return a null pointer to signal failure or missing resources.
*   **List Termination:** Self-referential structures (linked lists, trees) use null pointers to signal terminal nodes.
*   **Optional Parameters:** Functions use null pointers for optional callback handlers or optional output parameters.
*   **Defensive Resetting:** Setting freed or invalidated pointers to null prevents double-free vulnerabilities and accidental reuse.

## Mechanism and Language Rules
1.  **Null Pointer Constant Definition:**
    *   An integer constant expression with the value `0` (e.g., `0`, `0L`).
    *   An expression of type `void *` with value 0 (e.g., `(void *)0`).
    *   In C23: The keyword `nullptr` of type `nullptr_t`.
2.  **The `NULL` Macro:** Defined in `<stddef.h>`, `<stdlib.h>`, `<string.h>`, etc., as an implementation-defined null pointer constant, typically `0` or `((void *)0)`.
3.  **Contextual Conversion:**
    *   When assigning a null pointer constant to any pointer type, it becomes the null pointer of that type.
    *   In a boolean evaluation context (such as `if (ptr)` or `if (!ptr)`), a null pointer evaluates to `false`, and any non-null pointer evaluates to `true`.
4.  **Equality and Comparison:**
    *   Two null pointers of any type always compare equal to each other.
    *   Comparing a null pointer to an integer other than a constant 0 is a constraint violation.
5.  **Dereference Prohibition:** Dereferencing a null pointer is undefined behavior. There is no requirement in ISO C that a null pointer map to address zero in physical hardware, although nearly all modern desktop and microcontroller platforms implement it as binary all-zeros.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stddef.h>
#include <stdbool.h>

/* Correct: Defensive validation against null pointer */
static bool process_data(const int *input, int *output)
{
    if (input == NULL || output == NULL) {
        return false; /* Safe failure state */
    }

    *output = *input * 2;
    return true;
}

/* Correct: Safe teardown pattern */
static void cleanup_resource(int **ptr_ref)
{
    if (ptr_ref != NULL && *ptr_ref != NULL) {
        /* free(*ptr_ref) if dynamic */
        *ptr_ref = NULL; /* Invalidate pointer to prevent use-after-free */
    }
}

/* Incorrect: Dereference prior to null check */
static int bad_check(int *ptr)
{
    int val = *ptr; /* Undefined behavior if ptr is NULL */
    if (ptr == NULL) {
        return 0;
    }
    return val;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Dereferencing a null pointer (reading or writing). Performing pointer arithmetic on a null pointer (e.g., `NULL + 1`).
*   **Implementation-Defined Behavior:** The actual bit-pattern representation of a null pointer is implementation-defined. While commonly `0x00000000`, on certain legacy platforms or niche DSP architectures, a null pointer may be represented by a non-zero bit pattern (e.g., all-ones `0xFFFFFFFF`). ISO C guarantees that writing `p = 0;` produces the correct platform representation regardless of the underlying bits.
*   **Compiler Extension:** Modern compilers treat a null pointer dereference as an immediate optimization trigger: if `*p` is executed, the compiler assumes `p` cannot be `NULL` in any code path leading to or following that dereference, often optimizing away subsequent null checks.

## Edge Cases and Failure Modes
*   **The Zero-Address Hardware Conflict:** On bare-metal microcontrollers (e.g., ARM Cortex-M), memory address `0x00000000` is mapped to physical Flash (containing the Initial Main Stack Pointer and Reset Handler Vector). A dereference of `((uint32_t *)0)` does not fault; it successfully reads the vector table. This can mask null pointer bugs indefinitely until code attempts to *write* to it (which hard-faults if Flash is read-only).
*   **Check Erasure via Optimization:** If a pointer is dereferenced *before* checking it against `NULL`, the compiler assumes `ptr != NULL` must be true and strips out the check entirely:
    ```c
    int val = *p;
    if (p == NULL) { /* Compiler eliminates this check at -O2/-O3 */
        handle_error();
    }
    ```
*   **Variadic Function Traps:** Passing `0` to a variadic function (like `execl`) expecting a pointer can fail if pointers are larger than `int` (e.g., 64-bit systems where `sizeof(int) = 4` and `sizeof(void*) = 8`). `0` will be pushed as a 32-bit integer, corrupting the argument list. Always explicitly use `(void *)0` or `NULL`.

## Embedded Implications
*   **Vector Table Overwrites:** On systems without an MMU/MPU, writing through a null pointer corrupts address `0x00000000`. On ARM Cortex-M, this corrupts the reset vector, causing an unrecoverable crash on the next reset or interrupt.
*   **MPU (Memory Protection Unit) Configuration:** Robust embedded systems use the MPU to configure region 0 (`0x00000000` to `0x000000FF` or larger) as No-Access (`PROT_NONE`). Any accidental null pointer dereference will then immediately trigger a Memory Management Fault (MemManage).
*   **Bootloader Address Remapping:** If memory aliasing or remapping registers remap RAM to `0x00000000`, null pointer writes will corrupt live data silently without hardware write-protection faults.

## Firmware Review Angle
1.  **Order of Evaluation:** Ensure pointers are verified non-null *before* any dereference occurs.
2.  **API Input Contracts:** Verify whether internal static functions require null checks. Functions that cannot accept `NULL` should be documented and assert defensively (`assert(p != NULL)`).
3.  **Teardown Nullification:** Check that pointers are explicitly cleared to `NULL` immediately after the object they point to is released, deallocated, or goes out of scope.
4.  **Implicit Integer Conversions:** Flag the use of bare `0` for pointer arguments in function calls; require `NULL` or `nullptr`.

## Compiler, ABI, and Toolchain Implications
*   **Optimization Assumptions:** GCC and Clang assume that standard-compliant environments cause an illegal trap on null pointer dereference (`-fdelete-null-pointer-checks`). On bare-metal targets where address 0 is valid memory, this optimization can break low-level firmware. Use `-fno-delete-null-pointer-checks` if mapping memory at address 0.
*   **Register Passing:** A `NULL` parameter is passed as literal zero in the designated argument register (e.g., `R0 = 0` on ARM).
*   **Built-in Attributes:** Compilers support attributes like `__attribute__((nonnull))` to emit compile-time warnings if a null pointer constant is passed to marked parameters.

## Performance, Memory, Timing, and Power
*   **Branch Cost:** Checking `if (p == NULL)` introduces a conditional branch. On modern pipelined MCUs, an unpredictable branch takes 2-3 cycles if mispredicted.
*   **Code Footprint:** Defensive checking on every single internal function parameter inflates ROM size. Use checks at API boundaries, and use compiler assertions (`assert`) for private internal invariants.
*   **Zero-Register Utilization:** Architectures with dedicated zero registers (e.g., `xzr` on AArch64, `x0` on RISC-V) compare pointers to null in a single instruction without consuming additional register space.

## Verification / Debugging
*   **Compiler Warnings:** Enable `-Wnull-dereference` and `-Wnonnull`.
*   **MPU Protection:** Configure the hardware MPU during boot to trap on address 0 reads and writes.
*   **Sanitizers:** Compile test builds with `-fsanitize=null,undefined` (Clang/GCC) to automatically catch null dereferences during unit/host testing.
*   **GDB Inspection:** Pointers will display as `0x0` or `<null>`. Attempting to read them confirms invalid reference states.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 11.9:* The macro `NULL` shall be the only permitted form of null pointer constant (forbids bare `0`).
    *   *Rule 11.8:* A cast shall not remove any `const` or `volatile` qualification from the type pointed to by a pointer.
*   **Security Vulnerabilities:**
    *   CWE-476: NULL Pointer Dereference.
    *   Exploitation: On systems where user space can map address 0 (historical Linux kernel flaws), an unhandled kernel null pointer dereference allowed local privilege escalation to root.

## Trade-offs and Alternatives
*   **Defensive Null Checks vs. Contract Assertions:** Overuse of defensive runtime null checks across private functions can hide underlying architectural bugs and degrade performance. Enforce non-null contracts via design, check at system boundaries, and assert during development.
*   **Null Object Pattern:** Instead of passing `NULL` for an empty object or optional handler, pass a reference to a valid "dummy" instance with no-op function pointers to eliminate runtime branch checks entirely.

## Staff-Level Takeaway
A null pointer represents an intentional sentinel value, not a random uninitialized state. At the staff/architectural level, system designs must define clear null-handling policies: validate untrusted boundaries, utilize the MPU to lock down physical address zero against silent corruption, and prevent the optimizer from eliminating critical checks via appropriate compiler flags (`-fno-delete-null-pointer-checks`) when address zero holds legitimate hardware memory.

## Related Concepts
*   [[00_Chapter_Index]]
*   [[01_Pointer_declarations]]
*   [[02_Pointer_initialization]]
*   [[03_Address_of_and_dereference]]
*   [[Storage Duration and Lifetime]]
*   [[Memory Protection Unit (MPU) Configuration]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
