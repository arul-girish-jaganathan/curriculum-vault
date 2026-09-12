# 01: stddef.h

## Definition
`<stddef.h>` provides fundamental implementation-aware types, macros, and definitions used to write portable C interfaces. The key facilities are `size_t`, `ptrdiff_t`, `max_align_t`, `NULL`, `offsetof`, and related definitions. It is a bridge between the C abstract machine and the sizes, differences, alignment requirements, and layout of objects in a concrete implementation.

## Scope and Boundaries
* **Covers:** `size_t`, `ptrdiff_t`, `max_align_t`, `NULL`, `offsetof`, and implementation limits exposed through `<stddef.h>`.
* **Does not cover:** fixed-width integer types (`<stdint.h>`), complete object-layout rules, or allocator APIs (`<stdlib.h>`).

## Why Does It Exist
Portable C cannot assume that object sizes, pointer differences, or maximum alignment fit in a particular integer type. `<stddef.h>` gives the implementation a standard vocabulary for expressing these properties without hard-coding a target word size.

## Mechanism and Language Rules
1. **`size_t`:** Unsigned integer type capable of representing the size in bytes of any object. `sizeof` produces a `size_t` result.
2. **`ptrdiff_t`:** Signed integer type capable of representing the difference between two pointers into the same array object, when that difference is representable.
3. **`max_align_t`:** Type whose alignment requirement is at least as strict as every scalar type; useful for storage intended to hold arbitrary scalar objects.
4. **`offsetof(type, member)`:** Produces the byte offset of a structure or union member subject to the standard's constraints; portable use is for appropriate complete structure/union types and members.
5. **`NULL`:** Null pointer constant macro supplied by the implementation. Do not depend on its textual representation being `0` or `((void *)0)`.

## Examples
```c
#include <stddef.h>
#include <stdint.h>

struct packet {
    uint8_t type;
    uint32_t length;
    uint8_t payload[8];
};

static size_t payload_size(void)
{
    return sizeof(((struct packet *)0)->payload);
}

static size_t payload_offset(void)
{
    return offsetof(struct packet, payload);
}

static ptrdiff_t distance(const int *first, const int *last)
{
    return last - first;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
* **Pointer subtraction:** Subtracting pointers that do not refer into the same array object, or one-past it, is undefined behavior.
* **`offsetof`:** Applying it outside its standard constraints is undefined or constraint-violating depending on the expression and implementation; do not use it as a general “address arithmetic” primitive.
* **`size_t` conversion:** Converting a very large `size_t` to a narrower signed or unsigned integer can lose information or change the value.
* **`NULL`:** The implementation defines the macro; code should only rely on its semantic role as a null pointer constant.

## Edge Cases and Failure Modes
* Comparing a `size_t` value against `-1` causes the signed operand to be converted to unsigned, producing surprising results.
* Using `ptrdiff_t` for byte lengths can create negative values when a length should be unsigned.
* Assuming `offsetof` gives the “wire format” offset ignores padding, packing pragmas, ABI rules, and endianness.
* Using `sizeof(int)` where the API actually needs `sizeof(element)` creates portability defects when types change.

## Embedded Implications
* **DMA and buffers:** APIs should use `size_t` for buffer byte counts, avoiding hard-coded 16/32-bit lengths unless the hardware register explicitly requires them.
* **Memory-constrained targets:** `size_t` may be 16, 32, or wider depending on the implementation; API design must avoid truncation when buffers can cross that range.
* **ABI:** `size_t`, `ptrdiff_t`, and structure layout affect function signatures and binary interfaces, especially across modules compiled with inconsistent ABI options.

## Firmware Review Angle
1. Check every size calculation for signed/unsigned mixing.
2. Check that `offsetof` is not being used to infer a portable external binary layout.
3. Verify that public APIs use types appropriate to the representable domain, not merely the target's current word size.
4. Compare debug and release builds when packing, alignment, or ABI options change.

## Compiler, ABI, and Toolchain Implications
`sizeof`, `offsetof`, and alignment information are normally folded at compile time. The exact widths and alignments are ABI properties. Inlining and LTO can eliminate helper functions built around these compile-time constants. Cross-module ABI mismatches can silently corrupt parameters or structure interpretation even when source code looks type-correct.

## Performance, Memory, Timing, and Power
The `<stddef.h>` types themselves have no intrinsic runtime cost. `sizeof` and `offsetof` are compile-time constants in ordinary use. Choosing unnecessarily wide application-level fields where the API only needs a bounded range can increase memory footprint, but shrinking an interface below the implementation-defined range can create correctness bugs.

## Verification / Debugging
* Compile with `-Wall -Wextra -Wconversion -Wsign-conversion` where practical.
* Use `_Static_assert(sizeof(size_t) >= 2, "unexpected size_t width");` only when a project genuinely requires such a minimum.
* Inspect `sizeof` and `_Alignof` values in target-specific tests.
* Use debugger/watch expressions to verify structure offsets and compare them with map files or ABI documentation.

## Safety, Security, and Reliability
Size computations often become security boundaries. Integer truncation involving `size_t` can produce undersized allocations followed by oversized copies. Validate conversions at trust boundaries. Use `offsetof` carefully in container-style data structures and avoid turning layout assumptions into wire-protocol contracts without an explicit serialization format.

## Trade-offs and Alternatives
* **Use `<stddef.h>` types when:** expressing object sizes, pointer differences, alignment storage, and standard layout queries.
* **Avoid replacing them with:** `int`, `unsigned long`, or target-specific typedefs merely because they happen to work on one MCU.
* **Alternatives:** use `<stdint.h>` for protocol/register widths, and explicit serialization/deserialization for external formats.

## Staff-Level Takeaway
Treat `<stddef.h>` as the portable boundary between source-level intent and implementation-specific object representation. A Staff engineer should ask whether each use communicates a semantic domain—size, distance, alignment, offset—or merely encodes a machine assumption. Correct type selection here prevents a large class of portability and memory-safety failures.

## Related Concepts
* [[00_Chapter_Index]]
* [[02_stdint_h]]
* [[04_limits_h]]
* [[../27_C_Alignment_Object_Representation/00_Chapter_Index]]
* [[../26_C_Lifetime_Aliasing/00_Chapter_Index]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*