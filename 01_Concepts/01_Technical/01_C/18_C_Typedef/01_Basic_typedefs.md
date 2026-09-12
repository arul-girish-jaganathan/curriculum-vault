# 01: Basic Typedefs

## Definition
A basic `typedef` defines a new identifier as an alias for an existing primitive scalar type (integers, floating-point numbers, or characters). Syntactically, it is declared identically to a standard variable declaration prefixed by the `typedef` storage class specifier, where the identifier becomes the alias rather than a storage instance.

## Scope and Boundaries
Covers: Scalar aliasing syntax, fixed-width abstraction, ordinary identifier scope, and type equivalence.
Does not cover: Aggregate structs/unions (see `02_Struct_typedefs`) or pointer aliasing (see `05_Pointer_typedefs`).

## Why Does It Exist
C's primitive integer types (`short`, `int`, `long`, `long long`) have platform-dependent sizes. On a 16-bit DSP, `int` is 16 bits; on a 32-bit ARM Cortex-M, `int` is 32 bits; on a 64-bit Linux kernel, `long` is 64 bits, while on 64-bit Windows it is 32 bits. Basic typedefs allow programs to abstract native machine representations into guaranteed semantic widths (`uint32_t`, `size_t`, `intptr_t`).

## Mechanism and Language Rules
1. **Type Equivalence:** A `typedef` does NOT create a distinct, strongly checked type. An alias is completely interchangeable with its underlying type. `typedef int my_int;` produces a type that the compiler treats identically to `int`.
2. **Storage Class Specifier:** Syntactically, ISO C classifies `typedef` as a storage-class specifier (alongside `extern`, `static`, `auto`, `register`). Consequently, `typedef` cannot be combined with other storage classes (e.g., `static typedef int my_int;` is illegal).
3. **Scoping Rules:** Typedef names inhabit the ordinary identifier namespace (the same namespace as variables and functions). A typedef can be shadowed in inner block scopes.

## Examples
```c
#include <stdint.h>
#include <assert.h>

/* Portable hardware register width aliases */
typedef uint32_t reg32_t;
typedef uint16_t reg16_t;

/* Domain-specific unit aliases */
typedef uint32_t millivolts_t;
typedef uint32_t milliamps_t;

static void monitor_power(millivolts_t v, milliamps_t i) {
    /* No strong type checking: compiler allows mixing without error */
    millivolts_t sum = v + i; /* Valid C, though semantically questionable */
    (void)sum;
}

static void test_equivalence(void) {
    reg32_t reg = 0xA5A5A5A5u;
    uint32_t *ptr = &reg; /* Completely legal: identical type identity */
    assert(*ptr == 0xA5A5A5A5u);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Shadowing in Inner Scope:** Re-declaring a typedef name as a local variable in an inner block is valid ISO C, but masks the type alias, leading to severe code confusion.
- **Redefinition Rules:** Prior to C11, re-typedefing the same name to the same type in the same scope was an error. ISO C11 (§6.7) explicitly permits benign typedef redefinitions to the exact same type.

## Edge Cases and Failure Modes
- **Lack of Strong Typing:** Developers often mistakenly believe `typedef millivolts_t` prevents accidentally passing a `milliamps_t` value. The C compiler treats both as `uint32_t` and performs no domain validation.
- **Inner Scope Shadowing Trap:**
  ```c
  typedef uint32_t status_t;
  void func(void) {
      int status_t = 5; /* Valid C: shadows the type name! */
      // status_t x = 10; /* Compilation error: status_t is now a variable */
  }
  ```

## Embedded Implications
- **Cross-Architecture Hardware Mapping:** Fixed-width integer typedefs (`<stdint.h>`) are essential for portable device drivers. Driver headers must use `uint32_t` or explicit register typedefs (`reg32_t`) rather than raw `int` or `long`.

## Firmware Review Angle
- Verify that bare primitive integer types (`short`, `int`, `long`) are replaced with `<stdint.h>` types in all hardware, driver, and interface code.
- Check that typedef names do not collide with or shadow existing type aliases in global scopes.

## Compiler, ABI, and Toolchain Implications
- Typedef aliases do not alter code generation, instruction selection, or register allocation. The compiler's front-end immediately resolves the alias to its underlying type during AST creation.

## Performance, Memory, Timing, and Power
- Zero runtime, memory, timing, or power overhead. Typedef resolution occurs entirely at compile-time.

## Verification / Debugging
- Debuggers (GDB/LLDB) preserve typedef names in DWARF debug symbols: `ptype reg` will report `type = unsigned int` or `type = reg32_t` depending on symbol output options.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 8.1: Types shall be explicitly specified.
- MISRA C:2012 Rule 5.6: A `typedef` name shall be a unique identifier.

## Trade-offs and Alternatives
- **Typedef vs. Struct Wrapping:** If true strong type checking is required (e.g., preventing voltage from adding to current), wrap the scalar inside a single-member `struct`: `typedef struct { uint32_t raw; } millivolts_t;`.

## Staff-Level Takeaway
Basic typedefs establish platform independence and semantic clarity, but provide zero type safety or domain checking. Rely on standard `<stdint.h>` types for storage guarantees, and consider struct-wrapped types when the architecture demands compile-time type enforcement.

## Related Concepts
- `08_Typedef_vs_macro`
- `09_Readable_API_typedefs`
- `10_MISRA_oriented_typedef_usage`
