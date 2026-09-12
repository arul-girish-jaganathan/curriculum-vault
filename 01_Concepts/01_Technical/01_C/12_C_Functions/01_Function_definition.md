# 01: Function Definition

## Definition
A function definition specifies the name, return type, formal parameters, storage-class specifier, function specifiers (`inline`, `_Noreturn`), and the body (compound statement) of a function. In ISO C (C99 §6.9.1), a function definition constructs the executable translation unit object that binds an entry symbol to an executable block of code.

## Scope and Boundaries
*   **Covers:** Modern prototype function definitions, storage class specifiers (`static`, `extern`), specifiers (`inline`, `_Noreturn`), parameter scope, and body execution rules.
*   **Does not cover:** Non-defining prototypes (see [[02_Function_declaration]]), ABI calling conventions (see [[11_Calling_conventions]]), or function pointers (see [[13_C_Pointers/12_Function_pointers]]).

## Why Does It Exist
Function definitions are the primary structural abstraction in procedural programming:
*   **Modular Decomposition:** Encapsulating algorithms into testable, discrete computational units.
*   **Scope Isolation:** Establishing private local variable frames with automatic storage duration.
*   **Symbol Binding:** Providing the linker with concrete code definitions to resolve declared references.

## Mechanism and Language Rules
1.  **Syntax:** `storage-class-specifier(opt) type-specifier declarator compound-statement`.
2.  **Storage Classes:**
    *   `static`: Internal linkage. The function symbol is scoped strictly to the translation unit.
    *   `extern` (or omitted): External linkage. The function symbol is visible globally across all translation units during linking.
3.  **Parameter Scope:** Formal parameter identifiers have block scope matching the outermost compound statement of the function body.
4.  **Implicit Return Behavior:**
    *   For non-`void` functions, reaching the closing brace `}` without executing an explicit `return expression;` invokes undefined behavior if the caller attempts to evaluate the returned value (ISO C99 §6.9.1p12).
    *   Special exception: `main()` implicitly returns `0` if the closing brace is reached without a `return` statement (C99 §5.1.2.2.3).
5.  **Old-Style (K&R) Obsolete:** Identifier-list definitions (`int f(a, b) int a; int b; { ... }`) are obsolete in C99 and formally removed in C23.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stdbool.h>

/* Correct: Static function definition with complete prototype */
static int32_t compute_checksum(const uint8_t *data, size_t len)
{
    int32_t sum = 0;
    for (size_t i = 0; i < len; ++i) {
        sum += data[i];
    }
    return sum;
}

/* Incorrect: Non-void function omitting return on execution branch */
static int32_t invalid_branch(int32_t code)
{
    if (code > 0) {
        return code * 2;
    }
    /* ERROR: Execution falls through to closing brace without returning a value */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Flowing off the end of a non-void function and having the caller read the return value. Modifying formal parameters marked `const` through pointer casts. Defining two functions with the same identifier and external linkage in the same program (ODR violation).
*   **Constraint Violation:** Attempting to define a function inside another function (nested functions are forbidden in ISO C). Returning an expression in a `void` function.
*   **Compiler Extension:** GCC/Clang support nested functions via executable stack trampolines; this is non-standard, insecure, and breaks W^X protections.

## Edge Cases and Failure Modes
*   **The Unreachable Fallthrough:** If all `switch` branches or `if-else` trees return a value, but the compiler cannot statically verify exhaustiveness, execution falling off the end triggers UB in release builds (`-O2/-O3`), where compilers often emit `ud2` (illegal opcode trap).
*   **External Linkage Collisions:** Omitting `static` on utility functions in multiple `.c` files creates linker symbol collisions (`multiple definition of ...`) or silent symbol hijacking if weak linkage is active.

## Embedded Implications
*   **Section Placement:** Embedded firmware places performance-critical functions into internal SRAM instead of Flash using attributes:
    ```c
    __attribute__((section(".ramfunc"), noinline)) void critical_flash_write(void) { ... }
    ```
*   **Interrupt Handlers (ISRs):** An ISR is a function definition with hardware-invoked linkage. In bare-metal C, attributes like `__attribute__((interrupt))` configure entry/exit sequences to preserve execution contexts and use return-from-exception instructions (`BX LR` with EXC_RETURN on Cortex-M).

## Firmware Review Angle
1.  **Default to `static`:** Enforce that every function definition is `static` unless it is explicitly exported via a public header file.
2.  **Exhaustive Returns:** Verify that every code branch in non-`void` functions terminates with an explicit `return`.
3.  **Prototype Matching:** Ensure function definitions match their preceding prototype declaration precisely in qualifiers and types.

## Compiler, ABI, and Toolchain Implications
*   **Prologue / Epilogue Generation:** The compiler generates function prologues (allocating stack frames, pushing callee-saved registers) and epilogues (restoring registers, returning) based on target ABI.
*   **Link-Time Optimization (LTO):** LTO can eliminate unused static functions and inline small extern definitions across translation units.

## Performance, Memory, Timing, and Power
*   **Stack Allocation:** Function frames consume stack RAM for local variables and saved registers. Deep call depths risk stack overflows on RAM-constrained microcontrollers.
*   **Call Overhead:** Function calls incur instruction cycles for pushing/popping registers and branch misprediction penalties.

## Verification / Debugging
*   **Compiler Flags:** Enforce `-Wreturn-type -Wmissing-prototypes -Wstrict-prototypes`.
*   **Disassembly Inspection:** Review generated assembly (`objdump -d`) to verify prologue frame size and register preservation.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 8.4:* A compatible declaration shall be visible when an object or function with external linkage is defined.
    *   *Rule 17.4:* All exit paths from a function with non-void return type shall have an explicit return statement.
*   **Security Vulnerabilities:** Missing return statements allow uninitialized register values to be read by callers, causing information leakage or broken validation logic.

## Trade-offs and Alternatives
*   **Monolithic Functions vs. Modular Functions:** Small modular functions improve readability and unit testing, but increase stack frame usage and call overhead if not inlined.

## Staff-Level Takeaway
A function definition establishes a hard ABI boundary. Treat internal functions as `static` translation-unit private entities. For extern definitions, always ensure the public header is included directly in the implementation file to verify declaration-definition synchronization at compile time.

## Related Concepts
*   [[02_Function_declaration]]
*   [[07_Returning_values]]
*   [[10_Inline_functions]]
*   [[11_Calling_conventions]]
*   [[Stack Frame Architecture and ABI]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
