# 08: Typedef vs Macro

## Definition
Typedefs and `#define` macros can both create alias names for types, but they operate at fundamentally different stages of the compiler pipeline. A `#define` is a preprocessor lexical text replacement mechanism, whereas a `typedef` is a first-class language feature evaluated by the compiler's parser and Abstract Syntax Tree (AST) with strict scoping and typing rules.

## Scope and Boundaries
Covers: Preprocessor textual replacement vs AST parsing, multi-variable declarations, scope boundaries, qualifier binding, and debugger visibility.
Does not cover: Function-like macros or macro code generation metaprogramming.

## Why Does It Exist
Early C programmers often used `#define` for types before `typedef` was fully understood or standardized. While macros can substitute arbitrary tokens, they fail to respect C grammar rules, leading to catastrophic declaration bugs.

## Mechanism and Language Rules
1. **Pipeline Stage:** Macros are expanded during preprocessing (translation phase 4). Typedefs are parsed during syntactic and semantic analysis (translation phase 7).
2. **Grammar and Multi-Declarations:**
   ```c
   #define int_ptr_m int *
   typedef int *int_ptr_t;

   int_ptr_m a, b; /* Lexical expansion: int * a, b; -> 'a' is int*, 'b' is plain int! */
   int_ptr_t c, d; /* AST type binding: Both 'c' and 'd' are int* */
   ```
3. **Scope Control:** Macros ignore lexical blocks and functions; they pollute the global namespace from their declaration point until `#undef`. Typedefs obey standard C block scoping.
4. **Qualifier Association:** `const` binds correctly to the entire type node in a `typedef`, but textually associates with the leftmost token in a macro.

## Examples
```c
#include <stdint.h>
#include <assert.h>

/* The Multi-Variable Declaration Trap */
#define UINT32_PTR_MACRO   uint32_t*
typedef uint32_t*          uint32_ptr_type;

static void demonstrate_macro_hazard(void) {
    UINT32_PTR_MACRO p1, p2; 
    /* Expands to: uint32_t* p1, p2; */
    /* p1 is a pointer to uint32_t (4 or 8 bytes) */
    /* p2 is a PLAIN uint32_t integer (4 bytes)! */

    uint32_ptr_type p3, p4;
    /* p3 is a pointer to uint32_t */
    /* p4 is a pointer to uint32_t */

    static_assert(sizeof(p1) == sizeof(void*), "p1 must be a pointer");
    static_assert(sizeof(p2) == sizeof(uint32_t), "p2 is unexpectedly a scalar int!");
    static_assert(sizeof(p3) == sizeof(void*), "p3 is a pointer");
    static_assert(sizeof(p4) == sizeof(void*), "p4 is a pointer");
}

/* Scoping Demonstration */
static void scope_demonstration(void) {
    {
        typedef uint16_t local_type_t;
        #define LOCAL_MACRO uint16_t
    }
    // local_type_t var1; /* COMPILATION ERROR: local_type_t is out of scope */
    LOCAL_MACRO  var2; /* SUCCEEDS: Macros leak out of local scopes! */
    (void)var2;
}
#undef LOCAL_MACRO /* Required to clean up macro pollution */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Redefining an existing typedef name with a macro causes parser errors.
- Macros that redefine fundamental keywords (e.g., `#define int long`) invoke Undefined Behavior (§7.1.2).

## Edge Cases and Failure Modes
- **Macro Side Effects in Types:** Defining complex types via macros can break when combined with storage classes or attributes:
  `#define HANDLE void*` -> `unsigned HANDLE x; /* Syntax error */`.
- **Debugging Symbol Loss:** Preprocessor macros are discarded before symbol generation; debuggers cannot inspect macro names unless compiled with `-g3`. Typedefs are preserved in DWARF debug symbols.

## Embedded Implications
- **Namespace Collision in Vendor SDKs:** Large embedded codebases integrating multiple vendor stacks frequently break when vendors define types using `#define` instead of `typedef`, causing unresolvable token collisions.

## Firmware Review Angle
- Ban all type aliasing via `#define`. Enforce `typedef` across the entire codebase.
- Search for legacy preprocessor patterns: `#define BYTE uint8_t` and replace with `typedef uint8_t byte_t;`.

## Compiler, ABI, and Toolchain Implications
- Typedefs provide clean AST tokens, allowing compilers to output precise warning messages with exact type names. Macros produce error messages pointing to expanded tokens, confusing developers.

## Performance, Memory, Timing, and Power
- Zero difference in generated machine code.

## Verification / Debugging
- Compile with `-Wextra`. In GDB, `whatis` and `ptype` resolve typedefs cleanly, whereas macros require preprocessor macro expansion tables.

## Safety, Security, and Reliability
- MISRA C:2012 Directive 4.9: A function should be used in preference to a function-like macro where they are interchangeable.
- Using `typedef` prevents silent type degradation (like the `p1, p2` pointer/scalar bug).

## Trade-offs and Alternatives
- Macros can accept arguments (templates/generics simulation), which standard C typedefs cannot. If parameterized types are needed, use code-generation scripts or carefully audited token macros.

## Staff-Level Takeaway
Never use `#define` for type aliasing. Macros are blunt textual substitution tools that violate C's scoping rules, break multi-variable declarations, and vanish from debug symbols. Always use `typedef` for type abstraction.

## Related Concepts
- `01_Basic_typedefs`
- `05_Pointer_typedefs`
- `07_Qualified_typedefs`
