# 08: Include Guards

## Definition
Include guards are conditional preprocessor directives placed around the entire contents of a header file to prevent it from being included and parsed multiple times within the same translation unit. They ensure header idempotency and eliminate duplicate type definition errors.

## Scope and Boundaries
Covers: Classical `#ifndef` guards, `#pragma once`, Multiple-Include Optimization (MIOpt), and guard symbol collision risks.
Does not cover: Linker duplicate symbol resolution (`extern`, inline functions, `weak`).

## Why Does It Exist
In large C architectures, header dependency graphs are complex and interconnected (e.g., both `uart.h` and `timer.h` include `common_types.h`). Without include guards, `common_types.h` would be parsed twice in the same `.c` file, causing compiler redefinition errors for structs, enums, and typedefs.

## Mechanism and Language Rules
1. **Classical Guard Idiom:**
   ```c
   #ifndef MODULE_NAME_H
   #define MODULE_NAME_H
   /* Header contents */
   #endif /* MODULE_NAME_H */
   ```
2. **Multiple-Include Optimization (MIOpt):** Modern compilers (GCC, Clang, MSVC) recognize the classical guard structure. If no tokens exist outside the guard, the preprocessor records the guard macro. On subsequent `#include` attempts, the compiler skips opening and reading the file from the disk entirely.
3. **`#pragma once`:** A non-standard but universally supported compiler directive that instructs the preprocessor to include the file only once per translation unit.

## Examples
```c
/* ================= File: hal_gpio.h ================= */
/* Classical ISO C Guard with strict enterprise namespacing */
#ifndef PROJECT_DRIVERS_HAL_GPIO_H
#define PROJECT_DRIVERS_HAL_GPIO_H

#include <stdint.h>
#include <stdbool.h>

typedef struct {
    uint8_t pin_number;
    bool    is_output;
} GpioConfig_t;

void gpio_init(const GpioConfig_t *config);

#endif /* PROJECT_DRIVERS_HAL_GPIO_H */

/* ================= Modern Pragmatic Alternative ================= */
#pragma once

#include <stdint.h>
/* Rest of header */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **`#pragma once` Standard Status:** `#pragma once` is not defined by the ISO C standard; its behavior is implementation-defined. However, it is supported by GCC, Clang, MSVC, IAR, Keil, and Arm Compiler.
- **Filesystem Identity Issues with `#pragma once`:** If a file is accessed via hard links, symbolic links, or case-insensitive filesystems under differing paths, `#pragma once` may fail to recognize it as the same physical file and include it twice.

## Edge Cases and Failure Modes
- **Guard Name Collisions:** If two different files accidentally use the same guard identifier (e.g., both use `#ifndef CONFIG_H`), the second file included will be silently and completely skipped, leading to bizarre "type missing" compiler errors.
- **Tokens Outside the Guard:** Placing even a single comment or semicolon outside the `#ifndef` / `#endif` block can disable compiler Multiple-Include Optimization (MIOpt), forcing the preprocessor to re-open and re-parse the file repeatedly.

## Embedded Implications
- **Build Performance:** In large embedded firmware repositories containing thousands of headers, properly optimized include guards reduce full rebuild times by 30% to 50% by avoiding disk I/O and preprocessor parsing overhead.

## Firmware Review Angle
- Confirm guard macro names follow a deterministic, hierarchical pattern: `PROJECT_SUBSYSTEM_FILENAME_H`.
- Ensure no code or comments precede `#ifndef` or follow `#endif` to guarantee MIOpt activation.
- Verify `#endif` includes a descriptive trailing comment identifying the guard macro.

## Compiler, ABI, and Toolchain Implications
- GCC and Clang will emit diagnostic warnings if an included file has unclosed `#ifndef` guards.

## Performance, Memory, Timing, and Power
- Include guards optimize compilation wall-clock time; they have zero effect on the generated binary image.

## Verification / Debugging
- Use compiler flag `-H` to inspect header inclusions. If a guarded file is repeatedly traversed without being skipped, check if tokens exist outside the guard.

## Safety, Security, and Reliability
- MISRA C:2012 Directive 4.10: Precautions shall be taken in order to prevent the contents of a header file being included more than once. (Both classical `#ifndef` guards and `#pragma once` can satisfy this with appropriate tooling approval).

## Trade-offs and Alternatives
- **Classical `#ifndef` vs. `#pragma once`:**
  - Classical `#ifndef` is 100% standard-compliant and immune to symlink issues, but requires verbose boilerplate and risks identifier collisions.
  - `#pragma once` eliminates naming collisions and boilerplate, but is non-standard.
  - *Best Practice:* Many teams use both together: `#pragma once` immediately followed by standard `#ifndef` guards.

## Staff-Level Takeaway
Never permit unguarded headers. Prefix classical guard identifiers with the complete module path to prevent naming collisions (`SUBSYS_DRIVER_NAME_H`), keep the guard around the exact first and last lines of the file to preserve MIOpt caching, and safely pair with `#pragma once` for modern toolchains.

## Related Concepts
- `01_File_inclusion`
- `03_Conditional_inclusion`
- `09_Pragma`
