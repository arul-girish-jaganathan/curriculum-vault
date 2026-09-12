# Optimization-safe C

## Definition
**Optimization-safe C** is C whose behavior remains correct when a conforming compiler applies aggressive optimization. The goal is not to prevent optimization; it is to express object lifetime, aliasing, overflow assumptions, volatility, concurrency, ownership, and hardware interaction in ways the compiler is permitted to understand.

## Scope and boundaries
Optimization-safe code is well-defined code. It avoids relying on undefined behavior, unspecified evaluation order, accidental timing, debugger effects, or undocumented compiler behavior. Where implementation extensions are necessary, they are isolated and documented as toolchain contracts.

## Mechanism and language rules
Core practices include:

```c
/* Express intent instead of relying on optimizer folklore. */
static bool ready(const volatile uint32_t *status)
{
    return (*status & 1u) != 0u;
}
```

Use correct types, bounds, lifetime, alignment, and synchronization. Use `restrict` only when its no-alias contract is true. Use `_Atomic` and explicit memory orders for C concurrency. Use `volatile` for required volatile accesses, not as a substitute for synchronization.

### Avoid optimizer-dependent tricks
Do not depend on signed overflow wrapping, reading uninitialized objects, invalid pointer arithmetic, incompatible type punning, or “empty” delay loops. Such code may change behavior dramatically at higher optimization levels.

## Embedded implications
Optimization-safe firmware should survive changes in `-O0`/`-O2`/`-Os`, LTO, compiler version, and target configuration without semantic surprises. Hardware access must be specified at the appropriate abstraction layer: C volatile semantics, compiler barriers, CPU barriers, cache maintenance, DMA ownership, and peripheral requirements are separate contracts.

Keep timing requirements outside the assumption that a source loop or function consumes a fixed number of cycles. Use timers, hardware capture, RTOS scheduling primitives, or measured execution budgets.

## Edge cases and failure modes
- “Fixing” a race with volatile.
- Casting arbitrary bytes to a structure without alignment/representation analysis.
- Using `memcpy` into an object while ignoring lifetime or effective-type requirements.
- Assuming `const` means compile-time constant.
- Assuming `inline` means inlined.
- Assuming an optimizer setting is a correctness mechanism.

## Verification / debugging
Run warnings at a high level, static analysis, sanitizers on host builds, unit tests, boundary tests, and optimized production builds. Compare compiler versions when upgrading. Inspect assembly for critical paths and map files for placement. Use hardware tests for MMIO, DMA, cache, interrupt, and timing behavior.

## Performance, memory, timing and power
Well-defined code gives the compiler freedom to remove redundant work, propagate constants, vectorize, inline, and allocate registers effectively. This often produces better performance than manually restricting optimization. Excessive barriers, volatile qualifiers, aliasing ambiguity, and opaque interfaces can unnecessarily block those improvements.

## Staff-level takeaway
The best optimization-safe code makes **the real contract explicit and the false assumptions impossible**. Establish correctness first, then optimize measured bottlenecks. If a transformation appears to break valid code, preserve the minimal reproducer and investigate the language rule, compiler behavior, ABI, and target hardware separately.