# Build-mode assertions

> Canonical C topic note — chapter 35.

## Definition
Build-mode assertions are compile-time checks that validate configuration assumptions for a particular firmware variant: target MCU, feature set, memory map, ABI, safety profile, debug mode, or manufacturing configuration. They combine `_Static_assert`, preprocessor conditionals, and project configuration to reject invalid combinations early.

## Mechanism and language rules
Use preprocessor checks when a symbol's presence controls compilation:
```c
#if FEATURE_DMA && !FEATURE_CACHE_MAINTENANCE
#error "DMA configuration requires cache maintenance support"
#endif
```
Use `_Static_assert` when the compiler can evaluate a typed constant expression:
```c
_Static_assert(RX_SIZE <= 4096u, "RX_SIZE exceeds supported range");
```
`#error` and `_Static_assert` are complementary: the former is preprocessing/configuration validation, the latter is language-level constant-expression validation.

### What to reason about
- Validate mutually exclusive features and required dependencies.
- Prefer typed compile-time checks over string or textual tricks when possible.
- Make configuration failures deterministic and readable.
- Ensure generated configuration headers are reproducible and versioned.

## Embedded implications
Build matrices can explode as products acquire MCU variants, communication options, memory sizes, boot modes, and safety levels. Build-mode assertions prevent unsupported combinations from silently producing an image that boots but behaves incorrectly.

Typical checks include flash/RAM budgets, peripheral availability, DMA alignment, interrupt priorities, queue sizes, feature dependencies, and protocol configuration.

### Firmware review angle
Treat the configuration space as an architectural model. CI should compile representative and boundary configurations, including intentionally invalid configurations to prove that guards fire.

## Edge cases and failure modes
A configuration macro can be defined differently in different translation units, producing inconsistent declarations or behavior. Generated headers can also become stale relative to the build system.

Avoid checks that merely assert the current implementation instead of the product requirement. Also avoid a huge collection of duplicated `#if` logic that makes configuration behavior impossible to reason about.

## Example pattern
```c
#if defined(TARGET_MCU_A)
#define FLASH_BYTES  (512u * 1024u)
#elif defined(TARGET_MCU_B)
#define FLASH_BYTES  (1024u * 1024u)
#else
#error "Unsupported target"
#endif

_Static_assert(FLASH_BYTES >= REQUIRED_IMAGE_BYTES,
               "target flash is too small");
```

## Verification / debugging
Generate a configuration manifest during CI. Compile all supported product profiles and several invalid combinations. Keep compiler command lines and generated headers as build artifacts so a released image can be reconstructed.

## Staff-level takeaway
Build assertions convert configuration complexity into explicit, reviewable constraints. The goal is not maximum preprocessor usage; it is making invalid product configurations impossible to ship.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
