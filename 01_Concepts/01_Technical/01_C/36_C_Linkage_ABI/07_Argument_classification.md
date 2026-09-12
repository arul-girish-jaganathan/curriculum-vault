# Argument classification

> Canonical C topic note — chapter 36.

## Definition
**Argument classification** is the ABI process that maps a C parameter's type and representation to machine-level locations such as general-purpose registers, floating-point registers, stack slots, or memory. ISO C specifies the parameter and function semantics; the classification algorithm is ABI-specific.

## Mechanism and language rules
For a simple function:

```c
uint32_t f(uint32_t a, uint32_t b);
```

an ABI may pass `a` and `b` in integer registers. A different type, size, alignment, or position can change classification. Typical ABI rules consider:

- integer and pointer widths;
- signed/unsigned representation;
- floating-point types;
- aggregate size and alignment;
- whether an aggregate is homogeneous;
- register availability at the call site;
- variadic versus fixed-parameter calls;
- stack alignment and overflow areas.

The source type is therefore not enough to predict machine behavior without knowing the target ABI. A struct passed by value is especially important: it may be split across registers, passed in memory, or represented using a hidden address depending on ABI rules.

Default argument promotions also matter for variadic calls, while ordinary fixed parameters use the declared parameter types after the normal language conversions.

## Embedded implications
Classification affects performance and stack usage. A small integer parameter may require no stack traffic, while a large aggregate can cause memory loads/stores or hidden temporaries. This matters in ISR-adjacent paths, high-frequency callbacks, DSP loops and low-power code.

For public firmware interfaces crossing separately compiled components, avoid relying on accidental compiler behavior such as “this struct happens to fit in two registers.” The ABI, compiler version and options are part of the contract.

### Firmware review angle
Inspect representative disassembly for hot interfaces. Measure stack usage, not just source-level parameter counts. Check both caller and callee and verify that every component uses the same ABI mode.

## Edge cases and failure modes
Potential defects include:

- mismatched prototypes across translation units;
- incompatible packed/aligned structure definitions;
- hard-float versus soft-float objects;
- different compiler ABI switches;
- changing a public struct by value;
- assuming pointer and integer parameters consume equivalent resources;
- overlooking hidden parameters for certain return types.

A parameter's **source order** is not necessarily its **machine order** in a simplistic register/stack picture; classification and alignment rules determine placement.

## Example pattern
```c
typedef struct {
    uint32_t id;
    uint32_t value;
} sample_t;

sample_t process(sample_t in);
```

The source says “struct by value.” The exact register/memory representation is an ABI question.

## Verification / debugging
Use compiler-generated assembly, debugger register inspection and ABI documentation. Build an ABI test with known argument values and inspect the call boundary. Compare compiler flags such as architecture, floating-point ABI and structure-packing options.

Staff-level questions:
- What classification rule applies to this exact type?
- Does a public struct-by-value API create unnecessary ABI coupling?
- What changes if the struct gains one field?
- Is the interface stable across compilers and architectures?
- Can an opaque pointer/context API reduce ABI sensitivity?

## Staff-level takeaway
Argument classification is where **source-level types become physical calling resources**. For stable embedded interfaces, know the ABI rule, not merely the C declaration, and test the generated boundary.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
