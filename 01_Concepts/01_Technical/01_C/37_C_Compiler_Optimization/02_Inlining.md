# Inlining

> Canonical C topic note — chapter 37.

## Definition
Inlining replaces a function call with an implementation-derived expansion of the function body. In C, `inline` is primarily a linkage/definition-related language facility and an optimization hint; it does **not** require the compiler to inline a call. Modern compilers make the optimization decision from cost models, optimization level, profile data, visibility, and target architecture.

## Mechanism and language rules
Inlining can remove call/return overhead and expose caller arguments and surrounding control flow to constant propagation, dead-code elimination, register allocation, and vectorization. A function can therefore be optimized differently when inlined than when emitted as an out-of-line function.

```c
static inline uint32_t set_bit(uint32_t v, unsigned n)
{
    return v | (UINT32_C(1) << n);
}
```

`static inline` in a header is common because each translation unit can have its own internal definition without exporting one external symbol. Plain `inline` has subtle C linkage rules; do not assume C++ inline semantics. The exact emitted out-of-line copy is implementation-dependent.

### Cost model
Inlining is a trade-off: fewer calls and more optimization opportunity versus larger code, instruction-cache pressure, flash usage, register pressure, and potentially worse timing. A larger function can increase stack usage after expansion even if the source function itself has a small frame.

### Recursion and indirect calls
Recursive functions cannot be blindly expanded indefinitely. Function pointers can prevent direct inlining unless the compiler proves the target. LTO can recover opportunities across translation units.

## Embedded implications
On MCUs, call overhead can matter in tiny hot paths, but flash is often scarcer than CPU cycles. Inlining a large parser or protocol state machine can increase image size and instruction-cache misses. For hard real-time code, measure worst-case timing after final link rather than assuming “inline is faster.”

Headers containing many `static inline` functions can multiply generated code across translation units. Link-time identical-code folding or other toolchain features may reduce duplication, but this is not a portable C guarantee.

## Edge cases and failure modes
- Treating `inline` as a mandatory optimization.
- Putting large non-static inline definitions in public headers and creating linkage problems.
- Ignoring C's distinct inline-definition rules.
- Assuming inlining always reduces latency.
- Breaking debugability or traceability with excessive expansion.
- Measuring only average execution time instead of code size and worst-case latency.

## Verification / debugging
Inspect compiler optimization reports and disassembly. Compare code size with and without the candidate function. Measure cycle counts on the target for hot paths and inspect stack usage. Test both LTO and non-LTO builds when they are production options.

## Staff-level takeaway
Choose inlining from evidence: hotness, call overhead, code size, cache behavior, ABI boundaries, and timing requirements. `static inline` is a useful source-organization pattern, but the optimizer remains in control of the final machine code.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
