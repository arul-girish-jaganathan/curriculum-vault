# 05: Definition Ownership

## Definition
Definition ownership is the architectural rule that every object, variable, and non-inline function must have exactly one translation unit that owns its physical storage allocation and lifetime. All other translation units must interact with that object solely through non-allocating declarations.

## Scope and Boundaries
Covers: The One Definition Rule (ODR) in C, storage allocation in `.data`/`.bss`, multiple definition linker errors (`multiple definition of ...`), and tentative definitions.
Does not cover: Inline functions with internal linkage (`static inline`).

## Why Does It Exist
Unlike C++, C has historically permitted ambiguous "tentative definitions" where uninitialized global variables in multiple files could be merged by the linker (common storage model). Modern toolchains (GCC 10+) default to `-fno-common`, causing duplicate global definitions to throw fatal linker errors. Enforcing strict definition ownership prevents binary collisions and indeterminate memory initialization.

## Mechanism and Language Rules
1. **Single Definition Rule:** An object shall have exactly one definition across the entire program.
2. **Declaration vs Definition:**
   - `extern int counter;` -> Declaration (0 bytes allocated).
   - `int counter;` or `int counter = 0;` -> Definition (Allocates `sizeof(int)` in `.bss` or `.data`).
3. **Owner Translation Unit:** The `.c` file that implements the subsystem must define the object and initialize its starting state.

## Examples
```c
/* ================= INCORRECT: Definition in Header ================= */
/* sensor.h */
#ifndef SENSOR_H
#define SENSOR_H
int g_sensor_reading; /* ERROR: Every file including sensor.h allocates storage! */
#endif

/* Linker fails with: multiple definition of `g_sensor_reading` */

/* ================= CORRECT: Strict Definition Ownership ============ */
/* sensor.h */
#ifndef SENSOR_H
#define SENSOR_H
extern int g_sensor_reading; /* Declarative reference only */
#endif

/* sensor.c */
#include "sensor.h"
int g_sensor_reading = 0; /* Owner TU: Allocates memory once */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Under legacy toolchains with `-fcommon`, multiple definitions without initializers are merged into a single common block. Under `-fno-common` (modern standard), this causes fatal link-time errors.

## Edge Cases and Failure Modes
- **Header Constants Without `static`:** Writing `const uint32_t TIMEOUT = 100;` in a header creates an external symbol definition in every translation unit that includes it, failing the build with multiple definition linker errors.
  *Fix:* Use `static const uint32_t TIMEOUT = 100;` or an enum.

## Embedded Implications
- **SRAM Section Mapping:** Embedded linkers use definition ownership to place variables into specific hardware RAM banks via section attributes (`__attribute__((section(".ccmram")))`). Only the owning `.c` file can specify this placement.

## Firmware Review Angle
- Confirm that no header file contains variable definitions without `extern` or `static`.
- Verify that compiler flags include `-fno-common` to ensure linker enforcement of strict definition ownership.

## Compiler, ABI, and Toolchain Implications
- The defining translation unit assigns the symbol to the `.bss` (uninitialized) or `.data` (initialized) section of its ELF output.

## Performance, Memory, Timing, and Power
- Strict ownership guarantees deterministic variable placement and eliminates memory bloat from duplicated definitions.

## Verification / Debugging
- Check symbol bindings in compiled object files:
  `nm file.o | grep ' B '` shows uninitialized definitions owned by this TU.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 8.6: An identifier with external linkage shall have exactly one external definition.

## Trade-offs and Alternatives
- **Global Owner vs Static Encapsulation:** Making the variable `static` inside its `.c` file and providing access functions (`sensor_get_reading()`) provides even stronger ownership by eliminating external linkage entirely.

## Staff-Level Takeaway
A header must never allocate memory. Always enforce single definition ownership: declare variables in headers with `extern`, define them once in their owning `.c` file, and enforce `-fno-common` in your build flags to catch rogue definitions at link time.

## Related Concepts
- `04_External_declarations`
- `11_Linkage_hygiene`
- `12_Embedded_module_boundaries`
