# Structure return

> Canonical C topic note — chapter 36.

## Definition
C permits functions to return structures and unions by value. The **ABI**, not ISO C, determines whether the result is returned in registers, multiple registers, memory, or through a hidden pointer supplied by the caller.

## Mechanism and language rules
```c
typedef struct {
    uint32_t status;
    uint32_t value;
} result_t;

result_t sensor_read(void)
{
    return (result_t){ 0, 42 };
}
```

The language semantics are ordinary value semantics: the caller receives a result object/value of the declared type. The compiler may optimize copies away; the abstract C behavior does not require a particular temporary or machine representation.

At ABI level, aggregate classification may depend on size, alignment, fields, floating-point members, packing and target rules. A large aggregate may be implemented conceptually as:

```c
/* ABI concept, not portable source syntax */
result_t *hidden_result;
```

where the caller provides storage and the callee writes the result there. The exact hidden parameter position and register usage are ABI-specific.

## Embedded implications
Structure returns can make APIs readable but can also affect stack usage, memory traffic and deterministic latency. On small MCUs, returning a large descriptor or packet by value may generate copies that are expensive in a hot path.

This does **not** mean “never return structs.” Small value types can make ownership and error handling clearer. The engineering decision should be based on generated code, ABI stability, lifetime semantics and measured resource cost.

### Firmware review angle
For public interfaces crossing libraries or bootloader/application boundaries, document the exact ABI and structure layout. Avoid exposing compiler-specific packing assumptions. For performance-critical paths, inspect assembly and measure stack/RAM traffic.

## Edge cases and failure modes
Changing a structure can be an ABI break even when source code still compiles. Adding a member may change size, alignment, classification, register count or hidden-return behavior.

Packed structures introduce another concern: their representation may be unaligned and accessing members can generate special instructions or be inefficient/unsupported on some targets. Do not use packing merely to control a structure-return ABI without understanding alignment consequences.

Returning a pointer to a local structure is a different and incorrect pattern because the pointed-to object's lifetime ends when the function returns:

```c
const result_t *bad(void)
{
    result_t r = {0};
    return &r; /* dangling pointer */
}
```

## Example pattern
```c
result_t sensor_read(void);

void task(void)
{
    result_t r = sensor_read();
    if (r.status == 0u) {
        consume(r.value);
    }
}
```

The interface is simple; the machine-level cost remains ABI-dependent.

## Verification / debugging
Compile at each supported optimization level and inspect assembly. Measure stack high-water marks and memory traffic on target hardware. Compare ABI dumps when changing public structures.

Staff-level questions:
- Is the returned aggregate small enough for the target ABI?
- Is this API source-compatible but binary-incompatible after a field change?
- Would an explicit output buffer make ownership and ABI stability clearer?
- Does packing introduce unaligned accesses?

## Staff-level takeaway
Structure return is a good example of the distinction between **C value semantics and ABI mechanics**. Design for clear ownership and semantics, then verify the physical cost and binary compatibility on the actual target ABI.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
