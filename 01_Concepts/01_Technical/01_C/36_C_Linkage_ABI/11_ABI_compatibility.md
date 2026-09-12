# ABI compatibility

> Canonical C topic note — chapter 36.

## Definition
**ABI compatibility** means separately built components agree on the machine-level contract needed to exchange calls, objects and data. It is broader than source compatibility. Two programs can compile successfully while remaining ABI-incompatible because of differences in calling convention, data layout, alignment, symbol binding, floating-point mode, compiler options or runtime assumptions.

## Mechanism and language rules
ABI compatibility can involve:

- fundamental type sizes and alignment;
- structure/union layout and padding;
- enum representation where implementation-dependent;
- calling convention and register preservation;
- argument and return classification;
- name/symbol conventions;
- object visibility and linkage;
- floating-point ABI;
- thread-local storage and runtime conventions;
- compiler-generated initialization/destruction or unwind metadata where applicable.

ISO C guarantees source-language semantics, not a universal binary interface. A project therefore needs a specific ABI specification for each deployment boundary.

## Embedded implications
Firmware commonly has ABI boundaries between bootloader and application, ROM libraries and application code, vendor SDK and customer code, multiple compiler versions, and secure/non-secure execution domains.

A source-compatible change such as:

```c
typedef struct {
    uint32_t id;
    uint32_t flags;
} config_t;
```

becoming a larger structure can break a precompiled consumer even if both source trees still compile independently.

### Firmware review angle
Pin architecture, ABI options and compiler configuration in the build system. Record structure sizes/offsets with compile-time checks. For deployed binary interfaces, maintain ABI versioning and compatibility tests instead of relying on source review alone.

## Edge cases and failure modes
Typical ABI breaks include:

- changing a public struct's member order/type;
- changing packing or alignment options;
- switching hard-float/soft-float modes;
- changing calling-convention attributes;
- mixing incompatible runtime libraries;
- removing or renaming exported symbols;
- compiling one component with a different architecture extension that changes register conventions.

A linker resolving a symbol proves only that the names matched. It does not prove parameter types, structure layout or register conventions match.

## Example pattern
```c
_Static_assert(sizeof(config_t) == 8, "ABI: config_t size changed");
_Static_assert(offsetof(config_t, flags) == 4, "ABI: flags offset changed");
```

Such checks protect known layout contracts, but they do not replace full ABI validation.

## Verification / debugging
Use ABI-dump tools where available, compiler record-layout output, symbol-table comparisons, disassembly, and cross-version integration tests. Keep a small binary-compatibility test suite that builds producer and consumer independently.

Staff-level questions:
- Which boundaries must remain binary-compatible?
- What exact ABI version is deployed?
- Which source changes are ABI breaks?
- Can the boundary use opaque handles instead of exposing layouts?
- Is there an automated compatibility gate in CI?

## Staff-level takeaway
ABI compatibility is a **system property**, not a compiler switch. Treat binary interfaces as versioned contracts and verify them with layout, symbol, calling-convention and integration evidence.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
