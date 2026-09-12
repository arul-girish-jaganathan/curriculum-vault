# 06: Strict Aliasing

## Definition
Strict aliasing is an ISO C standard rule (C99/C11/C23 Section 6.5p7) stating that a pointer of one type shall not be used to access an object of a different, incompatible type. It enables Type-Based Alias Analysis (TBAA), allowing compilers to assume that pointers of different types do not point to the same memory location.

## Scope and Boundaries
- **Covers:** TBAA, pointer type compatibility, type punning violations, and compiler optimization flags (`-fno-strict-aliasing`).
- **Does not cover:** Character type exceptions ([[07_Character_type_access]]) or union punning nuances ([[08_Union_aliasing_nuances]]).

## Why Does It Exist
Without strict aliasing, compilers must assume that any pointer write could potentially modify *any* variable in scope of a compatible pointer type, severely limiting optimization passes like register caching and instruction reordering.

## Mechanism and Language Rules
- **Incompatible Types:** Pointers of distinct base types (e.g., `int *` and `float *`, or `int *` and `long *`) cannot alias each other.
- **Exceptions:**
  - Character types (`char`, `signed char`, `unsigned char`).
  - Compatible qualified types (`const int *` and `int *`).
  - Aggregate types containing the target type (structs/unions).
- **Compiler Flags:** `-fstrict-aliasing` (enabled by default in `-O2`/`-O3`) enforces this rule; `-fno-strict-aliasing` disables TBAA.

## Examples
```c
#include <stdio.h>

void increment(int *i_ptr, float *f_ptr) 
{
    *i_ptr += 1;
    *f_ptr += 1.0f;
    /* Under strict aliasing, compiler assumes i_ptr and f_ptr do not point */
    /* to the same memory. It caches *i_ptr in a register across *f_ptr write. */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Accessing an object through an incompatible pointer type. If `int *` and `float *` point to the same address, reading via one after writing via the other triggers undefined behavior.

## Edge Cases and Failure Modes
- **Type Punning Bugs:** Writing `int` and reading back via `float` through direct pointer casts breaks under optimization, producing corrupt calculations.

## Embedded Implications
- **MMIO Register Access:** Improperly casting pointers to access hardware registers of different widths can violate strict aliasing, leading to optimized-out register reads/writes.

## Firmware Review Angle
- **Flag Type Casts:** Search codebases for unsafe pointer casts between incompatible types (e.g., `*(float *)&my_int`). Require `memcpy` or union wrappers.
- **Check Optimization Flags:** Be aware whether `-fno-strict-aliasing` is relied upon in legacy embedded codebases.

## Compiler, ABI, and Toolchain Implications
- **TBAA Optimization:** TBAA allows compilers to eliminate redundant loads, keeping variables in CPU registers across function calls.

## Performance, Memory, Timing, and Power
- **Significant Speedups:** Strict aliasing yields 10% to 30% performance improvements in compute-heavy loops by eliminating redundant memory round-trips.

## Verification / Debugging
- **GCC `-Wstrict-aliasing`:** Warns about certain blatant strict aliasing violations during compilation.

## Safety, Security, and Reliability
- **Optimizer Induced Bugs:** Code that "works" at `-O0` often breaks catastrophically at `-O3` due to strict aliasing optimizations stripping out re-reads.

## Trade-offs and Alternatives
- **`memcpy` vs. Punning:** Using `memcpy` copies object representations without violating strict aliasing rules, compiling down to efficient register moves.

## Staff-Level Takeaway
Strict aliasing is non-negotiable in modern C. Never type-pun via direct pointer casts. Whenever you need to reinterpret the binary representation of data as a different type, use `memcpy` or standard union mechanisms.

## Related Concepts
- [[00_Chapter_Index]]
- [[07_Character_type_access]]
- [[08_Union_aliasing_nuances]]
- [[09_restrict_and_alias_analysis]]
