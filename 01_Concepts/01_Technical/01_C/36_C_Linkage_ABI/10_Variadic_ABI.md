# Variadic ABI

> Canonical C topic note — chapter 36.

## Definition
A **variadic ABI** defines how arguments beyond the named parameters of a variadic function are physically passed and later recovered by `va_list` machinery. ISO C specifies the `stdarg.h` interface and default argument promotions; register-save areas, overflow areas, stack alignment and register allocation are ABI/compiler details.

## Mechanism and language rules
Consider:

```c
void logf(const char *fmt, ...);
```

The caller applies default argument promotions to variadic arguments. For example, `float` becomes `double`, and integer types subject to integer promotion become `int` or `unsigned int` as appropriate. The callee initializes a `va_list` with `va_start` and retrieves arguments with `va_arg` using the expected promoted type.

An ABI may pass early arguments in registers and later arguments in stack memory. A variadic function can therefore need metadata or state describing where the next unnamed argument resides. On some architectures, floating-point and integer arguments use separate register classes, requiring the compiler to preserve enough state for `va_arg` traversal.

`va_list` is intentionally opaque. Code must not inspect its representation or assume it is a pointer.

## Embedded implications
Variadic formatting is convenient but can be expensive in flash, cycles and stack. It is usually a poor primitive for tiny ISR logging paths. Prefer typed event records or fixed-format queues when deterministic behavior matters.

Hard/soft floating-point ABI differences can be especially important because variadic calls must obey the same ABI assumptions as their fixed arguments while applying default promotions.

### Firmware review angle
Audit every variadic API for bounded output, context restrictions, stack depth and ABI consistency. Keep `va_list` lifecycle correct across wrappers; use `va_copy` where required rather than assigning it blindly.

## Edge cases and failure modes
The most dangerous defect is a type mismatch:

```c
logf("%u", (uint64_t)counter); /* format does not match argument type */
```

The callee's `va_arg` operation must match the actual promoted argument type. A format string does not provide runtime type metadata; it is a convention.

Passing a `float` and retrieving `float` is wrong because the caller passes a promoted `double`. Narrow integer types may likewise arrive as `int`/`unsigned int`.

Forwarding a `va_list` twice without respecting its consumption state is another common bug. On implementations where `va_list` is not a simple pointer, assignment may not create an independent traversal state.

## Example pattern
```c
void trace(const char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    trace_v(fmt, ap); /* trace_v must document va_list consumption */
    va_end(ap);
}
```

If another traversal is required, use the implementation-supported `va_copy` facility.

## Verification / debugging
Test each supported ABI with mixed integer/floating arguments and inspect generated call sequences. Use compiler format attributes where available so the compiler can validate printf-like calls. Exercise wrappers under sanitizers on host builds, while remembering that sanitizer success does not prove target ABI compatibility.

Staff-level questions:
- Are variadic APIs necessary at this boundary?
- What are the promoted types?
- How are register and stack argument areas represented on the target ABI?
- Is the API safe in ISR/fault contexts?
- Can a typed event structure replace runtime type conventions?

## Staff-level takeaway
Variadic calls combine a **language-level promotion rule** with an **ABI-level argument transport mechanism**. Keep the interface narrow, type expectations explicit, and `va_list` handling strictly conforming.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
