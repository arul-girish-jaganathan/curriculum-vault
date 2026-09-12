# 11: Linkage Hygiene

## Definition
Linkage hygiene is the strict control of symbol visibility across translation units. In ISO C, identifiers can have external linkage (accessible across all translation units), internal linkage (accessible only within the current translation unit via `static`), or no linkage (local variables). Linkage hygiene mandates minimizing external linkage to prevent global namespace pollution and unintended symbol collisions.

## Scope and Boundaries
Covers: `static` functions, `static` file-scope variables, `extern` declarations, GCC visibility attributes, and symbol hiding.
Does not cover: C++ class access modifiers.

## Why Does It Exist
All non-static functions and global variables in C share a single, flat global symbol namespace at link time. If two independent drivers both define a function named `init_hardware()`, the linker will fail with duplicate symbol errors, or worse, silently bind to the wrong function if weak symbols are involved.

## Mechanism and Language Rules
1. **Internal Linkage (`static`):** Declaring a file-scope function or variable as `static` limits its visibility strictly to the current translation unit. It cannot be seen or linked by other `.c` files.
2. **External Linkage (`extern`):** Non-static file-scope functions and variables have external linkage by default.
3. **No Linkage:** Block-scope local variables have no linkage; they exist only on the stack or in registers.

## Examples
```c
/* ================= drv_timer.c ================= */
#include "drv_timer.h"

/* Internal linkage: invisible outside this translation unit */
static volatile uint32_t s_overflow_count = 0;

static void internal_timer_recalibrate(void) {
    /* Private helper routine: cannot collide with other drivers */
    s_overflow_count = 0;
}

/* External linkage: the only symbol exported from this file */
void timer_init(void) {
    internal_timer_recalibrate();
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Declaring a symbol as `static` in a file after it was previously declared with external linkage in the same translation unit invokes Undefined Behavior in ISO C.

## Edge Cases and Failure Modes
- **Forgotten `static`:** Omitting `static` on an internal helper function (`void reset_fifo(void)`) exports it globally, risking collision with any other file that defines a helper of the same name.
- **Linker Masking:** In systems with weak symbols (`__attribute__((weak))`), a non-static helper function can inadvertently override a weak system hook, causing severe runtime bugs.

## Embedded Implications
- **Linker Section Optimization:** Compilers can optimize `static` functions more aggressively: if a `static` function is called only once, the compiler automatically inlines it and eliminates its function symbol entirely, reducing Flash memory usage.

## Firmware Review Angle
- Enforce the rule: **Every function and file-scope variable must be `static` unless it is explicitly declared in the module's public or private header**.
- Inspect compiler warnings for `-Wmissing-prototypes`: this flags any non-static function that lacks a header declaration.

## Compiler, ABI, and Toolchain Implications
- `static` symbols receive local symbol bindings (`STB_LOCAL`) in ELF symbol tables (`.symtab`) and are omitted entirely from dynamic symbol tables (`.dynsym`).

## Performance, Memory, Timing, and Power
- Marking functions `static` allows the compiler to make internal register-allocation decisions free from AAPCS calling convention constraints, improving execution speed and reducing stack frame overhead.

## Verification / Debugging
- Check global symbols exported by an object file:
  `nm -g --defined-only file.o`
  Only intended public API functions should appear in the output.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 8.7: Functions and objects should not be defined with external linkage if they are referenced in only one translation unit.
- MISRA C:2012 Rule 8.8: The `static` storage class specifier shall be used in all declarations of objects and functions that have internal linkage.

## Trade-offs and Alternatives
- Making everything `static` within a `.c` file improves safety and optimization, but makes white-box unit testing from external test harnesses harder (mitigated by test-specific compilation macros or mocking frameworks).

## Staff-Level Takeaway
Default to `static` for everything. A function or file-scope variable should only have external linkage if it is part of an official header contract. Enforce `-Wmissing-prototypes` across your toolchain to catch linkage leakage automatically.

## Related Concepts
- `04_External_declarations`
- `05_Definition_ownership`
- `12_Embedded_module_boundaries`
