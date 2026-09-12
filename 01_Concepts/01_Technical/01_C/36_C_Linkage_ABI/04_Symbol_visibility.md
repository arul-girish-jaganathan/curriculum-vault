# Symbol visibility

> Canonical C topic note — chapter 36.

## Definition
**Symbol visibility** controls which linker symbols are exposed to other objects, shared libraries, dynamic loaders, or tooling. ISO C does not define ELF visibility, DLL exports, hidden symbols, or dynamic symbol tables. These are ABI/toolchain concepts layered on top of C linkage.

Do not equate visibility with linkage: internal linkage (`static`) prevents cross-translation-unit references by the C language model, while visibility mechanisms can restrict or shape exposure of entities that otherwise have external linkage.

## Mechanism and language rules
A public API might be declared normally:

```c
void device_init(void);
int device_read(uint8_t *dst, size_t n);
```

A GCC/Clang ELF build may additionally use attributes such as `visibility("hidden")` or a linker version script. A Windows-oriented build may use `__declspec(dllexport)`/`dllimport`. These are implementation-specific.

Typical visibility classes include:

- **default** — potentially exported and preemptible in shared-object environments;
- **hidden** — not exported for normal dynamic symbol lookup;
- **protected** — exported but with special local binding semantics on supported systems;
- platform-specific export/import mechanisms.

Static embedded firmware often has no dynamic loader, but visibility still matters for symbol namespace hygiene, link-time optimization, map readability, binary interfaces, and library composition.

## Embedded implications
Reducing externally visible symbols can improve modularity and sometimes code generation. It also prevents accidental dependencies on private functions/data when a reusable library is distributed as an object archive or binary.

For firmware libraries, a deliberate public/private policy is valuable:

```c
/* public header */
void uart_init(void);
int uart_write(const void *data, size_t n);
```

Private helpers can use file-scope `static`, while cross-file implementation symbols can use an explicit visibility policy when the platform supports it.

### Firmware review angle
Treat the exported-symbol list as part of the interface. Compare symbol tables between releases to catch accidental API growth, symbol removal, or binding changes. For shared libraries, visibility can affect relocation, interposition and startup/runtime lookup; for bare-metal firmware, inspect the final image and archive extraction behavior.

## Edge cases and failure modes
A declaration being present in a public header does not guarantee that the final binary exports the symbol. Conversely, a symbol may become externally visible accidentally even though no public header documents it.

Common problems include:

- relying on platform visibility attributes in portable C;
- hiding a symbol that another image component legitimately references;
- assuming hidden visibility fixes an incompatible ABI;
- allowing implementation symbols to become contractual APIs;
- changing export lists without considering bootloader/application compatibility.

Visibility does not make a function thread-safe, reentrant, immutable, or secure. It only changes name exposure/binding at the toolchain boundary.

## Example pattern
```c
/* API boundary */
void sensor_start(void);

/* Implementation detail */
static void configure_clock(void)
{
    /* ... */
}
```

Prefer language-level internal linkage where it is sufficient; add platform visibility controls when a binary/shared-library boundary requires them.

## Verification / debugging
Use the compiler's symbol-dump tool, linker map, `nm`, `readelf -Ws`, or platform equivalents. Maintain an expected export list for reusable libraries. In CI, fail when private symbols unexpectedly become part of the supported ABI.

Staff-level questions:
- What is the supported binary interface?
- Which symbols are intentionally exported?
- Which boundary is static-link, dynamic-link, bootloader, or plugin based?
- Could internal linkage remove accidental coupling?
- Are visibility changes compatible with deployed consumers?

## Staff-level takeaway
Visibility is **interface governance at the binary boundary**. Keep the public surface intentionally small, distinguish it from C linkage, and verify the actual symbol table rather than trusting source-level declarations.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
