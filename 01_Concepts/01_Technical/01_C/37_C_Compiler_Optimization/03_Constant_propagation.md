# Constant propagation

> Canonical C topic note — chapter 37.

## Definition
Constant propagation substitutes a value known to be constant for a variable or expression and then enables further simplification. It is an optimizer transformation, not a promise that every `const` object becomes a compile-time constant.

## Mechanism and language rules
The compiler builds value information from initializers, control flow, interprocedural facts, and target assumptions. Related transformations include constant folding, copy propagation, range analysis, and conditional simplification.

```c
static int limit(void)
{
    const int n = 16;
    return n * 2;
}
```

The compiler may produce the constant `32`. A `const` object can still have an address and storage, so the C qualifier alone does not establish that it is an integer constant expression. `static const` data may be placed in read-only storage by the implementation, but that is not the same as C language `const` guaranteeing physical ROM.

A value may become constant only along one control-flow path. Optimizers track these facts and invalidate them when assignments or possible aliases make the value uncertain.

## Embedded implications
Propagation can remove loads, branches, table lookups, and arithmetic, reducing cycles, flash, and power. It can also specialize drivers for compile-time board configuration. Conversely, hidden aliasing or undefined behavior can cause the compiler to infer a constant that conflicts with hardware reality.

For MMIO or asynchronously changing state, accesses that must occur must be represented with the appropriate volatile/atomic/concurrency contract. Do not create a normal local mirror and expect the compiler to observe hardware changes.

## Edge cases and failure modes
- Confusing `const` with compile-time constant.
- Taking the address of an object and assuming storage must remain observable.
- Reading a hardware-updated register through an ordinary object.
- Relying on a debugger showing a variable that optimization eliminated.
- Assuming a value is constant across an aliasing boundary without proving it.
- Ignoring integer overflow rules when reasoning about folded expressions.

## Verification / debugging
Use compiler optimization reports, intermediate-representation dumps where available, and disassembly. Check whether a supposedly runtime value disappeared. When behavior is wrong only under optimization, investigate aliasing, lifetime, data races, volatile qualification, and undefined behavior before disabling optimization.

## Staff-level takeaway
Constant propagation is a consequence of trustworthy contracts. Keep configuration immutable, make hardware and concurrency boundaries explicit, and verify generated code when the distinction between a load and a constant has system-level consequences.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
