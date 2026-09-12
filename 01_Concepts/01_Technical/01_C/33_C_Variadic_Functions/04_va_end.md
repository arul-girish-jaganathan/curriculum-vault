# va_end

## Definition
`va_end` is the `<stdarg.h>` macro that terminates access to a `va_list` initialized by `va_start` or an appropriate copy operation. It completes the lifetime of the traversal state and is required before the `va_list` is reused or goes out of scope.

Although many implementations make `va_end` appear to do nothing, portable code must treat it as a required part of the variadic lifecycle. An implementation may need to release or finalize hidden traversal state.

## Scope and Boundaries
* **Covers:** cleanup requirements, control-flow correctness, copies, helper functions, and lifetime.
* **Does not cover:** argument initialization and retrieval in [[02_va_start]] and [[03_va_arg]].

## Why Does It Exist
The representation of `va_list` is not specified. An implementation may need bookkeeping associated with register-save areas, stack traversal, or other resources. `va_end` gives the implementation a defined point at which the traversal is finished.

## Mechanism and Language Rules
Typical use:

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

The lifecycle is:

`va_start` → zero or more `va_arg` operations → `va_end`.

If an independent traversal was created with `va_copy`, that copy also requires its own `va_end`.

### What to reason about
- Is every initialized `va_list` terminated exactly as required?
- Are there early returns, error paths, or `goto` paths that bypass cleanup?
- Has a `va_list` already been passed to a helper that consumed or otherwise affected it?
- Are copied traversals independently terminated?
- Is the traversal being used after `va_end` or after the containing function has returned?

## Examples

### Correct cleanup on all paths
```c
static int process(unsigned count, ...)
{
    va_list ap;
    int result = 0;

    va_start(ap, count);

    if (count > 100U) {
        va_end(ap);
        return -1;
    }

    for (unsigned i = 0; i < count; ++i)
        result += va_arg(ap, int);

    va_end(ap);
    return result;
}
```

In larger functions, structure control flow so there is a single cleanup point when practical.

## Undefined, Unspecified, and Implementation-Defined Behavior
* Failing to call `va_end` after initializing a traversal violates the required usage contract; an implementation may rely on it for cleanup.
* Calling `va_end` on an uninitialized or already terminated traversal is not a valid way to repair incorrect lifecycle management.
* Using a `va_list` after `va_end` is invalid.
* The observable implementation cost of `va_end` is target-dependent; it must not be optimized away by application assumptions.

## Edge Cases and Failure Modes
* **Early return:** the most common lifecycle bug.
* **Error labels:** `goto` cleanup can be correct, but ensure the label is reached only after initialization.
* **Copies:** each independently initialized copy needs its own termination.
* **Helper consumption:** after passing a traversal to another function, do not assume the caller's traversal state is unchanged.
* **Stored state:** never treat a terminated traversal as persistent application data.

## Embedded Implications
Embedded libc implementations sometimes make `va_end` empty because the ABI requires no explicit teardown. That is an implementation detail, not a license to omit it. Keeping the macro makes code portable to targets where traversal state does require finalization.

Correct cleanup also makes static analysis and code review much easier, which matters in safety-critical firmware.

## Firmware Review Angle
Search every variadic function for `va_start` and verify cleanup on every path. Pay special attention to diagnostic code containing multiple failure exits. If a helper consumes a traversal, make ownership explicit in the API documentation.

## Compiler, ABI, and Toolchain Implications
`va_end` is compiler/libc/ABI machinery. A toolchain can lower it to no instructions, but another target may require meaningful state finalization. This is exactly why source code should use the standard macro rather than relying on observed generated assembly.

## Performance, Memory, Timing, and Power
When `va_end` expands to no work, its runtime cost is zero; when the ABI requires cleanup, there can be a small cost. The more significant performance issue is generally the total variadic traversal and formatting path.

Do not remove `va_end` merely because a current compiler emits no instruction for it.

## Verification / Debugging
Use static analysis or code review to identify every `va_start` without a matching `va_end`. Add tests for early-return and error paths. Build with more than one compiler where portability matters.

When investigating an optimization-sensitive issue, compare generated code but preserve the source-level lifecycle contract regardless of whether the current implementation emits instructions.

## Safety, Security, and Reliability
Consistent cleanup prevents target-specific lifecycle defects and makes ownership of variadic state explicit. This is particularly important in shared logging libraries used by multiple firmware components.

## Trade-offs and Alternatives
* **Use `va_end` always:** it is cheap insurance for portability and required lifecycle correctness.
* **Do not replace it with:** casts, manual stack restoration, or implementation-specific cleanup.
* **Alternative API design:** avoid variadic traversal entirely when a typed record can express the interface.

## Staff-Level Takeaway
`va_end` is not optional boilerplate. It closes an ABI-dependent resource/lifetime contract. A Staff engineer should review variadic functions as resource-management code: every initialization has a clear owner, every path reaches cleanup, copies have independent lifetimes, and no traversal crosses its valid execution context.

## Related Concepts
* [[00_Chapter_Index]]
* [[01_va_list]]
* [[02_va_start]]
* [[03_va_arg]]
* [[09_ABI_details]]
