# 05: Effective Type

## Definition
The effective type of an object in ISO C is the type determined for an unnamed object allocated via dynamic storage functions (`malloc`) or objects declared without explicit type schemas (e.g., character arrays used for raw storage). It dictates how the memory location can be legally accessed under strict aliasing rules.

## Scope and Boundaries
- **Covers:** Dynamic object typing, character array type mutations, and type establishment rules.
- **Does not cover:** Static object declarations, strict aliasing rules ([[06_Strict_aliasing]]), or union aliasing ([[08_Union_aliasing_nuances]]).

## Why Does It Exist
C allows raw memory allocations (`malloc`) to store any data type. The effective type mechanism provides rules for how raw bytes acquire a specific type so compilers can optimize memory access without violating type safety.

## Mechanism and Language Rules
- **Initial State:** Newly allocated storage from `malloc` has no effective type.
- **Establishing Effective Type:** The effective type is established when a value is stored into the raw memory location via an lvalue of a specific type (other than character types).
- **Character Array Exception:** Writing to a character array (`char buf[10]`) does *not* change its effective type; it remains an array of characters, allowing raw byte inspection.

## Examples
```c
#include <stdlib.h>

int main(void) 
{
    void *mem = malloc(sizeof(int));
    if (!mem) return 1;

    /* Effective type of allocated memory becomes 'int' upon first store */
    *(int *)mem = 42; 

    /* Legal access via int pointer */
    int val = *(int *)mem;

    free(mem);
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Accessing memory allocated via `malloc` using an incompatible lvalue type *before* an effective type has been established via a store operation.

## Edge Cases and Failure Modes
- **Type Punning via `memcpy` vs. Direct Cast:** Direct casting raw `malloc` memory to incompatible pointers and dereferencing violates effective type and strict aliasing rules. `memcpy` must be used.

## Embedded Implications
- **Memory-Mapped I/O Buffers:** Raw peripheral buffers allocated as byte arrays must be accessed via character types or `memcpy` to comply with effective type rules.

## Firmware Review Angle
- **Inspect Casts on Raw Memory:** Verify that pointers derived from `malloc` or byte buffers are never cast and dereferenced as incompatible types without an intervening store of the correct type or use of `memcpy`.

## Compiler, ABI, and Toolchain Implications
- **Optimizer Assumptions:** Compilers assume objects of different effective types do not overlap, enabling aggressive load/store motion optimizations.

## Performance, Memory, Timing, and Power
- **Zero Runtime Cost:** Effective type is a purely compile-time language semantic rule used by optimizer alias analysis passes.

## Verification / Debugging
- **UBSan (-fsanitize=alignment,type):** Detects certain invalid type conversions and strict aliasing violations.

## Safety, Security, and Reliability
- **Undefined Behavior Mitigation:** Adhering to effective type rules prevents compiler optimizations from silently wiping out seemingly redundant memory writes.

## Trade-offs and Alternatives
- **`memcpy` Safety:** Using `memcpy` to copy bytes into typed structures bypasses effective type traps entirely and is 100% standard-compliant.

## Staff-Level Takeaway
Raw memory allocated by `malloc` is type-less until written to. Respect effective type rules by ensuring objects are initialized with matching lvalue types, and always use `memcpy` for byte-level type conversion.

## Related Concepts
- [[00_Chapter_Index]]
- [[../25_C_Dynamic_Memory/01_malloc]]
- [[06_Strict_aliasing]]
