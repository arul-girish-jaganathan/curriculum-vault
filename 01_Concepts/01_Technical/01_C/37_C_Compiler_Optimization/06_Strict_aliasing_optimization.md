# Strict-aliasing optimization

> Canonical C topic note — chapter 37.

## Definition
C's object-access and effective-type rules restrict which lvalue types may be used to access an object's stored value. Optimizers exploit these rules to infer that certain pointers do not alias. This is often called strict-aliasing optimization.

## Mechanism and language rules
Consider:

```c
int update(int *a, float *b)
{
    *a = 1;
    *b = 2.0f;
    return *a;
}
```

Under the language's aliasing rules, `int *` and `float *` do not generally designate the same `int` object for a valid access. The compiler may therefore reuse the value `1` rather than reload `*a`. If a program creates an invalid type-punning access, the resulting behavior is not rescued by “but both pointers have the same address.”

Character types have special access privileges for inspecting object representation. `memcpy` is the conventional portable technique for copying representation between unrelated types; modern C also requires careful reasoning about effective type and object lifetime.

## Embedded implications
Aliasing bugs can become release-only failures and are especially dangerous in drivers, protocol parsers, DMA buffers, and packed data conversion. Disabling strict-aliasing optimization may hide a defect while reducing performance; it does not make every invalid access portable.

Use explicit serialization, `memcpy`, unions only where the intended semantics are supported by the target/toolchain policy, or carefully designed typed APIs. DMA and hardware descriptors should have explicit representation and alignment contracts.

## Edge cases and failure modes
- Casting `uint8_t *` to an unrelated object pointer and dereferencing without a valid object/access model.
- Assuming `volatile` fixes aliasing.
- Confusing alignment correctness with effective-type correctness.
- Treating `-fno-strict-aliasing` as a general safety fix.
- Forgetting that optimizer assumptions can cross function boundaries with LTO.

## Verification / debugging
Compile with aggressive optimization and sanitizers where supported. Compare aliasing-sensitive code in assembly. Review casts at type boundaries and use static analysis. Test serialization on targets with different alignment and endianness properties.

## Staff-level takeaway
Aliasing is a semantic contract, not an optimization switch. Establish legal object access first; only then reason about performance consequences.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
