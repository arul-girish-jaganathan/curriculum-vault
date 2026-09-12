# Return-value ABI

> Canonical C topic note — chapter 36.

## Definition
The **return-value ABI** defines how a function communicates its result from callee to caller at machine level. C specifies the abstract result and its type; the ABI specifies registers, memory, hidden addresses, sign/zero extension, floating-point registers, and aggregate handling.

## Mechanism and language rules
For scalar results:

```c
uint32_t read_counter(void);
float scale(float x);
void *get_buffer(void);
```

an ABI commonly uses one or more designated registers. The exact register depends on architecture and ABI. The compiler handles representation automatically when caller and callee agree.

Return values may involve:

- integer/pointer result registers;
- floating-point result registers;
- sign or zero extension of narrower values;
- multiple registers for wider scalar/aggregate results;
- a hidden structure-return destination pointer;
- caller-owned temporary storage;
- ABI-specific rules for complex/vector types.

A function declaration is therefore an ABI contract. A mismatched declaration can cause the caller to read the wrong register or interpret the wrong width.

## Embedded implications
Return conventions influence cycle count, register pressure and stack traffic. Returning a small status code is usually cheap; returning a large structure by value may involve hidden memory operations depending on the ABI.

For MMIO-related APIs, do not assume a returned integer has the same width as the hardware register unless the API explicitly defines it. Use fixed-width types where the binary representation matters.

### Firmware review angle
For performance-sensitive code, inspect return-value generation rather than guessing from source. Check whether an apparently simple return causes a hidden temporary or copy. For fault/boot interfaces, ensure status and error encodings are stable across image boundaries.

## Edge cases and failure modes
A classic integration failure is a declaration mismatch:

```c
/* header */
uint32_t get_id(void);

/* implementation accidentally differs */
uint64_t get_id(void) { return 0x123456789ULL; }
```

The linker may resolve the symbol even though the source-level contract is broken. Depending on ABI, the caller may observe truncation or an unrelated value.

Other hazards include changing signedness/width, mixing floating-point ABI modes, and assuming structure returns always use a visible pointer argument.

## Example pattern
```c
typedef struct {
    uint16_t status;
    uint16_t value;
} result_t;

result_t sensor_read(void);
```

Whether this uses registers, memory, or a hidden return pointer is ABI-specific.

## Verification / debugging
Inspect generated assembly at both sides of the call. Set breakpoints immediately before return and after call, then inspect designated result registers. Use ABI documentation and compiler record-layout/assembly output for cross-toolchain validation.

Staff-level questions:
- Is the return type part of a stable binary interface?
- Would an output parameter make the ABI clearer or more stable?
- Does adding a field change the calling convention?
- Are narrow return types consistently represented?
- Is a hidden structure-return pointer affecting stack/latency budgets?

## Staff-level takeaway
A C return statement describes an **abstract value**; the ABI defines its physical transfer. When binary compatibility matters, verify the generated return path and treat type changes as potential ABI changes.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
