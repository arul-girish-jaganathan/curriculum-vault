# deprecated-style attributes

> Canonical C topic note — chapter 35.

## Definition
Deprecation marks an API as obsolete or discouraged while preserving it for compatibility. C23 provides standard attribute syntax such as `[[deprecated]]` and `[[deprecated("use new_api")]]`. Older code frequently uses compiler extensions such as `__attribute__((deprecated))` or `__declspec(deprecated)`.

Deprecation is primarily a source-compatibility and migration tool. It does not automatically remove the symbol, change its ABI, or make its implementation unsafe.

## Mechanism and language rules
Attributes can be attached to declarations such as functions, types, variables, or other entities where permitted by the language and implementation. A compiler can diagnose uses of a deprecated entity, usually with a warning.

```c
[[deprecated("use driver_read_v2")]]
int driver_read(int reg);
```
The diagnostic policy is compiler/build dependent. A project may promote deprecation warnings to errors, suppress them temporarily, or enforce them only in selected modules.

### What to reason about
- Deprecation does not itself create a runtime check.
- Keep the replacement API documented and migration-friendly.
- Consider ABI, binary compatibility, and header visibility separately from source warnings.
- Do not confuse deprecation with removal: old consumers may still exist.

## Embedded implications
Deprecation is valuable in long-lived firmware where APIs survive across bootloader, application, BSP, driver, and product generations. It can steer developers away from unsafe register interfaces, obsolete calibration formats, blocking APIs, or non-deterministic utilities without breaking existing products immediately.

### Firmware review angle
Define a staged policy: warn, measure remaining usage, migrate, then fail builds, and finally remove. Check generated code and vendor headers because external deprecation annotations may differ across compiler families.

## Edge cases and failure modes
Over-deprecating low-level interfaces can create warning fatigue. A deprecated function may still be the only supported interface on an older target, so migration needs explicit platform conditions. Suppressing every deprecation warning globally defeats the mechanism.

Also remember that attributes can be ignored or unsupported by older toolchains unless wrapped in portability macros.

## Example pattern
```c
#if defined(__GNUC__)
#define DEPRECATED(msg) __attribute__((deprecated(msg)))
#else
#define DEPRECATED(msg)
#endif

DEPRECATED("use sensor_read_scaled")
int sensor_read_raw(int channel);
```

For modern C23-only code, prefer the standard spelling when the supported toolchain set is ready for it.

## Verification / debugging
Enable deprecation warnings in CI and track remaining call sites. Test both the old and replacement APIs during migration, especially when they share storage formats or hardware side effects.

## Staff-level takeaway
Deprecation is a controlled migration mechanism. The engineering question is not merely “how do we warn?” but “how do we move an ecosystem from an old contract to a better one without destabilizing shipped firmware?”

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
