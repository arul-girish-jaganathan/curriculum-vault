# 03: stdbool.h

## Definition
`<stdbool.h>` historically provides a convenient Boolean interface through `bool`, `true`, and `false` for C99/C11-style source. In C23, `bool` is a language keyword and the `<stdbool.h>` interface is deprecated for new code. Boolean expressions in C still use scalar truth semantics: zero is false and nonzero is true.

## Scope and Boundaries
* **Covers:** `bool`, `true`, `false`, truth-value conversion, compatibility across C language revisions.
* **Does not cover:** C++ `bool` semantics, atomic Boolean objects, or application-specific Boolean protocol encodings.

## Why Does It Exist
Older C code commonly used integers as logical flags. A dedicated Boolean type communicates intent, makes APIs easier to review, and can prevent accidental use of arbitrary integer values as state representations. The standard header also provided a compatibility layer before C23 made Boolean types part of the language directly.

## Mechanism and Language Rules
1. A scalar value in a controlling context converts to a truth value: zero/null is false; anything else is true.
2. `_Bool` is the fundamental C Boolean type before C23. Assigning a scalar to `_Bool` stores `0` or `1`.
3. `bool`, `true`, and `false` were provided by `<stdbool.h>` as convenient macros in pre-C23 modes.
4. Comparisons and logical operators produce an `int` result in traditional C, even when the operands are `_Bool`.
5. `&&`, `||`, and `?:` participate in short-circuit or conditional evaluation rules; truth type and evaluation order must not be conflated.

## Examples
```c
#include <stdbool.h>

static bool is_valid(unsigned value)
{
    return value != 0U;
}

static int consume(bool ready)
{
    if (ready) {
        return 1;
    }
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
* Converting any scalar value to `_Bool` is well-defined: zero becomes `0`, nonzero becomes `1`.
* Writing a Boolean result into a protocol field without defining its external representation is a design error, not a guarantee that the peer sees one particular byte encoding.
* Reading an uninitialized automatic Boolean object is undefined behavior because the object has an indeterminate value.
* Bit-fields declared as `_Bool` have implementation constraints on layout and should not be treated as wire-format fields.

## Edge Cases and Failure Modes
* `bool x = 2;` yields `true`, not a stored value of `2`.
* `sizeof(bool)` is implementation-dependent; do not assume one byte across every C implementation.
* `if (flag == true)` can obscure the fact that a scalar flag may hold any nonzero value before conversion; `if (flag)` is often clearer.
* Using Boolean values directly as register fields can accidentally create a read-modify-write operation or an ABI-dependent storage width.

## Embedded Implications
* **State machines:** `bool` is useful for local control state, but state-machine domains with more than two states should use an enum or explicit state type.
* **MMIO:** never infer peripheral register width from the C Boolean type; use the access width required by the hardware reference manual.
* **Interoperability:** public interfaces crossing firmware modules should define whether Boolean state is a C value, an integer field, or a serialized byte.

## Firmware Review Angle
1. Check whether a Boolean is being used to represent more than two states.
2. Verify that Boolean values crossing an ABI or wire boundary have an explicit encoding.
3. Compare C language mode settings across all translation units.
4. In C23 migration work, identify code that depends on historical `<stdbool.h>` macros.

## Compiler, ABI, and Toolchain Implications
The representation and ABI rules for `_Bool` are implementation-defined within the standard's constraints. A compiler may optimize Boolean branches aggressively because the semantic domain is only zero/nonzero. Whole-program optimization can collapse repeated Boolean computations, but volatile MMIO accesses and observable side effects remain governed by their separate language rules.

## Performance, Memory, Timing, and Power
Boolean storage can reduce conceptual complexity without guaranteeing a one-byte object or lower RAM cost. Branch-heavy code may be optimized into conditional moves or branchless forms depending on target architecture. The semantic Boolean conversion itself is normally cheap, but unnecessary conversions at hot boundaries should still be measured on constrained MCUs.

## Verification / Debugging
* Compile with warnings such as `-Wall -Wextra -Wconversion`.
* Inspect the debugger's displayed type and underlying representation when ABI behavior matters.
* Add unit tests for zero, one, and representative nonzero values.
* During C23 migration, build the same module under the project's supported language modes.

## Safety, Security, and Reliability
A Boolean flag should represent a constrained state only when the API enforces that contract. Never use Boolean conversion to silently sanitize untrusted values when the distinction between multiple invalid states matters. For security-sensitive code, explicitly validate inputs before reducing them to true/false.

## Trade-offs and Alternatives
* **Use `bool`:** for genuinely binary state and predicate-returning APIs.
* **Use `enum`:** for finite multi-state domains.
* **Use fixed-width integers:** for hardware registers and serialized protocol fields with explicit widths.
* **Use bit masks:** when multiple independent flags must be packed into one control word.

## Staff-Level Takeaway
Boolean types are about semantic intent, not storage width. A Staff engineer should decide whether the domain is truly binary, where truth conversion occurs, and whether the value crosses a boundary where representation must be specified explicitly. C23 further changes the portability discussion, so the project's language mode should be a deliberate architectural choice.

## Related Concepts
* [[00_Chapter_Index]]
* [[../09_C_Expressions_Evaluation/00_Chapter_Index]]
* [[../16_C_Struct_Union_Enum/00_Chapter_Index]]
* [[../47_C_Safety_Security_Coding/00_Chapter_Index]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*