# External symbols

> Canonical C topic note — chapter 36.

## Definition
An **external symbol** is a linker-visible name associated with an object or function whose definition or reference can cross a translation-unit boundary. C's `extern` declaration gives a declaration external linkage in the cases where the language rules permit it; the actual symbol table, object format, relocation model, visibility attributes, and linker behavior are implementation/platform concerns.

Do not confuse **scope**, **storage duration**, **linkage**, and **symbol visibility**. A name may have file scope while having external or internal linkage, and a declaration can describe an entity without allocating storage.

## Mechanism and language rules
A typical pattern is:

```c
/* sensor.h */
extern volatile unsigned sensor_status;
void sensor_init(void);
```

```c
/* sensor.c */
volatile unsigned sensor_status;
void sensor_init(void) { /* ... */ }
```

The header provides declarations; exactly one program-wide definition should provide the external object unless a different valid definition arrangement is intended. For functions, a file-scope function declaration normally has external linkage unless `static` changes that linkage. For objects, `extern` can declare an existing object without defining it when no initializer is present.

Important distinctions:

- `extern int x;` at file scope normally declares `x`; it need not allocate storage.
- `int x;` at file scope without an initializer is a tentative definition under C rules; multiple tentative definitions may coalesce within the translation model, but a program still needs a compatible definition and must obey the language's linkage constraints.
- `extern int x = 1;` is a definition because the initializer requires storage to be defined.
- `static int x;` gives internal linkage rather than an external symbol usable by other translation units.
- A declaration must be compatible with the entity's type. Calling or accessing an entity through an incompatible declaration can produce undefined behavior or ABI corruption even if the linker resolves the spelling.

The linker operates after translation. It matches symbols and relocations according to the object-file format and toolchain. ISO C does not specify ELF symbol bindings, COFF records, relocation types, section names, archive extraction rules, or linker scripts.

## Embedded implications
External symbols are a central firmware integration mechanism. Drivers, board-support packages, startup code, middleware, bootloaders, and application modules frequently exchange symbols through headers and linker scripts.

A bad external declaration can cause:

- wrong register width or calling convention;
- incorrect data layout or alignment;
- relocation overflow on targets with limited address encoding;
- accidental RAM allocation instead of access to a linker-defined address;
- duplicate definitions or unresolved references;
- retention of otherwise dead code/data;
- ABI mismatch across compiler or library boundaries.

For MMIO, prefer a single authoritative declaration with the correct volatile-qualified integer type or vendor-provided definition rather than duplicating addresses manually.

### Firmware review angle
Check the map file and symbol table for every important external object/function. Verify section placement, address, size, binding, and whether the symbol unexpectedly became local, weak, hidden, discarded, or duplicated. Build debug and release images because optimization and section garbage collection can expose assumptions hidden by a debug build.

## Edge cases and failure modes
Common traps include declaring an object in a header as `int state;` instead of `extern int state;`, creating one definition per translation unit; mismatching `const`/qualifiers or structure declarations; assuming `extern` makes an object thread-safe; and assuming a linker-resolved name proves that the C types are compatible.

Another important boundary is linker-defined symbols. A linker script may expose symbols such as image boundaries to C, but those symbols are not ordinary C objects merely because a C declaration names them. Their address/value interpretation is toolchain-specific and must be documented.

## Example pattern
```c
/* api.h */
#ifndef API_H
#define API_H
extern unsigned boot_count;
void boot_record(void);
#endif

/* api.c */
#include "api.h"
unsigned boot_count;
void boot_record(void) { ++boot_count; }
```

The declaration is shared; the storage definition is owned by one translation unit.

## Verification / debugging
Use compiler warnings for incompatible declarations and duplicate definitions, inspect `nm`/`readelf` or the target equivalent, and inspect the linker map. A useful review experiment is to intentionally alter a declaration and verify that the build fails rather than silently producing an ABI mismatch.

Staff-level questions:
- Who owns the definition?
- Is the symbol part of a stable interface or an accidental implementation detail?
- What exact ABI crosses the boundary?
- Is the symbol reachable from unwanted modules?
- Can internal linkage reduce coupling and code-size exposure?

## Staff-level takeaway
Treat every external symbol as an **ABI and ownership boundary**, not merely a name that makes the linker happy. The strongest design makes ownership explicit, declarations canonical, visibility intentional, and the resulting binary verifiable.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
