# Return-code conventions

> Canonical C topic note — Chapter 42. Return codes are an explicit error-reporting channel. C does not prescribe a universal convention, so a project must define the value domain, success semantics, failure ownership, and propagation policy.

## Definition
A return-code API communicates operation status through the function's return value, commonly an enum, integer status, boolean, pointer/sentinel, or standardized error domain. A robust convention separates **success/failure classification** from any output data and makes every return value actionable.

## Mechanism and language rules
The C type system allows many representations, but the contract must define which values are valid. Enumerations improve readability but do not automatically prevent invalid integer values from arriving through casts, corruption, or ABI boundaries.

### What to reason about
- Is zero success or failure?
- Is success exactly one value or a range?
- Can multiple failure classes be represented without collisions?
- Are outputs valid on failure?
- Does the caller have to inspect the result immediately?
- Can errors be propagated without losing root-cause information?
- Is the API callable from ISR, task, or fault context?

Prefer named status types and explicit comparisons. Avoid mixing unrelated numeric domains such as POSIX `errno`, protocol status, driver status, and application status without translation.

## Embedded implications
Return codes are cheap in CPU/RAM terms but can become awkward when APIs cross asynchronous boundaries. A function may return “accepted” while hardware completion occurs later. That distinction must be explicit.

### Firmware review angle
Define a project-wide status model with ownership and conversion rules. Make it clear whether callers must retry, reset a peripheral, enter degraded mode, or propagate the failure. For safety-critical code, review every ignored status as a deliberate decision.

## Edge cases and failure modes
- Ignoring a non-success result.
- Treating any nonzero value as interchangeable across APIs.
- Returning a value outside the documented domain.
- Reporting success before an asynchronous operation actually completes.
- Translating an error and losing the original diagnostic cause.

## Example pattern
```c
typedef enum {
    STATUS_OK = 0,
    STATUS_INVALID_ARG,
    STATUS_BUSY,
    STATUS_TIMEOUT,
    STATUS_HW_FAULT
} status_t;

status_t sensor_read(uint16_t *value);
```
The contract should state which outputs are valid for each status and whether `STATUS_BUSY` is retryable.

## Verification / debugging
Test every documented status, including injected hardware failure and timeout paths. Use compiler warnings/static analysis to identify ignored results where practical. Review status translation at module boundaries.

Staff-level questions: Is the status domain closed and documented? Can a caller distinguish retryable from terminal failure? Does the return value describe the requested effect or merely local acceptance?

## Staff-level takeaway
A return code is useful only when its **semantic domain and caller obligations are unambiguous**. Standardize status meanings across module boundaries and make ignored failures explicit design decisions.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
