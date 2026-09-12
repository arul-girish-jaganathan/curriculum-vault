# va_start

## Definition
`va_start` is the `<stdarg.h>` macro that initializes a `va_list` so a variadic function can begin traversing its unnamed arguments. It establishes implementation-specific traversal state using the final named parameter as the point immediately before the first argument represented by `...`.

The operation is part of a strict lifecycle: initialize with `va_start`, consume with `va_arg`, and finish with `va_end`.

## Scope and Boundaries
* **Covers:** invocation requirements, the final named parameter, lifecycle, promotions, and common portability hazards.
* **Does not cover:** detailed argument retrieval in [[03_va_arg]] or target-specific register/stack layouts in [[09_ABI_details]].

## Why Does It Exist
A prototype such as `int log(const char *fmt, ...);` tells the compiler that additional arguments exist but does not give those arguments names or types. `va_start` connects the fixed portion of the function call with the traversal state needed to access the unnamed portion.

## Mechanism and Language Rules
Typical use:

```c
#include <stdarg.h>

static int sum(unsigned count, ...)
{
    va_list ap;
    int result = 0;

    va_start(ap, count);
    for (unsigned i = 0; i < count; ++i)
        result += va_arg(ap, int);
    va_end(ap);

    return result;
}
```

The final named parameter is important because the implementation uses the call's argument-passing state to establish where unnamed arguments begin. The parameter must satisfy the restrictions imposed by the targeted C standard; in particular, the old form where the last named parameter is declared with a type subject to default argument promotions is not a portable basis for `va_start` in modern C.

`va_start` does not inspect the runtime value of the named parameter. Its purpose is to initialize traversal metadata. The actual unnamed argument types are recovered later through `va_arg`.

### What to reason about
- The function must actually be variadic; `va_start` is not a general-purpose way to inspect arbitrary parameters.
- The `va_list` must be initialized before `va_arg` or a copy operation is used.
- The traversal must eventually be terminated with `va_end`.
- Default argument promotions affect what `va_arg` must request: for example, a passed `float` is retrieved as `double`, and narrow integer types are promoted according to the language rules.
- The final named parameter must be selected carefully; do not use an expression, register, or a parameter whose type violates the macro's requirements.

## Examples

### Correct counted interface
```c
static unsigned sum_u32(unsigned count, ...)
{
    va_list ap;
    unsigned total = 0;

    va_start(ap, count);
    for (unsigned i = 0; i < count; ++i)
        total += va_arg(ap, unsigned);
    va_end(ap);

    return total;
}
```

### Incorrect design: no reliable boundary
```c
/* There is no portable way to know how many unnamed arguments exist. */
static void bad_api(...); /* not a valid ISO C function definition/interface */
```

A variadic API therefore needs an explicit contract such as a count, a sentinel, or a format/tag scheme.

## Undefined, Unspecified, and Implementation-Defined Behavior
* Calling `va_arg` on a `va_list` that was never initialized with `va_start` or an appropriate copy operation is invalid.
* Using an inappropriate final named parameter can make the program fail to satisfy the requirements of `va_start` and therefore lose portability or correctness.
* There is no portable mechanism to discover the number of unnamed arguments automatically.
* The internal representation of the initialized `va_list` is implementation-defined and must not be decoded by application code.

## Edge Cases and Failure Modes
* **Promoted `float`:** pass `float`, retrieve `double`.
* **Small integers:** `char`, `signed char`, `unsigned char`, `short`, and related types may be promoted to `int` or `unsigned int`; retrieve the promoted type.
* **Sentinel APIs:** a sentinel must have a representation/type that can be compared safely; pointer sentinels deserve particular care on targets where integer constants and pointers are not interchangeable.
* **Count overflow:** if a count is attacker-controlled or computed incorrectly, the traversal can read beyond the actual arguments.
* **Early exit:** `return`, `goto`, or error paths must not bypass `va_end`.

## Embedded Implications
`va_start` can establish state involving registers and stack areas. On a small MCU, this can increase call overhead and stack pressure compared with a fixed parameter list. It should therefore be kept out of hard real-time paths unless measured.

Do not initialize a `va_list` in one execution context and defer its use to an ISR or another task. The traversal belongs to the lifetime of the originating call.

## Firmware Review Angle
Review the API contract before reviewing the macro call. Ask: How does the callee know how many arguments exist? How are their types encoded? Can a malformed message make traversal run past the provided arguments? Is the function allowed in an ISR or timing-critical task?

## Compiler, ABI, and Toolchain Implications
The compiler expands or lowers `va_start` according to the target ABI. A variadic function may need to make register-passed arguments available to a traversal mechanism and may therefore have a different prologue from a fixed-parameter function.

Never substitute a hand-written stack-pointer calculation for `va_start`; such code is ABI-specific and fragile across compiler versions, optimization levels, floating-point ABI settings, and architecture variants.

## Performance, Memory, Timing, and Power
Initialization is normally small but ABI-dependent. The more important system cost is often the complete variadic call path: argument setup, register-save handling, `va_arg` traversal, formatting, and output.

For deterministic firmware, prefer a fixed-layout event structure when the data schema is known.

## Verification / Debugging
Compile with strong warnings and test on every supported ABI. Exercise zero arguments where the API permits it, minimum and maximum counts, mixed promoted types, and all error exits. Inspect stack usage in embedded builds and use a debugger to inspect the `va_list` only as an opaque implementation object, not by assuming its layout.

## Safety, Security, and Reliability
The most important safety property is a trustworthy argument contract. A `va_start` call itself does not provide type safety. Pair variadic APIs with bounded counts, explicit tags, validated format strings, or generated wrappers.

## Trade-offs and Alternatives
* **Use:** generic logging, formatting, compatibility APIs, and truly variable argument interfaces.
* **Avoid:** variadic interfaces when a fixed struct or typed function can express the contract.
* **Alternatives:** typed parameter structures, tagged records, arrays of typed records, or generated wrappers.

## Staff-Level Takeaway
`va_start` is the bridge from a normal named-parameter interface to ABI-specific variadic traversal. A Staff engineer should verify the API's argument-count/type contract, understand promotion effects, guarantee `va_end` on every path, and treat the entire variadic call as a portability and determinism boundary.

## Related Concepts
* [[00_Chapter_Index]]
* [[01_va_list]]
* [[03_va_arg]]
* [[04_va_end]]
* [[05_Default_argument_promotions]]
* [[09_ABI_details]]
