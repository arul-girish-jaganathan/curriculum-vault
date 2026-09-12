# Optional outputs

> Canonical C topic note — Chapter 42. An optional output is an output object a caller may omit, usually represented by a nullable pointer. The API contract must define whether `NULL` means “do not produce,” “not supported,” or an invalid argument.

## Definition
A function such as `status_t read_value(value_t *out)` may accept `out == NULL` to indicate that the caller does not need the result. ISO C defines null pointer semantics, but whether a particular API accepts a null pointer is entirely contractual.

## Mechanism and language rules
The callee must check the pointer before dereferencing it when null is permitted. The contract should state whether the operation itself remains valid without the output and whether output storage is modified on failure.

### What to reason about
- Is `NULL` explicitly permitted?
- Is the pointer required to be aligned and point to writable storage?
- Is the output initialized on every success path?
- Is partial output possible on failure?
- Can the caller pass an aliased input/output object?

A nullable output is not a license to silently ignore an invalid pointer. Distinguish “optional” from “required but unchecked.”

## Embedded implications
Optional outputs can reduce unnecessary copies and RAM use. They are useful for APIs that can cheaply answer a status-only query. However, repeated nullable parameters can make contracts hard to understand and can hide ownership/lifetime requirements.

### Firmware review angle
For safety-critical interfaces, prefer explicit API variants or a result/status object when optionality becomes complex. Document whether an output is produced before a timeout or only after complete hardware transfer.

## Edge cases and failure modes
- Dereferencing a permitted null output causes UB.
- Writing an output before discovering an error leaves ambiguous partial state.
- Passing the same object as multiple outputs can create aliasing/ordering problems.
- Treating an optional output as always initialized causes stale-data bugs.

## Example pattern
```c
status_t adc_read(uint16_t *sample)
{
    uint16_t value = hardware_read_adc();
    if (sample != NULL) {
        *sample = value;
    }
    return STATUS_OK;
}
```
The contract must still define what happens if hardware acquisition fails and whether `sample` remains untouched.

## Verification / debugging
Unit-test `NULL`, valid aligned storage, boundary values, failure paths, and aliasing combinations. Static analysis should verify that nullable parameters are checked before dereference.

Staff-level questions:
- Does optionality actually simplify the API?
- Is the output contract atomic on failure?
- Can a result type communicate success and value more clearly?

## Staff-level takeaway
Optional outputs are a useful C pattern when **nullability and output validity are explicit contracts**. Keep the number of states small and test every combination of pointer presence and operation result.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
