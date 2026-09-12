# Default argument promotions

## Definition
Default argument promotions are the conversions applied to arguments passed through `...` when no parameter type is available to specify the destination type. Before a variadic argument is consumed, `float` is promoted to `double`, and integer types subject to integer promotions are promoted according to the integer-promotion rules.

These promotions are a central part of variadic correctness. The type originally written at the call site is not necessarily the type that `va_arg` must request.

## Scope and Boundaries
* **Covers:** integer promotions, floating promotion, variadic calls, `va_arg` matching, and common type-contract mistakes.
* **Does not cover:** general arithmetic conversions outside variadic calls or the complete ABI, which is covered in [[09_ABI_details]].

## Why Does It Exist
Older C interfaces and variadic functions need a predictable representation for arguments when the callee has no declared parameter type. Promotions reduce the number of narrow scalar representations that a variadic callee must handle and integrate variadic calls with C's ordinary expression conversion rules.

## Mechanism and Language Rules
Consider:

```c
static void inspect(unsigned tag, ...)
{
    va_list ap;
    va_start(ap, tag);

    int i = va_arg(ap, int);
    double d = va_arg(ap, double);

    (void)i;
    (void)d;
    va_end(ap);
}

inspect(0U, (short)-3, 1.5f);
```

The `short` argument undergoes integer promotion, commonly becoming `int`, while the `float` becomes `double`. Therefore the callee must request `int` and `double`, not `short` and `float`.

### What to reason about
- Determine the type after default argument promotions, not merely the source spelling at the call site.
- Integer promotions depend on rank and representability; do not reduce them to "everything becomes int" without checking `int`/`unsigned int` representability.
- `float` always promotes to `double` in this context.
- `double` does not promote further to `long double`.
- Arrays and functions undergo their normal argument transformations to pointers before being passed.
- A prototype's named parameters are not subject to the same variadic omission of declared types; do not confuse ordinary parameter conversion with default argument promotions.

## Examples

### Promotion table
| Source argument | Variadic type to expect |
|---|---|
| `char` / `signed char` | usually `int` |
| `unsigned char` | `int` or `unsigned int`, depending on representability/rules |
| `short` | usually `int` |
| `unsigned short` | `int` or `unsigned int` |
| `float` | `double` |
| `double` | `double` |
| `long double` | `long double` |

### Width-safe interface
For application-defined records, make the exact type explicit rather than depending on assumptions about underlying typedefs:

```c
static void log_value(unsigned kind, ...)
{
    va_list ap;
    va_start(ap, kind);

    switch (kind) {
    case 0:
        /* Contract says the caller supplies an int. */
        (void)va_arg(ap, int);
        break;
    case 1:
        (void)va_arg(ap, double);
        break;
    default:
        break;
    }

    va_end(ap);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
* Retrieving a promoted argument using its pre-promotion type can be undefined behavior.
* Assuming every unsigned narrow integer promotes to `int` is incorrect; the promotion depends on whether `int` can represent all values of the original type.
* Fixed-width typedefs such as `uint32_t` have implementation-defined underlying types, so a variadic API should define the actual expected type carefully.
* Promotions do not make arbitrary type mismatches safe. Passing a pointer and retrieving an integer of the same size is still invalid.

## Edge Cases and Failure Modes
* **`uint8_t`:** often aliases `unsigned char`; it may therefore arrive as `int` rather than `uint8_t`.
* **`uint32_t`:** may be `unsigned int` or another unsigned integer type. The API contract must match the actual type used by the caller.
* **`float`:** always arrives as `double` in an ordinary variadic argument.
* **Enums:** their compatible integer type and promotion behavior must be considered rather than assuming a fixed width.
* **Bit-fields:** when passed as variadic expressions, their integer-promotion behavior matters.
* **Variadic macros:** macro expansion occurs before the actual function call; do not confuse macro argument handling with C's runtime variadic calling rules.

## Embedded Implications
Promotion can increase argument width and register/stack traffic. A `float` becomes `double`, which can be materially more expensive on an MCU without efficient double-precision hardware.

A logging API that accepts many small integer arguments may also consume more register/stack bandwidth than its source code suggests. For high-frequency events, typed packed records can be more deterministic.

## Firmware Review Angle
For every variadic API, document the promoted type expected by the callee. Review both sides of the interface and compile on all supported architectures. Pay attention to ABI changes where integer and floating-point argument classes differ.

## Compiler, ABI, and Toolchain Implications
The compiler performs the language-level promotions and then maps the resulting types to the target ABI. This affects register classes, stack slots, alignment, and the behavior of `va_arg`.

Compiler diagnostics can catch some format mismatches but cannot generally prove arbitrary user-defined variadic contracts. Explicit wrappers with typed parameters are therefore valuable.

## Performance, Memory, Timing, and Power
The promotion itself is usually inexpensive, but widened values can increase data movement and floating-point work. On small MCUs, passing `float` through a variadic interface may pull in double-precision formatting or helper routines if it is subsequently formatted.

## Verification / Debugging
Create tests with `char`, `unsigned char`, `short`, `unsigned short`, `int`, fixed-width integers, `float`, `double`, pointers, and enums. Verify the exact `va_arg` type on every supported compiler/ABI.

When diagnosing a crash, inspect the call-site argument registers/stack and compare them with the callee's `va_arg` expectations.

## Safety, Security, and Reliability
Default promotions are predictable, but they do not provide runtime type metadata. A robust API must still communicate the expected type sequence through a count, tag, format, or fixed schema.

## Trade-offs and Alternatives
* **Use variadic promotions:** when interoperating with standard variadic interfaces.
* **Avoid relying on them as a type system:** define typed wrappers where possible.
* **Alternatives:** explicit parameter structures, tagged unions, generated logging calls, or `_Generic` wrappers that select typed implementations at compile time.

## Staff-Level Takeaway
The most dangerous variadic misconception is "the caller passed a `uint8_t`, so `va_arg(ap, uint8_t)` is correct." The real contract is the promoted type. A Staff engineer should reason from source expression → default promotion → ABI classification → `va_arg` request, and test that chain across every supported target.

## Related Concepts
* [[00_Chapter_Index]]
* [[01_va_list]]
* [[03_va_arg]]
* [[06_Format_strings]]
* [[09_ABI_details]]
