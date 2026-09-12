# 10: Macro Namespaces

## Definition
Macro namespacing is the organizational discipline of prefixing macro identifiers with unique module, subsystem, or project identifiers. Because the C preprocessor has a single global namespace with zero scoping boundaries, strict naming conventions are the only defense against silent identifier collisions.

## Scope and Boundaries
Covers: Prefix conventions, uppercase identifier standards, collision prevention in vendor SDKs, macro pollution, and `#undef` hygiene.
Does not cover: C++ namespaces or linker symbol visibility (`static`).

## Why Does It Exist
The C preprocessor does not respect C language scopes (blocks, functions, structs, or files). A macro defined in any included header exists globally across all subsequent code in that translation unit. Without disciplined namespacing, generic names like `MAX`, `BUFFER_SIZE`, `ENABLE`, or `STATUS` collide and corrupt code silently.

## Mechanism and Language Rules
1. **Unified Global Scope:** Every macro defined with `#define` occupies the preprocessor namespace globally from its point of declaration until the end of the translation unit, unless explicitly `#undef`'d.
2. **Uppercase Convention:** By universal convention, macro names are written in ALL_CAPS to provide visual notification to developers that the identifier is subject to lexical preprocessor replacement.
3. **Prefix Hierarchy:** Standard enterprise practice dictates a structured prefix:
   `[PROJECT]_[SUBSYSTEM]_[MODULE]_[NAME]`

## Examples
```c
#include <stdint.h>

/* ANTI-PATTERN: Generic, un-prefixed macros polluting global scope */
#define BUFFER_SIZE     128
#define TIMEOUT         1000
#define SET_FLAG(x)     ((x) = 1)

/* ROBUST PATTERN: Hierarchical namespacing */
#define DRV_UART_BUFFER_SIZE_BYTES  (128U)
#define DRV_UART_TIMEOUT_MS         (1000U)
#define DRV_UART_SET_FLAG(reg, bit) ((reg) |= (1UL << (bit)))

/* Scoped private macro pattern (cleaned up after use) */
#define LOCAL_CALC(x)               (((x) * 3U) + 1U)

static uint32_t process_data(uint32_t val) {
    return LOCAL_CALC(val);
}

#undef LOCAL_CALC /* Prevents macro leaking into downstream code */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Defining a macro with the same name as a standard C keyword (e.g., `#define inline ...`) invokes Undefined Behavior (§7.1.2).
- Defining a macro starting with an underscore followed by an uppercase letter (e.g., `_DEBUG`) enters reserved implementation namespace territory.

## Edge Cases and Failure Modes
- **Struct Member Hijacking:**
  ```c
  #define status 1 /* Macro declared in a low-level header */
  
  struct Device {
      int status; /* Expands to: int 1; -> Bizarre compiler syntax error! */
  };
  ```
  Because macros are type-blind, lowercase macros frequently hijack struct member names and local variables.
- **Vendor SDK Clashes:** Merging two third-party stacks (e.g., FreeRTOS and a vendor BLE stack) frequently fails because both define conflicting versions of un-prefixed macros like `MIN` or `ALIGN`.

## Embedded Implications
- **Header Pollution in Large Codebases:** A monolithic `#include "all.h"` that introduces thousands of un-prefixed macros can silently alter code behavior in unrelated driver modules.

## Firmware Review Angle
- Strictly reject any macro that is not written in `ALL_CAPS` (with rare exceptions for architectural shims).
- Reject any public macro in a header file that lacks a distinct module prefix (e.g., `HAL_`, `OS_`, `NET_`).
- Ensure private helper macros defined in `.c` files are cleaned up with `#undef` at the end of the file.

## Compiler, ABI, and Toolchain Implications
- Macro names do not exist in ELF object symbol tables; they cannot be resolved or protected by linker visibility rules.

## Performance, Memory, Timing, and Power
- Namespacing is a compile-time naming convention with zero runtime or memory impact.

## Verification / Debugging
- Compiler flag `-Wreserved-id-macro` warns if macros collide with standard system reservations.
- Use `clang-tidy` (`readability-identifier-naming`) to enforce uppercase and prefix rules automatically in CI.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 5.6: A `typedef` name shall be a unique identifier (applies equally by extension to macro namespace hygiene).
- MISRA C:2012 Rule 20.5: `#undef` should not be used in safety-critical code without architectural justification (to prevent confusing re-definitions).

## Trade-offs and Alternatives
- **Verbose Prefixes vs Concise Code:** Prefixed macros (`DRV_SPI_TIMEOUT_MS`) are longer to type than `TIMEOUT`, but completely eliminate name collisions across multi-million-line firmware codebases.

## Staff-Level Takeaway
Treat the preprocessor namespace as a shared global resource. Never define a public macro without a strict module prefix, enforce `ALL_CAPS` naming, and never allow lowercase macros that could hijack struct members or standard C keywords.

## Related Concepts
- `01_Object_like_macros`
- `02_Function_like_macros`
- `19_C_Preprocessor/12_Preprocessor_architecture`
