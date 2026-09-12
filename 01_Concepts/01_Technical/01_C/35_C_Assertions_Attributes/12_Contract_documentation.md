# Contract documentation

> Canonical C topic note — chapter 35.

## Definition
A contract documents what a C function, module, type, or subsystem requires, guarantees, modifies, owns, and does not support. Good contracts turn implicit assumptions into reviewable interfaces. They may be expressed through types, `_Static_assert`, attributes, comments, naming, tests, and runtime checks.

## Mechanism and language rules
For every public API, document at least:
- preconditions: valid pointers, ranges, state, alignment, initialization;
- postconditions: outputs, state changes, ownership transfer;
- failure behavior: return codes, side effects, recovery;
- concurrency context: thread safety, ISR safety, locking;
- timing/resource limits: blocking, allocation, stack, latency;
- lifetime: who owns and how long referenced objects remain valid.

Example:
```c
/* Requires: dst points to >= len writable bytes; src is valid for len bytes.
 * Does not allocate or block. Safe from task context only. */
int packet_copy(uint8_t *dst, const uint8_t *src, size_t len);
```
The C type system cannot express all of these properties, so documentation and verification complement language-level constraints.

### What to reason about
- Distinguish caller obligations from callee guarantees.
- State ownership and lifetime explicitly.
- Avoid documenting behavior the implementation does not actually guarantee.
- Keep contracts synchronized with tests and static analysis.

## Embedded implications
Contracts are especially important at hardware boundaries. A driver API may require clocks enabled, a peripheral initialized, a buffer aligned to a cache line, or calls restricted to task context. An undocumented assumption becomes an integration defect when another subsystem reuses the API.

### Firmware review angle
Review APIs for determinism, reentrancy, interrupt safety, memory ownership, error propagation, and reset behavior. Prefer contracts that can be mechanically checked with types, assertions, static analysis, or tests rather than prose alone.

## Edge cases and failure modes
A frequent defect is documenting `NULL` as accepted while dereferencing it, or saying an API is nonblocking while it takes a mutex. Another is documenting a buffer as “aligned” without specifying the required alignment.

Do not promise exact timing without measurement and a defined execution environment. Do not hide safety-critical restrictions in comments that are not visible at call sites.

## Example pattern
```c
/* Contract:
 * - buf: non-NULL, 4-byte aligned, writable for len bytes
 * - len: <= DEVICE_FIFO_MAX
 * - context: task context; may block
 * - ownership: caller retains buf ownership
 * - return: 0 on success, negative error code otherwise
 */
int device_write(const void *buf, size_t len);
```

## Verification / debugging
Turn important contract clauses into tests: invalid ranges, boundary sizes, concurrent calls, wrong context, alignment violations, and fault injection. Use static analysis and assertions for mechanically checkable properties. During debugging, compare observed behavior against the written contract rather than merely against current implementation behavior.

## Staff-level takeaway
A contract is the boundary between implementation freedom and caller responsibility. Staff engineers make important contracts explicit, minimize unverifiable promises, and design interfaces so the most important assumptions are difficult to violate.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
