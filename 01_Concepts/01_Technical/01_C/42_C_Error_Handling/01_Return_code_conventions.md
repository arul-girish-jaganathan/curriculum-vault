# Return-code conventions

> Canonical C topic note — Chapter 42. Return codes are one of the most portable C error-reporting mechanisms: a function returns a value representing success or failure, while detailed semantics are defined by the API contract.

## Definition
A return-code convention defines how a function communicates success, failure, partial success, and sometimes retry or state conditions. ISO C does not prescribe one universal convention. Common designs use `0` for success, nonzero error codes, negative errors, enumerations, or domain-specific status types.

## Mechanism and language rules
The return type must have enough representational capacity for every documented outcome. Callers must test the return value before using outputs whose validity depends on success. A good contract distinguishes programmer misuse from environmental/runtime failure and states whether output objects are modified on failure.

### What to reason about
- Is zero success or failure?
- Can multiple error domains collide?
- Is the returned value signed/unsigned and are conversions safe?
- Is partial progress represented?
- Are outputs valid after failure?
- Does the API require retry, cleanup, or reset?

Prefer named enums or status types over magic numbers. If ABI compatibility matters, explicitly control the underlying representation through the supported interface rather than assuming enum size.

## Embedded implications
Return codes are deterministic, allocation-free, and suitable for firmware APIs. They avoid global error state and make failure propagation explicit. However, deeply nested error checks can become verbose, so common cleanup patterns should be standardized.

### Firmware review angle
Status codes should be stable across bootloader/application boundaries and diagnostic tooling. Reserve ranges for subsystem ownership and document whether codes are persistent protocol values or private implementation details.

## Edge cases and failure modes
- Ignored return values cause silent failure.
- `-1` can be ambiguous across APIs.
- Unsigned conversion can turn a negative error into a large positive value.
- Reusing an enum value for a new meaning breaks diagnostics.
- Returning success before hardware completion creates a false contract.

## Example pattern
```c
typedef enum {
    STATUS_OK = 0,
    STATUS_INVALID_ARG,
    STATUS_TIMEOUT,
    STATUS_IO,
} status_t;

status_t sensor_read(uint16_t *value);
```
The contract should additionally state whether `*value` is modified on every failure class.

## Verification / debugging
Unit-test every documented status, invalid input, timeout, and partial-progress case. Enable compiler warnings for ignored results where supported or use a project-specific `WARN_UNUSED_RESULT` attribute. Trace status propagation at subsystem boundaries.

Staff-level questions:
- Can every caller distinguish recoverable from fatal failure?
- Is the status stable enough for telemetry and ABI boundaries?
- Are outputs and ownership rules explicit on failure?

## Staff-level takeaway
A return code is valuable only when its **semantic contract is unambiguous**. Design status spaces deliberately, preserve information through propagation, and make ignored or misinterpreted errors difficult to introduce.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
