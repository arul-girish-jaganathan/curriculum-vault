# 01: File Inclusion

## Definition
File inclusion (`#include`) instructs the preprocessor to suspend processing of the current translation unit, locate the specified file, and textually splice its entire contents into the translation stream at the directive's location. ISO C categorizes inclusions into quoted form (`"..."`) and angle-bracket form (`<...>`).

## Scope and Boundaries
Covers: Quoted vs angle-bracket search semantics, include path resolution order (`-I`, `-iquote`, `-isystem`), circular inclusion prevention, and include depth limits.
Does not cover: Header guards (see `08_Include_guards`) or module systems (C++20 modules).

## Why Does It Exist
C separates interface declarations from implementation definitions across distinct compilation units. The `#include` mechanism allows source files to import shared API prototypes, data structures, register definitions, and constants without code duplication.

## Mechanism and Language Rules
1. **Quoted Syntax (`#include "file"`):** The preprocessor searches first in the directory of the currently active source/header file. If not found, it falls back to the system include directories.
2. **Angle-Bracket Syntax (`#include <file>`):** The preprocessor skips the current file directory and searches system/toolchain include paths and paths added via compiler `-I` flags.
3. **Macro Inclusion:** A macro that expands to a valid `<...>` or `"..."` string can be used as the operand of an `#include` directive (Computed Includes).
4. **Translation Phase 4:** Header inclusion occurs strictly in Phase 4 of translation, before any semantic token parsing or type evaluation.

## Examples
```c
/* Standard library / Toolchain headers */
#include <stdint.h>
#include <stdbool.h>

/* Project-local and driver interfaces */
#include "hal_gpio.h"
#include "board_config.h"

/* Computed include (Architectural HAL abstraction pattern) */
#if defined(PLATFORM_STM32F4)
  #define PLATFORM_HEADER "arch/stm32f4/soc.h"
#elif defined(PLATFORM_NRF52)
  #define PLATFORM_HEADER "arch/nrf52/soc.h"
#else
  #error "Target platform undefined!"
#endif

#include PLATFORM_HEADER
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Path Search Order:** The exact order in which directories are traversed for `<...>` and `"..."` is implementation-defined.
- **Directory Separator:** Standard C uses `/` for portability. Windows backslashes `\` in include directives produce implementation-defined behavior.

## Edge Cases and Failure Modes
- **Shadowing System Headers:** Placing a local file named `string.h` or `math.h` in the search path causes `#include <string.h>` to resolve to the local file, hijacking standard library calls.
- **Include Depth Overflow:** Deeply nested circular includes can exhaust preprocessor resources (C99 mandates a minimum nesting depth of only 15 levels; modern compilers support up to 200).

## Embedded Implications
- **Search Path Collisions:** In large vendor SDKs (e.g., STM32Cube + FreeRTOS), conflicting versions of generic headers like `event_groups.h` can be shadowed if `-I` flags are ordered incorrectly in CMake or Makefiles.
- **`-isystem` Flag:** Marking third-party SDK paths with `-isystem` silences vendor compiler warnings and changes directory search priority.

## Firmware Review Angle
- Confirm all `#include` directives use forward slashes `/`, never backslashes `\`.
- Check that system headers use `<...>` and local headers use `"..."`.
- Enforce strict include directory hygiene in the build system: avoid adding repository root `.` to `-I`.

## Compiler, ABI, and Toolchain Implications
- Compiler dependency generation flags (`-MMD`, `-MP`) track included files to trigger rebuilds when headers change.
- Missing `-MP` flags cause Make to crash with "No rule to make target" when a header file is deleted or renamed.

## Performance, Memory, Timing, and Power
- Excessive file inclusion cascades dramatically inflate preprocessor memory usage and rebuild times. A 100-line `.c` file can expand to 50,000 lines of preprocessed source if headers are loosely managed.

## Verification / Debugging
- GCC/Clang: Use `-H` during compilation to print the entire hierarchical tree of included headers to stderr.
- Use `gcc -v -E - < /dev/null` to display the active search path resolution order.

## Safety, Security, and Reliability
- MISRA C:2012 Directive 4.10: Precautions shall be taken in order to prevent the contents of a header file being included more than once.
- MISRA C:2012 Rule 20.3: The `#include` directive shall be followed by either a `<filename>` or `"filename"` sequence.

## Trade-offs and Alternatives
- **Include What You Use (IWYU):** Include only the headers declaring symbols directly used in the file. Avoid "umbrella" or "catch-all" headers (`common.h`, `all.h`) which ruin modularity and rebuild parallelism.

## Staff-Level Takeaway
Never rely on transitive header inclusions. Every source file must explicitly include the direct headers it depends on. Keep `-I` search paths disciplined, use `-H` to audit header bloat, and isolate vendor HAL trees using explicit subdirectory prefixes.

## Related Concepts
- `03_Conditional_inclusion`
- `08_Include_guards`
- `12_Preprocessor_architecture`
