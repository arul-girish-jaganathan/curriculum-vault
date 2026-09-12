# 04: External Declarations

## Definition
An external declaration (`extern`) informs the compiler about the existence, identifier name, and type of a variable or function whose actual memory allocation and definition reside in a different translation unit (or elsewhere in the same file). It creates a symbol reference without reserving physical storage.

## Scope and Boundaries
Covers: `extern` function prototypes, `extern` global variable declarations, symbol resolution, and single-definition enforcement.
Does not cover: Internal linkage (`static`, see `11_Linkage_hygiene`).

## Why Does It Exist
Because C compiles each translation unit independently into an object file (`.o`), the compiler must know the types and signatures of external symbols to generate correct call instructions and data offsets. The linker subsequently resolves these external references to concrete physical memory addresses.

## Mechanism and Language Rules
1. **Functions Default to `extern`:** Function declarations in headers are implicitly `extern` whether the keyword is written or omitted.
2. **Variables Require Explicit `extern`:** Declaring a global variable in a header without `extern` creates a tentative definition or duplicate variable, violating linkage rules.
3. **No Initialization in Declarations:** An `extern` declaration must NOT initialize the variable:
   - `extern uint32_t g_system_ticks;` -> Declaration (No storage).
   - `extern uint32_t g_system_ticks = 0;` -> Definition! (Allocates storage; illegal in headers).

## Examples
```c
/* ================= system_state.h ================= */
#ifndef SYSTEM_STATE_H
#define SYSTEM_STATE_H

#include <stdint.h>

/* Declaration only: no storage allocated */
extern volatile uint32_t g_system_ticks;

/* Function declaration (extern is implicit) */
void system_tick_increment(void);

#endif /* SYSTEM_STATE_H */

/* ================= system_state.c ================= */
#include "system_state.h"

/* Single concrete definition: storage allocated in .bss/.data */
volatile uint32_t g_system_ticks = 0U;

void system_tick_increment(void) {
    g_system_ticks++;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Declaring an `extern` variable with a type that does not match its concrete definition in another translation unit invokes Undefined Behavior at runtime (symbol type mismatch).

## Edge Cases and Failure Modes
- **Ad-Hoc `extern` in `.c` Files:** Writing `extern int my_var;` inside a `.c` file without including the authoritative header bypasses type checking. If the variable's type later changes to `int64_t` in the defining `.c` file, the ad-hoc `extern` produces silent stack/memory corruption.

## Embedded Implications
- **Hardware Register Mapping:** CMSIS headers declare base peripheral pointers as `extern volatile USART_TypeDef *USART1;` allowing linkers to map them directly to hardware memory regions.

## Firmware Review Angle
- Ban ad-hoc `extern` declarations inside `.c` files. All external symbols MUST be declared in an authoritative header and included by both consumer and producer `.c` files.
- Reject any initialized variable declaration in a header file.

## Compiler, ABI, and Toolchain Implications
- Compilers generate relocatable symbol references (e.g., `R_ARM_ABS32`) in the object file's relocation table, which the linker binds during final image creation.

## Performance, Memory, Timing, and Power
- Accessing an external variable may require an extra indirect memory load instruction if the compiler cannot deduce its immediate address at compile time.

## Verification / Debugging
- Inspect unresolved symbols with `nm -u file.o` and exported symbols with `nm -g file.o`.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 8.4: A compatible declaration shall be visible when an object or function with external linkage is defined.
- MISRA C:2012 Rule 8.5: An external object or function shall be declared once in one and only one file.

## Trade-offs and Alternatives
- **Global `extern` Variables vs Getter/Setter Functions:** Global `extern` variables are fast and zero-overhead, but break thread-safety and encapsulation. Getter/setter functions encapsulate access at the cost of function call overhead (mitigated by `static inline`).

## Staff-Level Takeaway
Never use ad-hoc `extern` declarations in `.c` files. Declare external entities in a single authoritative header included by both the defining `.c` file (for validation) and all consuming `.c` files. Favor accessor functions over bare `extern` variables.

## Related Concepts
- `01_Public_headers`
- `05_Definition_ownership`
- `11_Linkage_hygiene`
