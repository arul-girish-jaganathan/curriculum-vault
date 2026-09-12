# API failure contracts

> Canonical C topic note — Chapter 42. An API failure contract defines preconditions, failure representation, output validity, ownership, side effects, recovery expectations, and timing behavior when an operation cannot complete normally.

## Definition
A function signature alone rarely tells callers what failure means. A robust contract states what inputs are valid, which outputs are produced, what resources are consumed, what state changes may occur, which errors are possible, and whether the operation is retryable.

## Mechanism and language rules
Contracts are expressed through documentation, types, assertions, static analysis annotations, and implementation checks. ISO C does not provide a universal contract system, so teams must establish conventions.

### What to reason about
- Preconditions: pointer validity, range, state, alignment, ownership.
- Postconditions: output validity, state transition, resource ownership.
- Failure postconditions: untouched output, partial output, rollback, degraded state.
- Concurrency: blocking, reentrancy, ISR safety, atomicity.
- Timing: bounded execution and timeout semantics.

The strongest contract makes invalid states difficult to represent rather than merely documenting them.

## Embedded implications
Embedded APIs often cross hardware boundaries. A `write()`-like function may mean “copied into a software buffer,” “accepted by the driver,” or “transmitted on the wire.” Those are different postconditions and must not be conflated.

### Firmware review angle
Document whether calls may block, whether interrupts must be enabled, whether DMA retains buffers, and which reset/power states are legal. Stable error contracts are especially important when drivers are reused across MCU variants.

## Edge cases and failure modes
- Success reported before the requested external effect occurs.
- Output partially modified on failure without documentation.
- Timeout returns while DMA continues using the caller's buffer.
- Retry duplicates a non-idempotent command.
- Error translation loses the information needed for recovery.

## Example pattern
```c
/* Contract: on success, *bytes_sent is valid; on failure it is unchanged. */
status_t transmit(const uint8_t *data, size_t len, size_t *bytes_sent);
```
The implementation can enforce the output guarantee by writing a local temporary and committing it only on success.

## Verification / debugging
Turn each contract statement into tests: invalid inputs, failure injection, timeout, ownership, output validity, concurrency, and recovery. Review public APIs for undocumented side effects and use static analysis annotations where supported.

Staff-level questions:
- Can the contract be expressed in the type system?
- Is success defined in terms of the actual external effect?
- What remains valid after failure?
- Can the caller safely retry?
- What timing and ownership guarantees cross the boundary?

## Staff-level takeaway
A failure contract is the **behavioral ABI of an API**. Treat it as a first-class design artifact, because ambiguity about failure is a major source of integration defects even when the underlying C code is syntactically correct.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
