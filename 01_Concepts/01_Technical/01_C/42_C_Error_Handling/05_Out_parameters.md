# Out-parameters

> Canonical C topic note — Chapter 42. An out-parameter lets a function write a result into caller-owned storage through a pointer. It is a core C interface pattern because C has no general multiple-return-value syntax.

## Definition
A parameter such as `T *out` designates caller-provided storage into which the callee writes a result. The API must define preconditions, ownership, initialization, output validity, and failure behavior.

## Mechanism and language rules
The pointer value is passed according to the ABI. Dereferencing it requires a valid, appropriately aligned object with sufficient storage and the required lifetime. `const` on input pointers and non-`const` output pointers can make intent explicit.

### What to reason about
- Is `out` allowed to be null?
- How large must the destination be?
- Is it fully initialized on success?
- Is it modified on failure?
- Can `out` alias an input object?
- Does the callee retain the pointer after returning?

If the API does not retain the pointer, the caller-owned object's lifetime only needs to cover the call. If the pointer is retained asynchronously, the lifetime and ownership contract becomes substantially stronger.

## Embedded implications
Out-parameters avoid returning large structures by value when ABI/code-size constraints make that useful, and they can let callers reuse static buffers. They also make ownership visible at the call boundary.

### Firmware review angle
For DMA or asynchronous APIs, an out-parameter may actually become an ownership transfer. Document whether the pointer is used synchronously, retained until completion, or returned through a callback.

## Edge cases and failure modes
- Passing an uninitialized pointer instead of a pointer to storage.
- Returning success without initializing the complete output.
- Partial writes on failure without documenting them.
- Stack output passed to an asynchronous operation and then going out of scope.
- Aliasing input/output unexpectedly changes results.

## Example pattern
```c
status_t parse_u16(const char *text, uint16_t *out)
{
    if ((text == NULL) || (out == NULL)) {
        return STATUS_INVALID_ARG;
    }

    uint16_t value;
    if (!parse_internal(text, &value)) {
        return STATUS_INVALID_DATA;
    }
    *out = value;
    return STATUS_OK;
}
```
A local temporary gives an atomic “commit on success” behavior for the output.

## Verification / debugging
Test null pointers, valid storage, failure-before-write, boundary values, aliasing, and asynchronous lifetime. Static analysis should track pointer validity and possible null dereferences.

Staff-level questions:
- What exactly does success guarantee about the output?
- Who owns the pointed-to storage before, during, and after the call?
- Can the function retain the pointer?
- Is partial output ever observable?

## Staff-level takeaway
An out-parameter is more than `*out = value`; it is a **storage, lifetime, ownership, and validity contract**. Make those dimensions explicit, especially when the operation crosses task, ISR, DMA, or subsystem boundaries.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
