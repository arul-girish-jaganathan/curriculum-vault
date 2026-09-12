# Optional outputs

> Canonical C topic note — Chapter 42. An optional output is a result the caller may request by supplying a valid pointer or configuration flag. The API must define whether a null/absent output is allowed and whether computation still occurs.

## Definition
An optional output lets one function support callers that need only the primary result while avoiding unnecessary storage or copying. A common C pattern is a nullable pointer such as `size_t *written`.

## Mechanism and language rules
A nullable pointer is meaningful only if the contract explicitly permits null. The implementation must branch before dereferencing it. The function must also define output validity on success and every failure path.

### What to reason about
- Is `NULL` a legal input for the optional output?
- Is the output modified on partial failure?
- Does absence of the output change timing or side effects?
- Does the pointer reference writable storage of sufficient size and lifetime?
- Can an output alias an input buffer?
- Is the output produced before an asynchronous operation completes?

Optional outputs should not silently change the semantic success condition.

## Embedded implications
Optional outputs can reduce RAM and copy costs in firmware APIs, especially when only some callers need diagnostics. They are useful for optional byte counts, status details, timestamps, or hardware metadata.

### Firmware review angle
Document nullability and ownership. For DMA/asynchronous APIs, distinguish “bytes accepted” from “bytes completed,” and never let an optional pointer hide a required synchronization or lifetime rule.

## Edge cases and failure modes
- Dereferencing a null optional pointer.
- Writing partial output before reporting failure without documenting it.
- Optional output aliases an input and breaks assumptions.
- Caller passes a pointer to expired stack storage.
- Null output changes behavior accidentally rather than merely suppressing storage.

## Example pattern
```c
status_t encode(const uint8_t *src, size_t len,
                uint8_t *dst, size_t cap, size_t *written)
{
    size_t n = compute_encoded_size(src, len);
    if (n > cap) {
        return STATUS_NO_SPACE;
    }
    write_encoded(dst, src, len);
    if (written != NULL) {
        *written = n;
    }
    return STATUS_OK;
}
```
The contract should state whether `written` is unchanged on failure.

## Verification / debugging
Test both `NULL` and non-null outputs, exact capacity, one-byte-too-small capacity, aliasing cases where permitted, and failure paths. Use static analysis/nullability annotations when available.

Staff-level questions: Is the output genuinely optional? Can the contract guarantee its validity independently of the main result? Does the API remain understandable compared with a result structure?

## Staff-level takeaway
Optional outputs are safe when **nullability, validity, ownership, and failure semantics are explicit**. They should reduce unnecessary work, not hide essential contract information.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
