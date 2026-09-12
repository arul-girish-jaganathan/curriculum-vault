# 08: stdarg.h

## Definition
`<stdarg.h>` defines the language/library interface for accessing arguments passed through a variadic function. The core facilities are `va_list`, `va_start`, `va_arg`, `va_copy`, and `va_end`. Variadic access is type-directed at each retrieval site; C does not carry runtime type metadata for the unnamed arguments.

## Scope and Boundaries
* **Covers:** variadic parameter syntax, `va_list`, argument traversal, default argument promotions, copying, and cleanup.
* **Does not cover:** implementation-specific calling conventions in detail or format-string parsing itself.

## Why Does It Exist
Generic APIs such as logging, formatting, and aggregation sometimes need a variable number of arguments. C exposes variadic functions while leaving the programmer responsible for maintaining a correct contract between the caller's actual arguments and the callee's `va_arg` requests.

## Mechanism and Language Rules
1. A function is variadic when its parameter list contains `...` after at least one named parameter.
2. `va_start` initializes a `va_list` to access unnamed arguments after the last named parameter.
3. `va_arg(ap, type)` retrieves the next argument as `type`, subject to the default argument promotions and the variadic contract.
4. `va_copy` creates an independent traversal state when the implementation requires separate passes.
5. Each initialized `va_list` must be passed to `va_end` before its lifetime ends.
6. The actual argument types are not dynamically encoded; mismatch between the call contract and `va_arg` type can produce undefined behavior.

## Examples
```c
#include <stdarg.h>

static int sum_ints(size_t count, ...)
{
    va_list ap;
    int total = 0;

    va_start(ap, count);
    for (size_t i = 0; i < count; ++i) {
        total += va_arg(ap, int);
    }
    va_end(ap);
    return total;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
* Requesting a type from `va_arg` that is incompatible with the promoted actual argument type can be undefined behavior.
* Reading beyond the number of supplied arguments is undefined behavior.
* Reusing a `va_list` after `va_end` without reinitialization is invalid.
* Passing an invalid named parameter to `va_start` violates the requirements of that macro's use.

## Edge Cases and Failure Modes
* `float` arguments are promoted to `double`, so `va_arg(ap, float)` is wrong for a caller passing a `float` through `...`.
* `char` and `short` are promoted to `int` or `unsigned int` as required by the integer promotions.
* A `va_list` is not guaranteed to be an ordinary pointer; on some ABIs it can be an array type or a structured state object.
* Copying a `va_list` by simple assignment is not universally sufficient; use `va_copy` where available/required.

## Embedded Implications
Variadic APIs can be expensive in firmware because each argument may have different ABI handling, formatting can pull in large library code, and type mismatches are difficult to diagnose statically. Logging frameworks should strongly prefer compiler-checked format attributes or typed wrappers.

## Firmware Review Angle
Inspect the complete caller/callee contract. Verify promotion rules, `va_copy` usage, and cleanup on every exit path. Check whether variadic formatting accidentally pulls floating-point, locale, or file I/O code into a small firmware image.

## Compiler, ABI, and Toolchain Implications
Variadic calls expose ABI details such as general-purpose versus floating-point argument registers, register save areas, stack layout, and alignment. A compiler knows the fixed parameters but generally cannot type-check arbitrary unnamed arguments unless the API adds format-string metadata. ABI mismatches across object files are especially dangerous for variadic code.

## Performance, Memory, Timing, and Power
Traversing a variadic list is usually modestly expensive, but format conversion can dominate execution time and code size. Variadic logging in an ISR is often a poor design because it creates unbounded work and may acquire locks or perform memory allocation.

## Verification / Debugging
* Compile with format-checking options such as `-Wformat` and project-specific attributes where applicable.
* Unit-test every supported argument type and boundary count.
* Inspect generated assembly for representative variadic calls on each ABI.
* Use sanitizers and fuzzed format strings for formatting APIs.

## Safety, Security, and Reliability
Variadic interfaces are a classic type-confusion boundary. Format-string vulnerabilities arise when untrusted strings control the expected argument layout. Keep format strings constant where possible, validate counts, and wrap low-level variadic APIs behind constrained, typed interfaces.

## Trade-offs and Alternatives
* **Use variadic functions:** when the flexibility is intrinsic to the API, such as `printf`-style formatting.
* **Prefer typed structures:** when arguments form a stable semantic object.
* **Prefer macros or generic selection:** when compile-time type information can improve safety.

## Staff-Level Takeaway
Variadic C trades compile-time type safety for API flexibility and ABI dependence. A Staff engineer should treat every `...` as an explicit contract that must be reconstructed from the caller, callee, promotions, and ABI rather than assuming runtime type information exists.

## Related Concepts
* [[00_Chapter_Index]]
* [[../12_C_Functions/00_Chapter_Index]]
* [[../33_C_Variadic_Functions/00_Chapter_Index]]
* [[../36_C_Linkage_ABI/00_Chapter_Index]]
* [[../47_C_Safety_Security_Coding/00_Chapter_Index]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*