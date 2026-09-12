# Inlining

## Definition
**Inlining** replaces a call to a function with code derived from the function body. It is primarily an optimization, although the C `inline` specifier also participates in the language's rules for function definitions and linkage. A critical distinction is that writing `inline` does **not** command the compiler to inline a call.

## Scope and boundaries
C semantics remain the source of truth. Whether a call is actually inlined depends on the implementation, optimization level, target cost model, visibility, translation-unit boundaries, recursion, code size, and build options. `static inline`, external `inline`, and compiler-specific attributes have different linkage/definition consequences.

## Mechanism and language rules
Inlining can remove call/return overhead, expose constants, propagate values, simplify branches, and enable further optimizations. For example:

```c
static inline uint32_t min_u32(uint32_t a, uint32_t b)
{
    return a < b ? a : b;
}
```

A compiler may emit a conditional move, branch, or other equivalent sequence, or keep an actual call. The source keyword is not an assembly directive.

### `static inline`
For header-defined small helpers, `static inline` is commonly used because each translation unit can have its own internal-linkage definition and the compiler can choose to inline it or emit a local out-of-line copy. This avoids an external definition requirement in many ordinary utility-header designs.

### External linkage
`inline` with external linkage is more subtle because ISO C defines rules for inline definitions and external definitions. Do not copy C++ inline habits into C without checking the C standard and compiler mode. A public API often has a normal external definition in one `.c` file and an appropriate declaration in its header.

## Embedded implications
Inlining can reduce function-call latency and improve ISR or driver hot paths, but aggressive inlining increases instruction-cache pressure, flash consumption, and sometimes worst-case timing variability. On small MCUs without caches, code-size growth can still increase flash fetch cost or affect placement. Inlining can also increase stack pressure when formerly shared code becomes duplicated or when larger expressions require more temporaries.

For register-level helpers, keep MMIO semantics explicit. Inlining a `volatile` access does not remove the access, but surrounding ordinary operations can still be optimized according to their contracts.

## Edge cases and failure modes
- Assuming `inline` guarantees inlining.
- Putting non-`static` definitions in headers and creating multiple-definition/linkage problems.
- Using compiler-specific `always_inline` without understanding diagnostics or build modes.
- Excessive inlining causing code bloat and worse instruction-cache behavior.
- Debugging optimized code as though every source call still exists.
- Measuring a microbenchmark in isolation and assuming the same result after LTO.

## Verification / debugging
Use compiler optimization reports when available, `-fdump-*`/remarks or equivalent diagnostics, and inspect assembly. Compare call graphs and code-size reports before and after a change. Confirm that public ABI remains unchanged if callers depend on the function symbol.

## Performance, memory, timing and power
Potential benefits include fewer branches, better constant propagation, better register allocation, and reduced call overhead. Costs include duplicated instructions, larger flash images, longer build times, and possible cache/I-cache degradation. On embedded targets, optimize based on measured hot paths rather than making every function inline.

## Staff-level takeaway
Treat inlining as a compiler cost-model decision. Design functions so that the optimizer *can* inline them when useful, but preserve clean interfaces and correct linkage. For performance claims, prove the generated code and measure the target; do not infer inlining from the presence of the keyword.