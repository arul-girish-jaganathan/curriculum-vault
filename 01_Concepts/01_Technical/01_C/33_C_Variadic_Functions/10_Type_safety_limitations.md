# Type-safety limitations

## Definition
C variadic functions intentionally weaken the compile-time type contract after the final named parameter. The compiler knows the declared parameters but, in general, cannot know the number, order, or types of arguments represented by `...`.

The callee therefore depends on an external contract such as a count, sentinel, format string, tag sequence, or documented convention. If caller and callee disagree, the program may have undefined behavior.

## Scope and Boundaries
* **Covers:** loss of static checking, type contracts, format checking, safer wrappers, and API design.
* **Does not cover:** the mechanics of `va_arg` in [[03_va_arg]] or the ABI implementation in [[09_ABI_details]].

## Why Does It Exist
Variadic interfaces are useful when an API genuinely needs variable argument counts, especially formatting and diagnostic systems. The trade-off is that C cannot express the complete runtime argument schema in an ordinary prototype.

## Mechanism and Language Rules
Compare:

```c
int add(int a, int b);
```

with:

```c
int log(const char *fmt, ...);
```

The first prototype lets the compiler diagnose many wrong calls. The second only exposes `fmt`; the remaining arguments are checked by convention or by additional compiler-specific format analysis.

### What to reason about
- How does the callee know the argument count?
- How does it know each argument's type?
- Does the compiler have special knowledge of the interface?
- Are default argument promotions documented?
- Can malformed input cause an out-of-bounds traversal?
- Can the interface be replaced by a typed structure without losing useful flexibility?

## Examples

### Explicit tagged contract
```c
#include <stdarg.h>

enum value_kind { VALUE_INT, VALUE_DOUBLE };

static void consume(enum value_kind kind, ...)
{
    va_list ap;
    va_start(ap, kind);

    if (kind == VALUE_INT)
        (void)va_arg(ap, int);
    else if (kind == VALUE_DOUBLE)
        (void)va_arg(ap, double);

    va_end(ap);
}
```

The tag documents the expected type, although the compiler still cannot fully prove that every caller obeys it.

### Stronger alternative
```c
struct value {
    enum value_kind kind;
    union {
        int i;
        double d;
    } data;
};
```

A typed object makes the data contract explicit and inspectable by ordinary C tooling.

## Undefined, Unspecified, and Implementation-Defined Behavior
* The absence of static type checking does not make mismatched `va_arg` requests implementation-defined; incompatible retrieval can be undefined behavior.
* Format-string diagnostics are compiler features, not a guarantee provided for arbitrary user-defined variadic protocols.
* Runtime tags reduce ambiguity but cannot repair a caller that supplies the wrong physical type.
* Equal size or identical representation is not sufficient to establish a valid variadic type contract.

## Edge Cases and Failure Modes
* **Wrong count:** traversal reads beyond the actual arguments.
* **Wrong type:** register/stack consumption may become desynchronized.
* **Promotion mismatch:** `float` arrives as `double`; narrow integers may arrive as promoted integers.
* **Format injection:** user-controlled format strings can read or write unintended data through formatting directives.
* **Cross-module drift:** caller and callee may evolve separately and silently disagree about the argument schema.
* **Disabled logging:** a compile-time-disabled macro must not evaluate expensive or side-effecting arguments accidentally.

## Embedded Implications
In embedded products, weakly typed variadic interfaces are particularly risky when they cross teams, firmware modules, bootloader/application boundaries, or persistent diagnostic protocols.

A fixed event structure gives static size, explicit ownership, easier serialization, and predictable memory use. Variadic logging is best kept at the human-readable diagnostic boundary.

## Firmware Review Angle
Ask whether every variadic interface has a written schema. Require examples for every supported argument sequence. Check whether the interface can be called from ISR, boot, or fault contexts and whether the output path has deterministic resource bounds.

## Compiler, ABI, and Toolchain Implications
Compiler format attributes can restore useful static checking for printf-like interfaces. Static analyzers can additionally enforce project-specific wrappers and argument conventions.

However, no warning mechanism replaces the ABI contract. The exact target compiler and architecture still determine how valid arguments are passed.

## Performance, Memory, Timing, and Power
Type checking has essentially no runtime cost, but variadic flexibility can increase runtime parsing, stack usage, and code size. Typed records often enable simpler encoders and better optimization.

## Verification / Debugging
Use compile-time tests that intentionally contain wrong format types and verify that the build fails or warns under the project toolchain. Unit-test all runtime tag combinations and malformed counts.

Static analysis should be part of CI, and cross-compiler tests should be used when binary compatibility matters.

## Safety, Security, and Reliability
For security-sensitive code, minimize untyped variadic boundaries. Treat external data as untrusted and validate counts, tags, and lengths before consuming anything.

For safety-critical code, prefer interfaces where the compiler can prove parameter types and object bounds.

## Trade-offs and Alternatives
* **Variadic:** maximum source-level flexibility, weakest static contract.
* **Typed structure:** explicit schema, easier testing and serialization.
* **Tagged union:** flexible alternatives with explicit runtime type.
* **`_Generic`:** compile-time selection for type-based wrappers without runtime type erasure.
* **Generated code:** useful when many typed combinations must be supported consistently.

## Staff-Level Takeaway
Variadic C is a deliberate escape from ordinary static typing. A Staff engineer should ask what safety mechanism replaces the missing prototype: format validation, tags, generated wrappers, or a typed record. If no such mechanism exists, the interface is relying on convention alone and should be treated as a high-risk architectural boundary.

## Related Concepts
* [[00_Chapter_Index]]
* [[03_va_arg]]
* [[05_Default_argument_promotions]]
* [[06_Format_strings]]
* [[07_printf_like_APIs]]
* [[08_Variadic_macros]]
* [[09_ABI_details]]
