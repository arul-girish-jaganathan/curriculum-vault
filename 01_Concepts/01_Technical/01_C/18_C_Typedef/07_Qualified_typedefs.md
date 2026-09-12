# 07: Qualified Typedefs

## Definition
Qualified typedefs involve the interaction between type qualifiers (`const`, `volatile`, `restrict`) and `typedef` specifiers. Because C builds types structurally through its Abstract Syntax Tree (AST), applying a qualifier to a typedef alias modifies the aggregate type as a whole rather than simply prepending textual tokens, leading to significant semantic divergence from naive macro substitutions.

## Scope and Boundaries
Covers: Top-level vs. low-level `const`, `volatile` qualification on typedefs, qualifier stripping traps, and AST qualification rules.
Does not cover: Qualifier rules in C++ or standard variable storage classes.

## Why Does It Exist
Qualifiers indicate access permissions and hardware mutability. Applying qualifiers to typedefs allows systems engineers to define immutable types, read-only hardware registers, or memory-barrier-sensitive hardware ports.

## Mechanism and Language Rules
1. **AST-Level Qualification:** Qualifiers applied to a typedef alias modify the outermost type node in the AST.
2. **Top-Level Pointer Constness:**
   ```c
   typedef int *int_ptr;
   typedef const int_ptr c_int_ptr; /* Result: int * const (top-level const) */
   ```
   The pointer is `const`, but the data pointed to remains completely mutable.
3. **Volatile Propagation:**
   ```c
   typedef uint32_t reg32_t;
   typedef volatile reg32_t vreg32_t; /* Guaranteed volatile unsigned 32-bit int */
   ```
4. **Idempotent Qualifiers (C99+):** Applying the same qualifier multiple times (e.g., `const const_int_t x`) is benign and permitted by ISO C99 §6.7.3.

## Examples
```c
#include <stdint.h>
#include <assert.h>

/* Qualified hardware MMIO register type */
typedef volatile uint32_t vreg32_t;

/* Volatile pointer to volatile register */
typedef vreg32_t *vreg_ptr_t;

static void mmio_write(vreg32_t *reg, uint32_t val) {
    /* Compiler is strictly forbidden from optimizing away this write */
    *reg = val; 
}

/* The Const Pointer Mutation Paradox */
typedef uint8_t *byte_ptr;

static void test_qualification(void) {
    uint8_t data[2] = {0x10, 0x20};
    
    /* Top-level const: pointer is locked, buffer is WRITABLE */
    const byte_ptr p = data; 
    
    *p = 0xFF;        /* Completely legal! data[0] is now 0xFF */
    // p = &data[1];  /* COMPILATION ERROR: p itself is read-only */
    
    assert(data[0] == 0xFF);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Attempting to cast away `const` or `volatile` qualifiers from an object originally defined with them and mutating it invokes Undefined Behavior.

## Edge Cases and Failure Modes
- **Accidental Pointer Constness:** A developer creates `typedef char *str_t;` and uses `const str_t` in an API, intending to promise that the API will not modify the caller's string buffer. In reality, the buffer is left unprotected, creating silent mutation bugs.
- **Volatile Array Decay:** Qualifying an array typedef with `volatile` creates an array of volatile elements; upon decay, it becomes a pointer to a volatile type.

## Embedded Implications
- **Hardware Register Mapping:** Drivers must strictly qualify MMIO structures and typedefs with `volatile` (`typedef volatile uint32_t io_reg_t;`). If `volatile` is omitted, the compiler optimizer will eliminate polling loops and cache hardware reads in registers.
- **Placing Constants in Flash:** Misunderstanding top-level `const` on pointer typedefs can result in variables being allocated in SRAM instead of Flash/ROM.

## Firmware Review Angle
- Audit any typedef containing pre-applied `const` or `volatile` qualifiers: are downstream users aware that the qualifier is baked in?
- Prefer applying qualifiers explicitly at variable declaration sites (`const T *`) rather than baking qualifiers into the typedef itself.

## Compiler, ABI, and Toolchain Implications
- `volatile` prevents compilers from reordering memory accesses across sequence points and forbids instruction merging.

## Performance, Memory, Timing, and Power
- Overuse of `volatile` typedefs on regular variables prevents CPU register caching and forces redundant memory bus cycles, degrading execution speed and increasing power consumption.

## Verification / Debugging
- Compiler flag `-Wcast-qual` warns whenever a cast removes a type qualifier from a pointer.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 11.8: A conversion shall not remove any `const` or `volatile` qualification from the type pointed to by a pointer.

## Trade-offs and Alternatives
- **Baking Qualifiers vs. Explicit Qualification:** Baking `volatile` into register types (`vreg32_t`) enforces safety across peripheral drivers. Baking `const` into pointer typedefs causes developer confusion and should be avoided.

## Staff-Level Takeaway
Never hide low-level `const` behind a pointer typedef. Qualifiers applied to typedefs always apply to the topmost type. Reserve qualified typedefs for explicit architectural hardware types like `vreg32_t`, and keep pointer qualifications visible at function call boundaries.

## Related Concepts
- `01_Basic_typedefs`
- `05_Pointer_typedefs`
- `08_Typedef_vs_macro`
