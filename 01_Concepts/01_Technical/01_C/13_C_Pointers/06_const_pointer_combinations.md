# 06: Const Pointer Combinations

## Definition
A `const` pointer combination is the syntactic pairing of the `const` type qualifier with a pointer declarator to enforce immutability on either the pointed-to object, the pointer object itself, or both. In ISO C (C99 §6.7.3), `const` specifies that an lvalue designating the qualified object cannot be used to modify that object.

## Scope and Boundaries
*   **Covers:** The four canonical combinations of `const` and pointers, left-associative parsing semantics, qualifier qualification conversions, and `const` casting rules.
*   **Does not cover:** `volatile` and `restrict` pointer combinations (see [[Type Qualifiers]]), storage in read-only memory/linker sections (see [[Linker Scripts and Memory Sections]]), or string literal storage duration (see [[Storage Duration and Lifetime]]).

## Why Does It Exist
Pointer indirection creates two distinct entities in memory: the address holder (the pointer object) and the address target (the pointee object). `const` pointer combinations exist to:
*   **Establish API Contracts:** Distinguish pure read-only input buffers from mutable output/inout buffers at compile time.
*   **Hardware Register Safety:** Pin down pointer addresses for memory-mapped I/O peripherals so software cannot inadvertently redirect register base pointers.
*   **Optimization Enablement:** Signal immutability to the compiler to allow register caching and common subexpression elimination.

## Mechanism and Language Rules
1.  **The Four Combinations:**
    *   `int *p;`: Mutable pointer to mutable data. Both `p` and `*p` can be reassigned.
    *   `const int *p;` (or `int const *p;`): Mutable pointer to `const` data. `p` can change, `*p` cannot.
    *   `int * const p;`: `const` pointer to mutable data. `*p` can change, `p` cannot.
    *   `const int * const p;` (or `int const * const p;`): `const` pointer to `const` data. Neither `p` nor `*p` can change.
2.  **Clockwise/Right-to-Left Rule:** Read from right to left starting at the identifier: `const int * const p` -> `p` is a `const` pointer (`* const`) to `int` which is `const`.
3.  **Qualification Conversions:** A pointer to an unqualified type can be implicitly converted to a pointer to a `const`-qualified type. The reverse conversion requires an explicit cast and violates language constraints if assigned directly.
4.  **Modification Constraints:** Any attempt to modify an object through a `const`-qualified lvalue is a compile-time constraint violation requiring a diagnostic message.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>

static void example_combos(int *src, int *dst)
{
    int val = 10;

    /* 1. Pointer to const: read-only input buffer pattern */
    const int *read_ptr = src;
    read_ptr = &val;       /* Allowed: pointer itself is mutable */
    /* *read_ptr = 20; */  /* Error: assignment of read-only location */

    /* 2. Const pointer: fixed hardware address pattern */
    int * const fixed_ptr = dst;
    *fixed_ptr = 30;       /* Allowed: target is mutable */
    /* fixed_ptr = &val; *//* Error: assignment of read-only variable */

    /* 3. Const pointer to const: immutable lookup anchor */
    const int * const locked = src;
    (void)locked;
}

/* Incorrect: Implicit qualifier discard (Constraint Violation) */
static void invalid_discard(const int *c_ptr)
{
    /* int *mutable_ptr = c_ptr; */ /* Warning/Error: assignment discards 'const' */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Modifying an object originally declared with a `const`-qualified type by casting away its `const` qualifier (e.g., `const int a = 1; *(int *)&a = 2;`). If the object was allocated in Flash/ROM, this also triggers a hardware bus fault.
*   **Constraint Violation:** Assigning a `const`-qualified pointer to an unqualified pointer without an explicit cast.
*   **Implementation-Defined:** Whether casting away `const` and writing to an object that was not originally declared `const` succeeds or faults based on memory mapping and platform MMU/MPU settings.

## Edge Cases and Failure Modes
*   **Casting Away Const:** Using an explicit cast `(int *)c_ptr` silences compiler warnings but invokes undefined behavior at runtime if `c_ptr` addresses an object allocated in read-only storage (`.rodata`).
*   **Multi-Level Pointer Constness:** `const int **p2` cannot safely receive an `int **` implicitly. In C (unlike C++ with qualified conversions), converting `int **` to `const int **` is an implicit conversion constraint violation because it would allow downstream code to indirectly assign the address of a `const` object to a mutable pointer without a cast.
*   **Typedef Obfuscation:** In `typedef int *int_ptr; const int_ptr p;`, `p` is an `int * const` (const pointer to int), NOT a `const int *`.

## Embedded Implications
*   **Flash vs. RAM Placement:** An object declared `const int x = 5;` resides in `.rodata` (Flash). Passing its address as a `const int *` to a driver is completely valid. If the driver erroneously casts away `const` to write to it, an MPU/BusFault occurs because Flash cannot be written via standard store instructions.
*   **Peripheral Registers:** Hardware peripheral base addresses should be declared as `const` pointers to `volatile` registers:
    ```c
    #define USART1 ((volatile USART_TypeDef * const)0x40013800UL)
    ```
    This prevents code from accidentally rebinding `USART1 = NULL;` while ensuring volatile hardware reads/writes occur.

## Firmware Review Angle
1.  **Defensive API Parameters:** Verify that all pointer parameters meant strictly for reading data are declared as `const Type *` (e.g., `buffer`, `length`).
2.  **Cast Inspection:** Heavily scrutinize any explicit cast that removes a `const` qualifier (`(Type *)ptr`). This is a code smell and often masks safety violations.
3.  **Peripheral Base Addresses:** Ensure all MMIO register mappings feature the `* const` declarator to lock the peripheral base address.

## Compiler, ABI, and Toolchain Implications
*   **Register Caching:** Knowing a pointer points to `const` data allows the compiler's optimizer to hold pointee values in registers across loops without reloading from RAM, assuming no aliasing with mutable pointers.
*   **Diagnostics:** Compilers provide `-Wcast-qual` and `-Wdiscarded-qualifiers` to trap accidental or explicit loss of `const` integrity.
*   **ABI:** Qualifiers do not affect calling conventions or register allocation. `const int *` passes identically to `int *`.

## Performance, Memory, Timing, and Power
*   **Zero Runtime Overhead:** Constness is strictly a compile-time invariant; it generates no runtime instructions or memory footprint for the qualifier itself.
*   **Code Optimization:** Enables aggressive dead code elimination, constant propagation, and loop invariant code motion by the compiler backend.
*   **Memory Savings:** Pointers to `const` data allow shared lookup tables and strings to reside in read-only Flash, preserving precious SRAM on MCUs.

## Verification / Debugging
*   **Compiler Flags:** Enforce `-Werror=discarded-qualifiers` and `-Wcast-qual`.
*   **Static Analysis:** Tools like MISRA checkers and Clang Static Analyzer will flag any assignment that strips const qualification.
*   **GDB Inspection:** Inspecting a const object (`ptype p`) verifies type qualification. Memory write attempts in GDB can trigger target hardware write faults if backed by Flash.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 8.13:* A pointer parameter should point to `const` if the referenced object is not modified.
    *   *Rule 11.8:* A cast shall not remove any `const` or `volatile` qualification.
*   **Security Impact:** Prevents buffer corruption bugs where utility routines (e.g., `crc16_calc(const uint8_t *data, size_t len)`) accidentally mutate sensitive payload data.

## Trade-offs and Alternatives
*   **Strict Const-Correctness vs. Ergonomics:** Retrofitting `const` into an existing non-const codebase triggers cascading compiler warnings across call graphs. However, enforcing const-correctness upfront provides bulletproof compile-time interface safety.

## Staff-Level Takeaway
`const` is an API design and structural contract tool. Staff engineers must mandate const-correct interfaces across all library boundaries: if a function does not mutate an input buffer, that buffer must be `const *`. Never permit casting away `const` to bypass interface constraints—fix the upstream API instead.

## Related Concepts
*   [[01_Pointer_declarations]]
*   [[02_Pointer_initialization]]
*   [[Storage Duration and Lifetime]]
*   [[Type Qualifiers]]
*   [[Linker Scripts and Memory Sections]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
