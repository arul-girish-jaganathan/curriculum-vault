# 02: Function Declaration

## Definition
A function declaration (often called a function prototype) specifies the name, return type, and formal parameter types of a function without providing the function body. In ISO C (C99 §6.7.5.3), prototypes establish the type signature required for compile-time type checking and argument conversions across translation boundaries.

## Scope and Boundaries
*   **Covers:** Forward declarations, prototype syntax, parameter type lists, empty parameter lists (`()`) vs. `(void)`, parameter identifiers in prototypes, and header-file linkage.
*   **Does not cover:** Function definitions (see [[01_Function_definition]]), variable-argument lists (see [[Variadic Functions]]), or function pointer declarations (see [[13_C_Pointers/12_Function_pointers]]).

## Why Does It Exist
C utilizes separate compilation of individual translation units:
*   **Type Safety Across Units:** Enables the compiler to validate call sites (checking argument count and performing implicit conversions) before the linker resolves the definition.
*   **Mutual Recursion & Forward References:** Allows functions to call each other or call functions defined later in the same source file.
*   **Interface Decoupling:** Separates public API contracts (header files) from private implementation details (`.c` files).

## Mechanism and Language Rules
1.  **Prototype Syntax:** `return-type identifier(parameter-type-list);`.
2.  **The `(void)` vs. `()` Rule (Critical):**
    *   `int foo(void);`: Specifies a function taking **zero** arguments.
    *   `int foo();`: In C99/C11/C17, indicates an **unspecified** number of arguments (an obsolete feature). In C23, `()` is finally standardized to mean the same as `(void)`.
3.  **Identifier Scope:** Parameter names inside declarations are optional and have prototype scope; they exist purely as documentation and expire at the end of the declarator.
4.  **Compatible Declarations:** Multiple declarations of the same function are permitted within the same scope, provided all declarations specify compatible types.
5.  **Composite Type Formation:** If a declaration specifies an array size (e.g., `int f(int a[static 10]);`), it forms a composite type with subsequent declarations.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stdbool.h>

/* Correct: Prototype explicitly specifying zero arguments */
bool system_is_ready(void);

/* Correct: Prototype with descriptive parameter names */
int32_t filter_sample(int32_t raw_value, uint8_t filter_weight);

/* Correct: Multiple matching declarations allowed */
int32_t filter_sample(int32_t, uint8_t);

/* Incorrect: Obsolete unprototyped declaration (in C99/C11/C17) */
int32_t process_stream(); /* Does NOT mean void! Means unspecified args */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Calling a function declared without a prototype where the passed arguments do not match the expected parameters after default argument promotions. Calling a function through a prototype that conflicts with its actual definition.
*   **Constraint Violation:** Declaring a function with an invalid return type (e.g., returning an array or returning a function). Conflicting declarations of the same identifier with incompatible types in the same scope.
*   **Implicit Function Declarations:** In C90, calling an undeclared function caused the compiler to implicitly declare `extern int identifier();`. In C99 and later, implicit function declaration is a constraint violation.

## Edge Cases and Failure Modes
*   **The `()` Zero-Argument Trap:** Writing `void init()` in C99 allows callers to pass arbitrary arguments (`init(1, 2, 3)`) without triggering a compiler error, bypassing compile-time argument checks. Always declare zero-argument functions as `(void)`.
*   **Header Synchronization Drift:** Modifying a function definition without updating its declaration in the public header file leads to mismatched signatures, causing stack frame corruption at runtime if the compiler does not catch it.

## Embedded Implications
*   **Weak Declarations:** Embedded device drivers frequently declare weak default implementations for interrupt handlers:
    ```c
    void SysTick_Handler(void) __attribute__((weak, alias("Default_Handler")));
    ```
*   **Header Inclusion in Implementations:** Always `#include "driver.h"` inside `driver.c`. This forces the compiler to cross-check the prototype declarations in the header against the concrete definitions in the source file.

## Firmware Review Angle
1.  **Check for `(void)`:** Ban `()` in declarations; require explicit `(void)` for all parameterless functions.
2.  **No Implicit Declarations:** Ensure compiler flags treat implicit function declarations as fatal errors (`-Werror=implicit-function-declaration`).
3.  **Header Inclusion:** Verify that every `.c` file includes its matching `.h` file containing its public prototypes.

## Compiler, ABI, and Toolchain Implications
*   **Default Argument Promotion:** For functions declared with complete prototypes, arguments are converted directly to the parameter type. If a prototype is missing, integer promotions (`char`/`short` -> `int`) and float-to-double promotions occur.
*   **Compile-Time Verification:** Prototypes allow compilers to warn about implicit truncations (e.g., passing `uint32_t` into `uint8_t`).

## Performance, Memory, Timing, and Power
*   **Zero Runtime Overhead:** Declarations are purely compile-time schema metadata; they generate zero ROM instructions and consume zero RAM.
*   **Inlining Optimization:** Exposing prototypes alongside `inline` definitions in header files allows the compiler to inline functions across calling translation units.

## Verification / Debugging
*   **Compiler Warning Flags:** Enforce `-Wstrict-prototypes -Wmissing-prototypes -Werror=implicit-function-declaration`.
*   **Static Analysis:** Use tools (PC-lint, Clang Static Analyzer) to verify prototype parameter consistency across multiple compilation units.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 8.2:* Function types shall be in prototype form with named parameters.
    *   *Rule 8.4:* A compatible declaration shall be visible when an object or function with external linkage is defined.
*   **Security Hazards:** Missing prototypes allow callers to pass mismatched types, resulting in stack misalignment, parameter truncation, or register corruption across ABI boundaries.

## Trade-offs and Alternatives
*   **Prototypes in Headers vs. Monolithic Single-File Compilation:** Prototypes require header management and synchronization overhead, but enable clean architectural decoupling, parallel compilation, and modular unit testing.

## Staff-Level Takeaway
Function declarations are the type system's contract across translation boundaries. A Staff engineer must mandate strict prototyping with explicit `(void)` parameters, enforce `-Wmissing-prototypes` across the build system, and ensure that headers are rigorously included in implementation files to guarantee compile-time type verification.

## Related Concepts
*   [[01_Function_definition]]
*   [[03_Parameter_passing]]
*   [[12_Function_API_contracts]]
*   [[Stack Frame Architecture and ABI]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
