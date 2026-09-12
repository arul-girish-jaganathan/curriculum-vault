# Compiler attributes

> Canonical C topic note — chapter 35.

## Definition
Compiler attributes are metadata attached to declarations or other language entities to influence diagnostics, optimization, code generation, section placement, calling conventions, or analysis. C23 standardizes an attribute syntax, but many useful attributes remain compiler- or platform-specific.

Examples include `[[deprecated]]`, `[[fallthrough]]`, `[[noreturn]]`, and implementation extensions such as GCC/Clang `__attribute__` forms.

## Mechanism and language rules
Attributes generally describe properties rather than execute operations. Their effect is defined by the language for standard attributes or by the compiler for extensions. Unsupported or incorrectly placed attributes can produce diagnostics or be ignored according to the implementation.

Common nonstandard properties include `packed`, `aligned`, `section`, `weak`, `used`, `format`, `interrupt`, `always_inline`, and visibility controls. These are powerful precisely because they cross the boundary between C semantics and toolchain behavior.

### What to reason about
- Identify whether an attribute is ISO C, compiler-specific, assembler/linker-specific, or vendor-specific.
- Check declaration placement and whether all translation units see the same attributes.
- Understand whether the attribute changes ABI, object layout, optimization assumptions, or only diagnostics.
- Never infer portability from identical syntax across compilers.

## Embedded implications
Attributes are fundamental in embedded systems: placing objects in flash/retention sections, aligning DMA buffers, describing interrupt handlers, preserving startup symbols, controlling packing, and expressing optimization intent.

A section attribute may require a matching linker-script rule. An alignment attribute may affect RAM usage. `packed` may create unaligned accesses with hardware-dependent cost or faults. `always_inline` may increase code size and does not override every compiler constraint.

### Firmware review angle
For each attribute, document the complete toolchain contract: compiler version, target ABI, linker behavior, debugger visibility, and fallback behavior. Verify map files and disassembly rather than trusting source annotations.

## Edge cases and failure modes
The most dangerous mistake is assuming an attribute is merely a hint when it actually changes ABI or object representation. Another is using a compiler extension in a public header without a portability abstraction.

Attributes can also become stale: an `aligned` requirement may no longer match DMA hardware, or a `section` annotation may survive while the linker script changes.

## Example pattern
```c
#if defined(__GNUC__)
#define DMA_ALIGNED(n) __attribute__((aligned(n)))
#else
#define DMA_ALIGNED(n)
#endif

static uint8_t dma_buffer[256] DMA_ALIGNED(32);
```

The real correctness proof must include the linker image and the hardware's actual alignment/cache requirements.

## Verification / debugging
Compile with warnings enabled, inspect object metadata with `readelf`/`objdump` where available, inspect the linker map, and verify generated instructions. Maintain compiler-specific attribute wrappers in one portability header.

## Staff-level takeaway
Attributes are contracts at the language/toolchain boundary. A Staff engineer should know exactly which layer consumes each attribute and what evidence proves its intended effect.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
