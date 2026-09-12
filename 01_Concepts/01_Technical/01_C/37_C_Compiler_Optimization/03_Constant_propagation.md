# Constant propagation

## Definition
**Constant propagation** is an optimization in which a compiler tracks values known to be constant and substitutes those values into later expressions. It is closely related to constant folding, copy propagation, dead-code elimination, and branch simplification. The optimization is valid only when the compiler can prove the relevant value and side-effect rules.

## Scope and boundaries
The C programmer does not need to manually perform every constant calculation. The important job is to express correct invariants using appropriate types, `const`, enumerations, macros, static initialization, and well-defined control flow. `const` itself is primarily a type qualifier, not a universal promise that an object is compile-time constant.

## Mechanism and language rules
Consider:

```c
static int mode_value(int mode)
{
    if (mode == 3)
        return 100;
    return 0;
}
```

If a caller passes a provably constant `3`, interprocedural optimization may replace the call with `100`. Even without inlining, local analysis can propagate constants through basic blocks.

### Constant folding versus propagation
Constant folding evaluates an expression whose operands are known constants. Propagation moves a known value to another use. Example:

```c
int f(void)
{
    int x = 8;
    int y = x * 4;
    return y + 1;
}
```

A compiler can propagate `8`, fold `8 * 4`, and ultimately return `33`.

### Control-flow simplification
Known conditions can remove branches:

```c
if (CONFIG_FEATURE == 0) {
    /* code can disappear when the configuration is compile-time known */
}
```

This is especially powerful in embedded configuration code when constants are visible to the optimizer.

## Embedded implications
Compile-time-known hardware configuration can eliminate unused driver paths, reduce flash, and shorten startup. A constant buffer length can enable bounds simplification; a fixed protocol field can eliminate general parsing branches. Conversely, accidentally making a value appear constant when it must change asynchronously can create a serious bug. Hardware state must use the correct volatile or synchronization contract.

`volatile` accesses are observable and cannot be freely treated as ordinary stable memory. An ordinary global shared with an ISR or thread is not made safe merely because a debug build happened to reload it.

## Edge cases and failure modes
- Confusing `const` with compile-time constantness.
- Expecting a macro or enum to have the same object/linkage behavior as a variable.
- Reading hardware through a non-volatile object and then blaming constant propagation.
- Relying on signed-overflow behavior that is actually undefined.
- Assuming propagation across a separate translation unit without LTO or equivalent visibility.

## Verification / debugging
Compile with optimization reports enabled when available and inspect assembly. If a value unexpectedly disappears, identify which invariant allowed the compiler to prove it. Compare LTO and non-LTO builds. Static analysis can expose writes that are unreachable or ineffective.

## Performance, memory, timing and power
Propagation often reduces loads, branches, multiplications, and memory traffic. It can shrink flash and improve deterministic execution. It may also expose larger opportunities for dead-code elimination and inlining. Reduced memory traffic can lower energy consumption on systems where memory accesses dominate.

## Staff-level takeaway
The strongest optimization technique is not a clever flag; it is making real invariants visible to the compiler without lying about hardware or concurrency. When a value is truly fixed, express that fact in the most precise C construct available and verify the generated image.