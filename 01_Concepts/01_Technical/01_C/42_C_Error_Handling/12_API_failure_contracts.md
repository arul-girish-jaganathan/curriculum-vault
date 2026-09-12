# API failure contracts

> Canonical C topic note — Chapter 42. An API failure contract defines preconditions, postconditions, failure state, output validity, ownership, side effects, retry semantics, concurrency behavior, and timing guarantees when an operation cannot complete normally.

## Definition
A function signature rarely captures the meaning of failure. A strong contract answers: what inputs are valid, what outputs are produced, what state may change, what resources are consumed or transferred, which failures are possible, and whether the caller may retry.

## Mechanism and language rules
Contracts are communicated through types, documentation, assertions, static-analysis annotations, naming conventions, and implementation checks. ISO C has no universal contract language, so consistency must come from project policy.

### What to reason about
- **Preconditions:** pointer validity, range, state, alignment, ownership.
- **Success postconditions:** outputs, state transitions, ownership.
- **Failure postconditions:** unchanged output, partial output, rollback, degraded state.
- **Concurrency:** blocking, reentrancy, ISR safety, atomicity.
- **Timing:** worst-case execution and timeout semantics.
- **External effects:** whether hardware or communication activity has already occurred.

The best contract makes invalid states difficult to represent and makes ambiguous recovery impossible.

## Embedded implications
A driver call such as `transmit()` may mean “copied to a queue,” “DMA started,” or “wire transmission completed.” These are materially different success conditions. Buffer lifetime and ownership must be explicit when hardware retains a pointer.

### Firmware review angle
Document blocking behavior, interrupt context restrictions, DMA retention, reset/power-state requirements, and error translation. Stable failure contracts are essential when drivers are reused across MCU variants.

## Edge cases and failure modes
- Success reported before the requested external effect occurs.
- Output partially modified on failure without documentation.
- Timeout returns while DMA still owns the caller's buffer.
- Retry duplicates a non-idempotent command.
- Error translation loses recovery-critical information.

## Example pattern
```c
/* Contract: on success, *bytes_sent is valid; on failure it is unchanged. */
status_t transmit(const uint8_t *data, size_t len, size_t *bytes_sent);
```
The implementation can enforce the failure-output rule by computing into local state and committing the caller-visible result only on success.

## Verification / debugging
Turn every contract clause into tests: invalid inputs, exact boundaries, injected failures, timeout, output validity, ownership, concurrency, retry, and recovery. Review APIs for undocumented side effects and use static-analysis annotations where available.

Staff-level questions: Can the contract be expressed in the type system? Is success defined by the actual external effect? What remains valid after failure? Is retry safe? What timing and ownership guarantees cross the boundary?

## Staff-level takeaway
A failure contract is the **behavioral ABI of an API**. Treat it as a first-class design artifact because ambiguity about failure causes integration defects even when the underlying C implementation is correct.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
