# errno semantics

> Canonical C topic note — Chapter 42. `errno` is a thread-local error indicator provided by the C library for selected library interfaces; it is not a universal C exception mechanism and its meaning is defined by the function that documents it.

## Definition
`errno` is a modifiable integer object used by library functions to report additional error information. A function may set it when a documented error occurs. A successful call generally does not guarantee that `errno` is reset, so callers should inspect it only when the API specifies that an error occurred and that `errno` is meaningful.

## Mechanism and language rules
`<errno.h>` provides the `errno` identifier and error macros such as `EDOM`, `ERANGE`, and implementation-defined additional values. In a threaded hosted environment, `errno` is commonly implemented so each thread has independent state, though the C standard specifies the interface rather than a particular TLS implementation.

### What to reason about
- Does the immediately preceding API call document `errno` use?
- Was the failure return checked first?
- Could another library call overwrite `errno` before it is consumed?
- Is the target freestanding or using a restricted C library?
- Is the error code stable across platforms?

Do not write `if (errno != 0)` after an arbitrary successful call and conclude that the call failed.

## Embedded implications
Many embedded libraries provide only a subset of hosted-library `errno` behavior, and some RTOS/libc configurations implement it with thread-local storage that has RAM and context-switch cost. In tight firmware, explicit status returns are often clearer and cheaper.

### Firmware review angle
If `errno` crosses a portability boundary, document the supported libc and threading model. Avoid using it as hidden global state in ISR paths or callbacks unless the implementation explicitly guarantees the required behavior.

## Edge cases and failure modes
- Reading `errno` after another call can report the wrong failure.
- `errno` can retain an old value after success.
- Assuming POSIX-specific error meanings in ISO C code reduces portability.
- ISR and task contexts can have different error-state semantics.
- Logging code can itself make calls before `errno` is copied.

## Example pattern
```c
long value = strtol(text, &end, 10);
if (end == text) {
    /* conversion failed */
} else if (errno == ERANGE) {
    /* range error, when documented by the function */
}
```
The important pattern is to save/use error state at the point required by the API contract and validate the other result conditions too.

## Verification / debugging
Test boundary values, malformed input, range errors, and successful calls following failures. Verify the exact libc documentation for the target. In multithreaded firmware, test whether error state is per-thread as expected.

Staff-level questions:
- Why is `errno` preferable to an explicit status here?
- What are its storage and context-switch costs?
- Does the target's libc actually implement the required semantics?
- Can diagnostic code overwrite the evidence?

## Staff-level takeaway
Treat `errno` as **API-specific diagnostic state**, not as a global failure flag. Explicitly check the primary return condition first, then consume `errno` only where documented.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
