# 05: Void Pointers

## Definition
A void pointer (`void *`) is the generic object pointer type in C. It is a pointer to an incomplete type (`void`) that cannot be completed. ISO C guarantees that a pointer to `void` has the same representation and alignment requirements as a pointer to a character type (`char *`). It serves as a raw memory address stripped of its underlying type information, acting as the fundamental mechanism for type-erased polymorphic programming in C.

## Scope and Boundaries
*   **Covers:** `void *` syntax, semantics, implicit/explicit conversions, object pointer type erasure, and alignment guarantees.
*   **Does not cover:** Function pointers (see [[12_Function_pointers]]), strict aliasing rules (see [[Strict Aliasing and Effective Types]]), or integer-to-pointer conversions (see [[uintptr_t and intptr_t]]).

## Why Does It Exist
C does not have templates, generics (until C11 `_Generic`, which is limited), or base object classes. `void *` exists to enable generic programming and memory manipulation where the specific data type is either unknown or irrelevant to the function being called:
*   **Memory APIs:** Functions like `malloc` and `memcpy` operate on raw bytes.
*   **Generic Algorithms:** `qsort` and `bsearch` must sort arrays of arbitrary structures.
*   **Opaque Contexts:** RTOS tasks, event loops, and callbacks use `void *` to pass arbitrary user-defined context blocks through generic framework code.

## Mechanism and Language Rules
1.  **Implicit Conversion:** Any pointer to an *object* or *incomplete type* can be implicitly converted to `void *` and back to its original type without loss of information or change in value.
2.  **No Dereferencing:** You cannot directly dereference a `void *` because the compiler does not know the size or type of the object it points to (it is an incomplete type).
3.  **No Pointer Arithmetic:** ISO C strictly forbids pointer arithmetic (addition, subtraction, array subscripting) on `void *` because the size of the pointed-to object is unknown.
4.  **Qualifiers:** A pointer to a qualified type (e.g., `const int *`) cannot be implicitly converted to a plain `void *`. It must be converted to a `const void *` to preserve const-correctness.
5.  **Not for Functions:** A pointer to a function cannot be portably converted to a `void *`. `void *` is explicitly for object pointers.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stddef.h>
#include <stdint.h>

/* Correct: Passing contextual state via generic pointer */
static void execute_callback(void (*cb)(void *), void *context) 
{
    if (cb) {
        cb(context);
    }
}

/* Correct: Safely casting back to the known type */
static void my_callback(void *context) 
{
    /* Cast is implicit in C, but explicit assignment clarifies intent */
    int *state = context; 
    (*state)++;
}

/* Incorrect: Attempting arithmetic (Constraint Violation) */
static void* invalid_arithmetic(void *ptr) 
{
    return ptr + 1; /* ERROR: ISO C forbids arithmetic on void* */
}

/* Incorrect: Dereferencing (Constraint Violation) */
static int invalid_deref(void *ptr) 
{
    return *ptr;    /* ERROR: Cannot dereference void* */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Constraint Violation (Arithmetic):** Performing `ptr + 1` on a `void *` violates ISO C constraints. **Compiler Extension:** GNU C (GCC/Clang) explicitly allows arithmetic on `void *` as an extension, treating the size of `void` as 1 byte. Code relying on this is non-portable.
*   **Undefined Behavior (Function Pointers):** Casting a function pointer (e.g., `void (*)(void)`) to `void *` is undefined in ISO C. (POSIX specifically requires it to work for `dlsym`, but embedded bare-metal compilers are not bound by POSIX).
*   **Undefined Behavior (Alignment/Aliasing):** Converting an object pointer to `void *` is always safe. Converting it *back* to a type with stricter alignment requirements than the original object, or dereferencing it as an incompatible type, triggers UB (Strict Aliasing Violation / Alignment Fault).

## Edge Cases and Failure Modes
*   **Type Erasure Traps:** Once cast to `void *`, the compiler abandons type checking. Passing a `float *` to an API that internally casts the `void *` to `int *` will compile without warnings but fail catastrophically at runtime.
*   **Accidental `const` Stripping:** If a programmer explicitly casts `(void *)` over a `const uint32_t *`, they silently strip the `const` qualifier, allowing downstream code to attempt writes to Read-Only memory (ROM/Flash), causing a hard fault.
*   **Double Pointers:** A `char **` does *not* implicitly convert to `void **`. It only implicitly converts to `void *`.

## Embedded Implications
*   **RTOS Tasks:** Every major RTOS (FreeRTOS, Zephyr) uses `void *` for task parameters (`void vTask(void *pvParameters)`). Careless casting of stack-allocated variables passed to RTOS tasks often leads to use-after-free bugs if the creator function exits before the task runs.
*   **DMA and Hardware Buffers:** Hardware abstraction layers (HALs) heavily use `void *` for DMA source/destination addresses. The hardware doesn't care about C types, only addresses and byte lengths.
*   **Harvard Architectures:** On some specialized DSPs/MCUs with distinct memory spaces (Program vs. Data memory), `void *` only represents data memory. Attempting to store a program memory address (like a function pointer or const flash string) in a `void *` may truncate the address.

## Firmware Review Angle
1.  **Check the Casts:** Is the `void *` being cast back to the exact type that originally created it? 
2.  **Look for GNU Extensions:** Flag any `void_ptr + offset` math. Enforce casting to `uint8_t *` or `char *` before doing byte-level arithmetic.
3.  **Check Lifetime/Scope:** If a pointer to a local (stack) variable is passed as a `void *` context to an asynchronous callback, ensure the variable outlives the callback execution.
4.  **Verify Alignment:** If an incoming generic buffer (e.g., UART receive payload) is cast from `void *` to a `struct *`, ensure the buffer originated from an appropriately aligned memory address.

## Compiler, ABI, and Toolchain Implications
*   **ABI:** `void *` is passed in standard pointer registers (e.g., `R0` on ARM AAPCS) just like any other pointer.
*   **Optimization Barrier:** Opaque callbacks (`void func(void *ctx)`) act as optimization barriers. The compiler cannot easily infer what `ctx` points to, forcing it to assume memory might have been mutated (aliasing), which prevents caching values in registers across the callback.
*   **LTO (Link Time Optimization):** LTO can sometimes trace `void *` types across compilation units, recovering some inlining and aliasing optimization that type-erasure normally destroys.

## Performance, Memory, Timing, and Power
*   **Execution Cost:** Casting to and from `void *` generates zero assembly instructions. It is purely a compile-time construct.
*   **Code Size:** Using generic `void *` functions (like one `qsort`) reduces ROM size compared to C++ template instantiation (which generates a new function copy for every type).
*   **Memory Cost:** No inherent overhead; a `void *` takes exactly the same RAM as any other data pointer (e.g., 4 bytes on a 32-bit system).

## Verification / Debugging
*   **Compiler Flags:** Use `-Wpointer-arith` to catch illegal void pointer math. Use `-Wcast-align` to detect unsafe alignment casts. Use `-Wdiscarded-qualifiers` to catch silent `const` stripping.
*   **Debugger Visibility:** A debugger (GDB) cannot expand or inspect a `void *` variable because it lacks type schema. You must explicitly cast it in the debugger (e.g., `print *(my_struct_t *)ctx`).
*   **Sanitizers:** Undefined Behavior Sanitizer (UBSan) will flag alignment faults and strict aliasing violations originating from unsafe `void *` conversions at runtime.

## Safety, Security, and Reliability
*   **MISRA C:2012:** Rule 11.5 severely restricts `void *`: *A conversion should not be performed from pointer to void into pointer to object.* MISRA strongly prefers type-safe unions, statically typed functions, or C11 `_Generic` macros over type erasure.
*   **Security:** Type confusion vulnerabilities occur when a system is tricked into casting a `void *` to the wrong struct type, allowing an attacker to overwrite adjacent memory or hijack control flow by manipulating mismatched struct offsets.

## Trade-offs and Alternatives
*   **Use `void *` when:** Designing agnostic data structures (linked lists, ring buffers), generic memory allocators, or RTOS task definitions where the underlying type truly does not matter to the subsystem.
*   **Avoid `void *` when:** You can solve the problem with standard type checking. 
*   **Alternatives:** 
    1. C11 `_Generic` for type-safe polymorphic macros.
    2. Tagged Unions (struct containing an `enum type` and a `union` of supported payloads).
    3. Dedicated typed functions (e.g., `list_add_int()` vs `list_add_void()`).

## Staff-Level Takeaway
Type erasure via `void *` trades compile-time safety for architectural flexibility. A Staff engineer should view `void *` as an encapsulation boundary. The subsystem accepting the `void *` must treat it strictly as an opaque token (store it, pass it, but never interpret it). The subsystem providing the `void *` assumes full liability for safely establishing the type contract. If a generic framework needs to interpret the payload, you don't need a `void *`—you need a common header interface (e.g., embedding a base struct inside the target struct, utilizing macro-based pseudo-inheritance).

## Related Concepts
*   [[00_Chapter_Index]]
*   [[01_Pointer_declarations]]
*   [[12_Function_pointers]]
*   [[Strict Aliasing and Effective Types]]
*   [[Memory Alignment and Padding]]
*   [[uintptr_t and intptr_t]]
*   [[Opaque Pointers (Pimpl Idiom in C)]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
