# Out-parameters

> Canonical C topic note — Chapter 42. An out-parameter is caller-owned storage supplied to a function for receiving a result. The contract must define validity, required capacity, initialization, ownership, and behavior on failure.

## Definition
A pointer parameter such as `uint32_t *value` can let a function return primary status through its return value and data through caller storage. This separates error classification from the result and supports multiple outputs.

## Mechanism and language rules
The pointer must designate writable, suitably aligned storage with sufficient lifetime and size. The implementation must define whether the pointer may be null and whether the output is modified before success.

### What to reason about
- Is the pointer an input, output, or in/out parameter?
- What preconditions apply to alignment and capacity?
- Is the output initialized on every success path?
- Is it unchanged on failure or partially written?
- Can it alias an input or another output?
- Does asynchronous execution retain the pointer after return?

Use `const` on input pointers and explicit documentation for ownership and aliasing.

## Embedded implications
Out-parameters avoid large structure returns or copies on some ABIs and can be useful in constrained systems. They are common in drivers and parsers, but pointer lifetime becomes critical when DMA or deferred work is involved.

### Firmware review angle
Define ownership at every API boundary. For asynchronous APIs, do not retain an out-parameter pointer unless the contract explicitly says so and the lifetime mechanism is robust.

## Edge cases and failure modes
- Null pointer dereference.
- Uninitialized output after an error.
- Partial output interpreted as complete output.
- Input/output aliasing causing self-overwrite.
- Stack output passed to a function that stores it for later asynchronous use.

## Example pattern
```c
status_t parse_id(const uint8_t *buf, size_t len, uint32_t *id)
{
    if (buf == NULL || id == NULL || len < 4U) {
        return STATUS_INVALID_ARG;
    }
    *id = ((uint32_t)buf[0] << 24) |
          ((uint32_t)buf[1] << 16) |
          ((uint32_t)buf[2] << 8)  |
          (uint32_t)buf[3];
    return STATUS_OK;
}
```
The contract says `*id` is valid only when `STATUS_OK` is returned.

## Verification / debugging
Test null pointers, boundary lengths, exact output values, failure preservation, aliasing if allowed, and asynchronous lifetime rules. Static analysis can help detect nullability and uninitialized-output paths.

Staff-level questions: What exactly does success guarantee? What happens to the output on every failure? Could a result structure make the contract clearer? Is the pointer still valid after the function returns?

## Staff-level takeaway
Out-parameters are a simple C mechanism for **separating status from data**, but the pointer contract is part of the API ABI. Define validity and lifetime as precisely as the data type itself.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
