# Unused diagnostics

> Canonical C topic note — chapter 35.

## Definition
Unused diagnostics are compiler or static-analysis warnings for declarations, parameters, labels, expressions, or other entities that appear not to contribute to a program. C itself does not define a universal “unused” diagnostic; these are implementation/toolchain diagnostics intended to expose dead code, forgotten outputs, incomplete refactoring, or suspicious interfaces.

## Mechanism and language rules
Common diagnostics include unused variables, parameters, functions, labels, and values. Whether an entity is considered used depends on the compiler's semantic analysis and options. `(void)x;` is a conventional explicit-use idiom for an intentionally unused parameter, although project-specific attributes may be clearer.

```c
static void callback(void *context)
{
    (void)context;
}
```

Do not silence a warning by changing code semantics. A compiler may still remove genuinely dead objects during optimization, while warnings often operate before or alongside optimization analysis.

### What to reason about
- Determine whether “unused” indicates a real defect or intentional API shape.
- Distinguish compile-time diagnostics from dead-code elimination.
- Prefer local, documented suppression over global disabling.
- Check generated/configuration-dependent code before assuming a warning is universally valid.

## Embedded implications
Unused code and data can consume review attention and, depending on linkage and toolchain behavior, flash/RAM. More importantly, an unused variable may reveal a missing error check, a stale hardware status read, or a configuration path that was accidentally disconnected.

### Firmware review angle
Use strict warnings in CI, but define a documented exception mechanism for hardware callbacks, RTOS entry points, linker-retained symbols, startup hooks, and conditionally compiled interfaces. Check map files to verify that supposedly unused objects are actually absent when size matters.

## Edge cases and failure modes
`volatile` reads can have intentional side effects even when the resulting value is unused. Conversely, reading a non-volatile value and discarding it is generally not a substitute for an intended hardware access. Taking an address can count as use without proving that the pointee is meaningfully consumed.

Beware warning suppression macros that hide real defects in nearby code.

## Example pattern
```c
void isr_entry(void *arg)
{
    (void)arg; /* Required by the common ISR ABI, intentionally unused. */
    clear_irq_flag();
    service_irq();
}
```

## Verification / debugging
Build with warnings such as `-Wall -Wextra` and the project's stricter unused diagnostics. Review every suppression. Use link maps and `nm`/object inspection to distinguish source-level unused entities from symbols intentionally retained by the image.

## Staff-level takeaway
Treat unused diagnostics as design feedback, not cosmetic noise. A mature codebase can explain every intentional unused entity and keeps the warning budget near zero.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
