# errno semantics

> Canonical C topic note — Chapter 42. `errno` is a library error-reporting mechanism, not a universal C exception system. Its exact availability and error values depend on the applicable C/POSIX environment.

## Definition
`errno` is an integer error indicator used by specified library interfaces. A function documents when failure is reported through `errno`; callers should inspect it only when the operation's contract says the value is meaningful. ISO C and POSIX define overlapping but not identical sets of interfaces and semantics.

## Mechanism and language rules
In POSIX environments, `errno` is typically thread-local. The value may remain unchanged after successful calls, so success does not imply `errno == 0`. A failing call can set it to a documented error value. Some functions may also legitimately modify it as an implementation detail.

### What to reason about
- Does the function contract guarantee that `errno` is meaningful after failure?
- Must `errno` be saved before another library call overwrites it?
- Is the environment threaded and is `errno` thread-local?
- Is the error value stable across platforms?
- Is an error retryable, transient, or permanent?
- Is this actually a freestanding embedded environment with no `errno` support?

A common pattern is: check the function result first, then copy `errno` immediately if required.

## Embedded implications
Many embedded systems use minimal libc implementations, so `errno` may be costly in code size, TLS support, RAM, or integration complexity. Drivers often use project-specific status codes instead because errors need hardware-specific detail.

### Firmware review angle
Do not mechanically import hosted/POSIX `errno` conventions into a freestanding driver layer. If used, define the supported subset and translation boundary explicitly.

## Edge cases and failure modes
- Checking `errno` after a successful call and treating a stale value as a new error.
- Calling another function before saving `errno`.
- Assuming POSIX error numbers are portable to a bare-metal target.
- Sharing a non-thread-safe error variable across tasks.
- Collapsing distinct hardware faults into a generic error.

## Example pattern
```c
int fd = open_device();
if (fd < 0) {
    int saved = errno;
    report_open_failure(saved);
    return -1;
}
```
The pattern is meaningful only where the interface's contract specifies `errno` semantics.

## Verification / debugging
Read the relevant standard/library documentation for each API. Test failures explicitly and verify error translation at subsystem boundaries. In embedded builds, inspect whether `errno` introduces TLS or runtime dependencies that violate the intended architecture.

Staff-level questions: Who owns the error domain? Is `errno` appropriate here? Can the caller distinguish transient hardware state from permanent configuration failure? Is the error captured before subsequent operations overwrite it?

## Staff-level takeaway
Treat `errno` as **API-specific diagnostic state**, not as a universal global exception channel. Use it where its environment and contract justify it, and translate it deliberately at embedded abstraction boundaries.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
