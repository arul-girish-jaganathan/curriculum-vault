# va_list

## Definition
`va_list` is the C type used to represent the state required to traverse arguments supplied through a variadic function. It is declared by `<stdarg.h>` and is intentionally opaque: portable C code must not assume whether it is a pointer, array, structure, or scalar, nor how arguments are physically stored.

A variadic function normally has at least one named parameter followed by `...`. `va_list` provides the implementation-defined machinery needed by `va_start`, `va_arg`, and `va_end` to access the unnamed arguments according to the calling convention.

## Scope and Boundaries
* **Covers:** the `va_list` type, lifetime, copying, passing to helper functions, repeated traversal, and interaction with the other `<stdarg.h>` macros.
* **Does not cover:** the complete ABI for variadic calls, which is examined in [[09_ABI_details]], or the security design of format strings, covered in [[06_Format_strings]].

## Why Does It Exist
A function cannot declare an ordinary prototype for an arbitrary number and mixture of arguments. Variadic APIs such as logging, formatting, tracing, and compatibility interfaces therefore need a standard abstraction for walking the unnamed argument list.

The abstraction is deliberately stronger than "a pointer to the next argument." On some ABIs, arguments may be split among integer registers, floating-point registers, and stack memory, so a `va_list` can contain several pieces of traversal state.

## Mechanism and Language Rules
A typical traversal is:

```c
#include <stdarg.h>

static int sum_ints(unsigned count, ...)
{
    va_list ap;
    int total = 0;

    va_start(ap, count);
    for (unsigned i = 0; i < count; ++i) {
        total += va_arg(ap, int);
    }
    va_end(ap);
    return total;
}
```

The important rules are:

1. `va_list` objects are initialized by `va_start` or by copying an already initialized traversal with `va_copy` where supported by the language version being targeted.
2. Arguments are consumed in the order defined by repeated `va_arg` operations.
3. The type requested by `va_arg` must match the actual promoted argument type, subject to the specific compatible-type rules of the standard. Asking for an incompatible type can produce undefined behavior.
4. A `va_list` must be passed to `va_end` before the traversal object ceases to be usable.
5. Passing a `va_list` to another function can change the state of the caller's traversal; portable code must not assume that a passed `va_list` remains unchanged.
6. If independent traversals are required, create an independent copy with `va_copy` and terminate that copy separately.
7. `va_list` is not a general serialization format. Its state is meaningful only during the active variadic call and according to the ABI/compiler that created it.

## Examples

### One traversal
```c
static void dump_ints(unsigned count, ...)
{
    va_list ap;
    va_start(ap, count);

    for (unsigned i = 0; i < count; ++i) {
        int value = va_arg(ap, int);
        /* consume value */
        (void)value;
    }

    va_end(ap);
}
```

### Independent traversal
```c
static int count_and_sum(unsigned count, ...)
{
    va_list ap;
    va_list copy;
    int sum = 0;

    va_start(ap, count);
    va_copy(copy, ap);

    for (unsigned i = 0; i < count; ++i)
        sum += va_arg(ap, int);

    for (unsigned i = 0; i < count; ++i)
        (void)va_arg(copy, int);

    va_end(copy);
    va_end(ap);
    return sum;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
* The representation of `va_list` is implementation-defined and must not be inspected as if it were a normal pointer or integer.
* Fetching an argument with the wrong type can be undefined behavior even when the representations happen to look compatible on one target.
* Using a `va_list` after its corresponding `va_end`, or after the containing variadic invocation has returned, is invalid.
* Assuming that passing a `va_list` by value always creates an independent traversal is non-portable. On implementations where it is an array type or contains shared state, the behavior differs from a simple pointer copy.
* Reusing a `va_list` after passing it to a helper without following the required copy/consumption rules is a common portability defect.

## Edge Cases and Failure Modes
* **Array-type `va_list`:** an implementation may make `va_list` an array type, so ordinary C parameter adjustment can produce surprising semantics when it is passed to a function.
* **Register save areas:** a traversal may need to track both general-purpose and floating-point argument locations.
* **Mixed arguments:** `int`, `double`, pointers, and structures can follow different ABI rules.
* **Nested helpers:** a helper that consumes arguments changes the traversal position unless an independent copy is used.
* **Early return:** every initialized traversal must still reach `va_end`; cleanup must be structured carefully around all exits.
* **Asynchronous use:** a `va_list` cannot safely be retained for later processing after the original call has ended.

## Embedded Implications
On MCUs, `va_list` exposes a boundary between ISO C and the target ABI. A variadic call can use more registers, stack space, or prologue/epilogue work than an ordinary fixed-parameter call. This matters in small-stack tasks and interrupt-adjacent diagnostic code.

Do not store a `va_list` in a long-lived queue, pass it to another task, or defer its processing to an ISR. If a log record must cross a lifetime or execution-context boundary, materialize typed data or a serialized record instead.

## Firmware Review Angle
1. Confirm that every `va_start` has exactly one corresponding `va_end` on every control-flow path.
2. Check every `va_arg` against the actual argument contract, including default argument promotions.
3. Look for helpers that consume a traversal and then reuse the caller's `va_list`.
4. Inspect stack usage when variadic logging is used in deeply nested firmware paths.
5. Treat variadic APIs as ABI-sensitive interfaces when compilers, architectures, or optimization modes change.

## Compiler, ABI, and Toolchain Implications
The compiler knows the fixed parameters from the prototype but relies on the ABI to implement unnamed argument passing. On ARM-family ABIs, for example, integer and floating-point arguments can have distinct register/stack rules. The exact `va_list` representation is therefore a toolchain concern, not application-level data.

Compiler builtins commonly implement `<stdarg.h>` operations so that optimization can understand argument traversal without exposing the representation to user code. LTO can optimize around a variadic wrapper, but it cannot make an invalid type contract valid.

## Performance, Memory, Timing, and Power
A `va_list` itself has no portable fixed size. Traversal can involve register-save areas, stack reads, alignment adjustments, and conversions. The cost depends on the ABI and requested types.

For high-rate embedded telemetry, a typed record or fixed-format encoder is often cheaper and more deterministic than a general-purpose variadic formatter.

## Verification / Debugging
Use compiler warnings and format checking where available. Test every supported argument type on every supported ABI. Build for both debug and optimized configurations and inspect generated code when stack usage matters.

A useful unit-test strategy is to exercise mixed integer/floating-point/pointer arguments and verify that helper functions using `va_copy` do not disturb the original traversal. Static analysis should flag missing `va_end`, suspicious `va_arg` types, and retained traversal state.

## Safety, Security, and Reliability
Variadic APIs weaken compile-time type checking. A corrupted count, tag, or format string can cause the consumer to fetch arguments that do not exist or have the wrong type. In security-sensitive code, prefer a typed structure or an explicit tagged record when the argument set is known.

Logging must also avoid retaining pointers to temporary data whose lifetime ends before formatting occurs.

## Trade-offs and Alternatives
* **Use `va_list` when:** implementing a genuinely variadic interface or a `v*` helper such as `vprintf`-style APIs.
* **Avoid it when:** the argument schema is known at design time.
* **Alternatives:** typed structures, fixed parameter lists, tagged unions, arrays of explicitly typed records, or generated logging encoders.

## Staff-Level Takeaway
`va_list` is an ABI abstraction, not a portable pointer to a list. A Staff engineer should reason simultaneously about the language contract, default promotions, `va_arg` type correctness, traversal lifetime, helper-function ownership, and target calling convention. If an interface can be typed, make it typed; reserve variadic traversal for APIs where its flexibility has a clear architectural benefit.

## Related Concepts
* [[00_Chapter_Index]]
* [[02_va_start]]
* [[03_va_arg]]
* [[04_va_end]]
* [[05_Default_argument_promotions]]
* [[09_ABI_details]]
* [[10_Type_safety_limitations]]
