# _Static_assert

> Canonical C topic note — chapter 35.

## Definition
`_Static_assert` is the C11 language construct for a compile-time assertion. Its condition must be an integer constant expression whose value is nonzero. If it is zero, the implementation issues a diagnostic and the translation cannot successfully complete for that construct.

## Mechanism and language rules
The syntax is:
```c
_Static_assert(constant_expression);
_Static_assert(constant_expression, "message");
```
The second form is the familiar C11 form; C23 adds `static_assert` and modernizes the syntax. The condition is evaluated during translation. It has no runtime execution and introduces no runtime storage by itself.

Useful expressions include `sizeof(T)`, `_Alignof(T)`, `offsetof(T, member)`, integer constants, and preprocessor configuration values. Because it is a language constraint rather than a macro convention, the compiler can reason about the expression directly.

### What to reason about
- Ensure the expression is an integer constant expression.
- Understand which implementation properties are being frozen into the build.
- Keep messages useful because build failures should be diagnosable in CI and cross-toolchain environments.
- Distinguish standard guarantees from implementation-specific ABI assumptions.

## Embedded implications
`_Static_assert` is a powerful defense at hardware/software boundaries. For example, a driver can assert that register-width types have the intended size, a protocol can assert serialized structure assumptions, and a memory allocator can assert that block geometry is valid.

```c
_Static_assert(sizeof(uint32_t) == 4, "32-bit register type required");
_Static_assert((BUFFER_SIZE % 32u) == 0u, "DMA alignment requirement");
```
A failed assertion stops a bad configuration from reaching flashing, manufacturing, or field deployment.

### Firmware review angle
Test assertions across debug/release, target variants, compiler versions, packing options, endianness assumptions, and generated configurations. Avoid using them as a substitute for runtime validation of untrusted data.

## Edge cases and failure modes
A common mistake is assuming `_Static_assert` can test runtime state. It cannot. Another is asserting an accidental layout property that changes with ABI or compiler flags without documenting why that layout is required.

Be careful with preprocessor expressions whose type or value differs across targets. Also distinguish `sizeof(char) == 1`—guaranteed by C—from assumptions that a byte is eight bits.

## Example pattern
```c
struct dma_desc {
    uint32_t address;
    uint16_t length;
    uint16_t control;
};

_Static_assert(sizeof(struct dma_desc) == 8, "DMA descriptor ABI changed");
_Static_assert(_Alignof(struct dma_desc) >= 4, "DMA descriptor alignment too small");
```

## Verification / debugging
Use CI to compile every supported configuration. Deliberately violate assertions to verify that failures are caught at build time. For generated hardware descriptions, compare static assertions with linker/map-file checks so compile-time and image-level assumptions are both verified.

## Staff-level takeaway
`_Static_assert` is one of the simplest ways to move architectural risk from runtime to build time. Use it aggressively for invariants that the compiler can prove.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
