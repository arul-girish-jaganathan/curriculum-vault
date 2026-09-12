# 03: Include Guards

## Definition
Include guards are conditional preprocessor directives wrapping the contents of a header file to ensure its declarations are parsed at most once within any single translation unit. This maintains header idempotency and prevents compiler redeclaration errors.

## Scope and Boundaries
Covers: Standard `#ifndef` guards, `#pragma once`, Multiple-Include Optimization (MIOpt), and collision prevention.
Does not cover: Linker symbol resolution (see `05_Definition_ownership`).

## Why Does It Exist
Because headers include other headers in complex dependency trees, a shared header (like `stdint.h` or `error_codes.h`) is inevitably encountered multiple times while compiling a single `.c` file. Without include guards, redefinition of typedefs, structs, and enums causes compilation failure.

## Mechanism and Language Rules
1. **Classical Guard Idiom:**
   ```c
   #ifndef NAMESPACE_SUBSYSTEM_HEADER_H
   #define NAMESPACE_SUBSYSTEM_HEADER_H
   /* Declarations */
   #endif /* NAMESPACE_SUBSYSTEM_HEADER_H */
   ```
2. **Multiple-Include Optimization (MIOpt):** Compilers record headers that have no code outside the `#ifndef` wrapper and bypass re-opening the physical file on subsequent `#include` directives.
3. **`#pragma once`:** Supported by virtually all modern C compilers (GCC, Clang, IAR, Arm Compiler 6), it provides identical functionality with lower boilerplate.

## Examples
```c
/* ================= File: drv_sensor_types.h ================= */
#ifndef DRV_SENSOR_TYPES_H
#define DRV_SENSOR_TYPES_H

#include <stdint.h>

typedef struct {
    int16_t x;
    int16_t y;
    int16_t z;
} AccelRawData_t;

#endif /* DRV_SENSOR_TYPES_H */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- `#pragma once` is implementation-defined by ISO C, though universally supported in production embedded compilers.

## Edge Cases and Failure Modes
- **Macro Name Collisions:** Using generic guard names (`#ifndef SENSOR_H`) across different directories leads to silent suppression of the second header, resulting in missing types.
- **Tokens Outside Guard:** Comments or whitespace outside the `#ifndef` block are fine, but stray code tokens disable compiler MIOpt optimizations.

## Embedded Implications
- In large firmware projects with thousands of source files, MIOpt-compliant guards reduce compilation times by up to 40% on build servers.

## Firmware Review Angle
- Confirm guard macro names include full subsystem prefixes (`PROJECT_SUBSYS_MODULE_H`).
- Reject any header lacking include guards or `#pragma once`.

## Compiler, ABI, and Toolchain Implications
- Both `#ifndef` guards and `#pragma once` are resolved entirely in Translation Phase 4; they produce zero object code.

## Performance, Memory, Timing, and Power
- Zero runtime footprint. Reduces developer build-and-test cycle times.

## Verification / Debugging
- Use `gcc -H` to verify headers are not redundantly re-parsed.

## Safety, Security, and Reliability
- MISRA C:2012 Directive 4.10: Precautions shall be taken in order to prevent the contents of a header file being included more than once.

## Trade-offs and Alternatives
- **Guard Macros vs `#pragma once`:** Modern practice recommends `#pragma once` followed by standard `#ifndef` guards for guaranteed cross-toolchain portability.

## Staff-Level Takeaway
Never write a header without idempotency protection. Use standardized, fully qualified guard macros to prevent collisions and keep build-time compilation overhead minimal.

## Related Concepts
- `01_Public_headers`
- `07_Header_self_sufficiency`
- `09_Circular_include_avoidance`
