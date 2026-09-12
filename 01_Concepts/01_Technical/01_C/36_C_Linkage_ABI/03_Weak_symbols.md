# Weak symbols

> Canonical C topic note — chapter 36.

## Definition
A **weak symbol** is a linker/toolchain feature in which a definition has lower precedence than a strong definition with the same symbol name. Weak binding is **not specified by ISO C**. It is commonly supplied through ELF toolchains, compiler attributes, assembler directives, or linker conventions.

This distinction matters: C defines declarations, definitions, linkage and types; the weak/strong resolution policy belongs to the implementation and binary toolchain.

## Mechanism and language rules
A common GCC/Clang-style pattern is:

```c
__attribute__((weak)) void board_hook(void)
{
    /* default implementation */
}
```

If another object provides a strong `board_hook`, the linker can select that definition. If no strong definition exists, the weak one may remain in the image.

Weak symbols are often used for default hooks, interrupt handlers, board overrides, startup callbacks, and optional platform services. They do not magically create a type-safe interface: every candidate definition still needs a compatible C declaration and ABI.

Important toolchain questions include whether multiple weak definitions are allowed, how archives are extracted, how weak undefined references are represented, whether section garbage collection removes an unused weak definition, and what happens for a weak data symbol. These are not portable C guarantees.

## Embedded implications
Weak hooks can make board ports convenient:

```c
void app_idle(void); /* documented extension point */
```

with a default weak implementation supplied by the platform layer. They can also be useful for startup and vendor SDK customization.

The danger is **silent fallback**. A missing override may still link successfully and execute the default handler, turning an integration error into runtime behavior. For safety-critical code, that is often undesirable.

Weak interrupt handlers deserve special care: vector-table generation, section placement, aliasing, startup code and linker scripts can all affect whether the expected handler is actually installed.

### Firmware review angle
Document every weak symbol as a deliberate extension point. Inspect the final map/symbol table, not just source declarations. Confirm which implementation won and test both “override present” and “override absent” cases. Build with identical linker scripts and startup objects across configurations.

## Edge cases and failure modes
Common traps:

- assuming weak linkage is portable C;
- defining a weak object in a header and unintentionally creating multiple candidates;
- relying on link order to select behavior without documenting it;
- assuming an undefined weak reference behaves like a normal unresolved reference;
- using weak symbols to hide required dependencies;
- changing a function signature while the linker still resolves the symbol name.

A weak symbol is also not the same as C `static`. `static` creates internal linkage; weak binding changes linker resolution priority.

## Example pattern
```c
/* platform_default.c */
__attribute__((weak)) void platform_fault_hook(unsigned code)
{
    (void)code;
}

/* application.c */
void platform_fault_hook(unsigned code)
{
    /* intentional application override */
    log_fault(code);
}
```

The project should explicitly define which toolchain feature provides the weak behavior.

## Verification / debugging
Inspect `nm`, `readelf -Ws`, the linker map, or the target toolchain's equivalent. Verify the symbol binding and final address. Add a build test that intentionally omits the override and decides whether fallback is acceptable.

Staff-level questions:
- Is the fallback safe if the override is missing?
- Can a required dependency be made a link-time error instead?
- Is the selection deterministic across linkers and LTO modes?
- Is the ABI documented?
- Can a generated interface or explicit registration mechanism be clearer?

## Staff-level takeaway
Weak symbols are powerful **link-time extension mechanisms**, not a C language feature. Use them deliberately, verify final symbol resolution, and avoid using silent fallback where a missing implementation should fail the build.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
