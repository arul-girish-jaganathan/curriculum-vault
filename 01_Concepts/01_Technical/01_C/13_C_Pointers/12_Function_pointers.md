# 12: Function Pointers

## Definition
A function pointer is a pointer variable that stores the memory address of executable code (a function entry point) rather than data. In ISO C (C99 §6.7.5.3), a function pointer is declared with the function signature and parentheses around the pointer declarator: `ReturnType (*identifier)(ParamTypes)`. It enables indirect function invocation and dynamic runtime dispatch.

## Scope and Boundaries
*   **Covers:** Function pointer declarations, assignment, direct/indirect call syntax, callback architectures, dispatch tables, and type compatibility.
*   **Does not cover:** Conversion between function pointers and `void *` (see [[Void Pointers]]), data-to-function pointer casting constraints (see [[01_Pointer_declarations]]), or interrupt vector tables (see [[Interrupt Handling and ISRs]]).

## Why Does It Exist
C does not have object-oriented virtual methods or closures. Function pointers provide:
*   **Dynamic Dispatch:** Selecting execution paths at runtime without massive switch/case statements (e.g., driver HALs, state machines).
*   **Callbacks:** Allowing generic subsystems (timers, event loops, sort algorithms like `qsort`) to notify application-specific code.
*   **Polymorphism:** Constructing virtual method tables (vtables) in C for modular interfaces.

## Mechanism and Language Rules
1.  **Declaration Syntax:**
    *   `int (*fp)(int, int);`: Pointer to a function taking two `int`s and returning `int`.
    *   `int *fp(int, int);`: Function declaration returning a pointer to `int` (precedence of `()` is higher than `*`).
2.  **Address and Invocation Identity:**
    *   Function names automatically decay into function pointers: `fp = my_func;` is equivalent to `fp = &my_func;`.
    *   Invocation syntax is interchangeable: `fp(1, 2);` is equivalent to `(*fp)(1, 2);`.
3.  **Type Compatibility:** A function pointer can only be safely called if the function pointed to is compatible with the pointed-to function type (matching return type, matching parameter count, and compatible parameter types).
4.  **No Arithmetic:** Function pointers point to code, not data. Pointer arithmetic on function pointers is strictly forbidden in ISO C.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stddef.h>

/* Minimal function pointer typedef for clean syntax */
typedef int32_t (*math_op_t)(int32_t, int32_t);

static int32_t add(int32_t a, int32_t b) { return a + b; }
static int32_t sub(int32_t a, int32_t b) { return a - b; }

/* Minimal dispatch table */
static const math_op_t g_ops[] = { add, sub };

static int32_t example_dispatch(size_t op_index, int32_t a, int32_t b)
{
    if (op_index >= (sizeof(g_ops) / sizeof(g_ops[0]))) {
        return 0;
    }

    math_op_t handler = g_ops[op_index];
    if (handler != NULL) {
        return handler(a, b); /* Indirect call */
    }
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:**
    *   Calling a function pointer that is `NULL` or uninitialized.
    *   Calling a function through a pointer whose signature is incompatible with the real function definition (e.g., calling `void (*)(void)` when the function is `void (*)(int)`).
    *   Casting a function pointer to an object pointer (`void *`) or integer and back in standard ISO C (though allowed in POSIX via `dlsym`).
*   **Constraint Violation:** Attempting pointer arithmetic (`fp++`) on a function pointer.
*   **Implementation-Defined:** Calling convention mismatches (e.g., `__cdecl` vs `__stdcall`) on architectures that support multiple calling conventions.

## Edge Cases and Failure Modes
*   **Signature Mismatch Stack Corruption:** Calling a function via an incompatible signature corrupts the stack frame or registers (e.g., caller passes 4 arguments, callee expects 1), leading to crashes or return address corruption.
*   **Unchecked NULL Calls:** Invoking an unassigned callback pointer (`if (cb) cb();` omitted) causes an immediate crash or HardFault.
*   **Type Confusion via `void *`:** Storing function pointers in generic `void *` variables strips signature checking and invites illegal invocation casts.

## Embedded Implications
*   **Interrupt Vector Tables:** Microcontroller vector tables (e.g., ARM Cortex-M vector table at address `0x00000000`) are simply static arrays of function pointers placed at fixed linker locations.
*   **Driver Hardware Abstraction Layers (HALs):** Peripheral drivers use structs of function pointers to expose uniform APIs across different hardware variants:
    ```c
    struct UartDriver {
        void (*init)(uint32_t baud);
        void (*putc)(char c);
    };
    ```
*   **RAM Function Execution (Thumb Bit):** On ARM Cortex-M, the least significant bit (LSB) of a function pointer address must be `1` to indicate Thumb state. If an absolute address is loaded manually without setting bit 0, the processor triggers an `INVSTATE` UsageFault on call.

## Firmware Review Angle
1.  **Null Guard Before Call:** Verify that every function pointer call is guarded (`if (fp != NULL) fp();`) or guaranteed non-null by design.
2.  **Typedef Enforcement:** Mandate `typedef` declarations for all function pointer signatures to prevent unreadable, bug-prone declaration syntax.
3.  **Const Dispatch Tables:** Ensure static dispatch tables and HAL driver structs of function pointers are declared `const` so they reside in Flash/ROM, preventing runtime hijacking.
4.  **Signature Compatibility:** Verify that functions registered as callbacks match the expected typedef signature exactly, without using casts to suppress warnings.

## Compiler, ABI, and Toolchain Implications
*   **Branch-and-Link Indirect:** Compilers translate function pointer calls to indirect branch instructions (e.g., `BLX Rm` on ARM, `call *%rax` on x86).
*   **Inlining & Optimization Barriers:** Function pointers prevent compile-time inlining and constant propagation unless Link Time Optimization (LTO) can statically prove the target.
*   **Branch Target Identification / CFI:** Modern processors utilize Control Flow Integrity (CFI) and Branch Target Identification (ARM BTI) to ensure indirect branches only target valid function landing pads.

## Performance, Memory, Timing, and Power
*   **Branch Misprediction Penalty:** Indirect calls through function pointers cannot easily be predicted by simple CPU branch predictors, potentially stalling pipelines by 10-15 cycles on deep architectures.
*   **Memory Lookups:** Function calls through structs (e.g., `driver->send()`) require loading the function address from memory before branching, adding latency compared to direct calls.
*   **Determinism:** Function pointers introduce variable latency depending on cache and branch history, which must be accounted for in hard real-time tasks.

## Verification / Debugging
*   **Compiler Diagnostics:** Compile with `-Wstrict-prototypes` and `-Wcast-function-type` to detect signature mismatches.
*   **GDB Inspection:** GDB identifies function pointers cleanly: `print fp` outputs the function address and the associated symbol name (e.g., `{int (int, int)} 0x08000240 <add>`).
*   **Static Analysis:** Tools verify that dispatch table indices are bounded and callbacks are non-null.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 11.1:* Conversions shall not be performed between a pointer to a function and any other type (including `void *` and integers).
*   **Security Vulnerabilities:**
    *   CWE-822: Untrusted Pointer Dereference.
    *   Corrupting a function pointer via a buffer overflow allows an attacker to hijack the CPU's Program Counter (PC), executing arbitrary code. Storing function pointer tables in read-only Flash (`const`) is critical for defense.

## Trade-offs and Alternatives
*   **Function Pointers vs. Switch/Case:**
    *   *Function Pointers:* O(1) dispatch, modular, decoupled architecture, extensible without modifying central dispatcher. Harder for compilers to inline and branch-predict.
    *   *Switch/Case:* O(1) to O(N) dispatch, tightly coupled, requires editing central enum/switch when adding features. Easier for compilers to optimize, inline, and statically verify.

## Staff-Level Takeaway
Function pointers are the bedrock of modular, polymorphic architectures in C. Staff engineers must enforce two cardinal rules: never store mutable function pointer tables in RAM where memory corruptions can lead to code execution exploits (always use `const` tables in Flash), and never cast function pointer types to suppress signature warnings.

## Related Concepts
*   [[01_Pointer_declarations]]
*   [[04_Null_pointers]]
*   [[Void Pointers]]
*   [[Interrupt Handling and ISRs]]
*   [[Linker Scripts and Memory Sections]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
