# Static assertions

> Canonical C topic note — chapter 35.

## Definition
A static assertion is a compile-time constraint that requires a constant expression to evaluate true. C11 introduced `_Static_assert`; C23 also provides `static_assert` as a keyword spelling. A failed assertion requires a diagnostic and prevents successful translation of that translation unit.

Static assertions are ideal for assumptions that must be true before firmware can be built: type sizes, offsets, enum ranges, protocol widths, configuration relationships, and ABI properties.

## Mechanism and language rules
A static assertion has the conceptual form:
```c
_Static_assert(sizeof(packet_header_t) == 8, "wire header size");
```
The controlling expression must be an integer constant expression. It is evaluated by the implementation during translation, not at runtime. It therefore cannot depend on runtime state, MMIO, variables, or function calls.

C11 permits an optional diagnostic string. C23 simplifies the spelling and permits `static_assert` directly. The expression tests the implementation's actual type/layout rules, making static assertions valuable at portability boundaries.

### What to reason about
- Ask whether the property is genuinely compile-time knowable.
- Use `sizeof`, `_Alignof`, `offsetof`, integer constants, and configuration macros carefully.
- Remember that a passing assertion proves only the stated property, not the entire design assumption.
- Place assertions near the declaration or interface whose invariant they protect.

## Embedded implications
Static assertions prevent an incorrect firmware image from being produced. Typical uses include:
```c
_Static_assert(sizeof(uint32_t) == 4, "unexpected uint32_t");
_Static_assert(offsetof(struct header, payload) == 12, "ABI drift");
_Static_assert(RING_SIZE && ((RING_SIZE & (RING_SIZE - 1)) == 0),
               "ring size must be power of two");
```
They are especially useful for DMA descriptors, memory-mapped register wrappers, persistent records, IPC packets, bootloader/application interfaces, and generated configuration.

### Firmware review angle
Check assertions under every supported compiler, architecture, packing option, ABI, and configuration. A layout assertion can expose accidental padding or packing differences before integration. Avoid asserting implementation properties unless portability requirements explicitly depend on them.

## Edge cases and failure modes
Do not confuse `_Static_assert` with `assert`: one fails the build, the other normally fails at runtime. Do not use a runtime variable in the controlling expression. Beware assertions whose truth changes with compiler options such as packing, ABI, language mode, or target architecture.

An assertion on `sizeof(struct)` can also be fragile if the structure contains implementation-dependent fields or is intended only as an internal object.

## Example pattern
```c
typedef struct {
    uint16_t id;
    uint16_t flags;
    uint32_t length;
} message_header_t;

_Static_assert(sizeof(message_header_t) == 8, "unexpected header layout");
```

## Verification / debugging
Compile representative configurations with all supported toolchains. Intentionally break each assertion in a test build and confirm that the compiler emits a diagnostic. For ABI-sensitive code, combine assertions with generated headers and binary/layout tests.

## Staff-level takeaway
Static assertions turn architectural assumptions into executable build-time contracts. Prefer them wherever a failure should be impossible to defer until runtime.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
