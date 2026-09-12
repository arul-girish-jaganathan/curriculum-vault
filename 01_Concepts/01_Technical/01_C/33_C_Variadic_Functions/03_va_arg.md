# va_arg

## Definition
`va_arg` is the `<stdarg.h>` macro used to retrieve the next unnamed argument from a `va_list` and advance the traversal state. It requires the caller to supply the type that the argument has at the point where it is retrieved.

Unlike an ordinary typed parameter, the compiler generally cannot derive the unnamed argument's type from the function prototype. The type supplied to `va_arg` is therefore part of the programmer-defined contract, and violating that contract can result in undefined behavior.

## Scope and Boundaries
* **Covers:** retrieval syntax, promotions, type matching, sequencing, alignment, and failure modes.
* **Does not cover:** initialization in [[02_va_start]], cleanup in [[04_va_end]], or complete ABI layouts in [[09_ABI_details]].

## Why Does It Exist
Variadic functions need a portable operation for consuming an arbitrary sequence of arguments without knowing their names at compile time. `va_arg` provides that operation while allowing the implementation to hide whether the next argument resides in a register, stack slot, register-save area, or another ABI-specific location.

## Mechanism and Language Rules
The basic form is:

```c
int value = va_arg(ap, int);
```

The macro evaluates the current traversal state, retrieves the next argument as the requested type, and advances `ap` so the following call obtains the following argument.

The requested type is not a request to convert an arbitrary argument safely. It describes the type that the variadic caller actually supplied after default argument promotions, subject to the standard's special compatible-type rules. The distinction is critical.

For example:

```c
static double first_value(...); /* illustrative only: ISO C needs a named parameter */
```

A valid variadic function would instead use:

```c
static double first_value(int count, ...)
{
    va_list ap;
    va_start(ap, count);
    double value = va_arg(ap, double); /* caller supplied float or double */
    va_end(ap);
    return value;
}
```

### What to reason about
- What exact type did the caller pass?
- What type did default argument promotions produce?
- Does the requested type satisfy the `va_arg` compatibility rules?
- Does the caller actually provide another argument at this position?
- Does the requested type impose alignment requirements that the ABI must honor?
- Has the traversal already been consumed or terminated?

## Examples

### Correct promotion-aware retrieval
```c
static double read_number(int unused, ...)
{
    va_list ap;
    va_start(ap, unused);

    /* A float argument is promoted to double. */
    double x = va_arg(ap, double);

    va_end(ap);
    return x;
}
```

### Counted sequence
```c
static int sum(unsigned count, ...)
{
    va_list ap;
    int total = 0;

    va_start(ap, count);
    for (unsigned i = 0; i < count; ++i)
        total += va_arg(ap, int);
    va_end(ap);
    return total;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
* If there is no actual next argument, invoking `va_arg` is invalid.
* If the requested type is incompatible with the actual promoted argument type, behavior is undefined except for the specific compatibility cases defined by the C standard.
* Asking for `float` when the caller passed `float` is a classic mistake: the argument was promoted to `double`, so `double` must be requested.
* Requesting a type that cannot be represented correctly according to the variadic rules is not repaired by an implicit conversion.
* The implementation's traversal representation and argument placement are not portable application-level details.

## Edge Cases and Failure Modes
* **`char`/`short`:** usually promoted to `int` or `unsigned int`; do not retrieve them as their original narrow type.
* **`float`:** promoted to `double`.
* **Pointers:** retrieve the pointer type actually passed; do not assume unrelated pointer types are interchangeable merely because their sizes match.
* **Width-sensitive integers:** `uint32_t` may have a different underlying type on another implementation; explicit format/type contracts must account for this.
* **Structures:** variadic structure passing is ABI-sensitive and may involve multiple registers or stack locations.
* **Repeated reads:** every `va_arg` advances the traversal; reading twice does not return the same argument.
* **Sentinel termination:** if a sentinel is part of the API, the loop must identify it without first retrieving an incompatible type.

## Embedded Implications
Incorrect `va_arg` use is especially dangerous on embedded targets because register-class and stack-layout differences can turn a seemingly harmless mismatch into immediate corruption. A wrong retrieval can consume the wrong number of bytes or read from the wrong argument area.

In an ISR or high-priority task, repeated `va_arg` processing can also create unpredictable execution time. General-purpose formatting should not be assumed to be real-time safe.

## Firmware Review Angle
For each `va_arg`, trace backward to the caller contract. Do not review the macro in isolation. Check all call sites, compiler warnings, format annotations, integer widths, floating-point ABI, and target architecture.

A particularly useful review question is: "If I change the compiler's ABI option or move this function across a module boundary, does the type contract remain identical?"

## Compiler, ABI, and Toolchain Implications
The compiler lowers `va_arg` according to the calling convention. ABIs can classify integer, floating-point, aggregate, and aligned arguments differently. A change such as hard-float versus soft-float can therefore affect variadic behavior and generated code.

Hand-written replacements based on casts from `char *`, stack-pointer arithmetic, or guessed register offsets are not portable substitutes for `va_arg`.

## Performance, Memory, Timing, and Power
A `va_arg` may be more expensive than a normal local variable load because it can perform alignment adjustments, select an argument register area, update traversal state, and access stack memory. Exact cost is target-dependent.

For small deterministic messages, a typed structure can reduce both execution cost and worst-case complexity.

## Verification / Debugging
Unit-test every variadic argument class used by the API: promoted integers, floating-point values, pointers, and any supported aggregates. Build on every target ABI. Enable compiler diagnostics for format-like wrappers where available.

When debugging a failure, inspect the call site and callee together. Disassembly is often more useful than looking at the opaque `va_list`, because it shows where arguments were actually placed and loaded.

## Safety, Security, and Reliability
A variadic API with no trustworthy type contract is effectively a runtime type system implemented by convention. A malicious or corrupted input can cause the callee to interpret arbitrary call data incorrectly.

For safety-critical interfaces, prefer explicit tags and typed records. If variadic formatting is required, constrain and validate the format language before calling the traversal code.

## Trade-offs and Alternatives
* **Use:** generic formatting and logging APIs where argument flexibility is essential.
* **Avoid:** using `va_arg` to emulate a dynamically typed data model when a tagged structure is simpler.
* **Alternatives:** fixed structures, tagged unions, generated serializers, typed wrappers, or separate APIs for distinct argument schemas.

## Staff-Level Takeaway
`va_arg` is where a variadic API's type contract becomes executable. A Staff engineer must be able to prove that every retrieval corresponds to the caller's promoted type, argument count, ABI, alignment, and lifetime. Matching representations by accident is not correctness; the interface contract must be explicit and testable.

## Related Concepts
* [[00_Chapter_Index]]
* [[01_va_list]]
* [[02_va_start]]
* [[04_va_end]]
* [[05_Default_argument_promotions]]
* [[06_Format_strings]]
* [[09_ABI_details]]
