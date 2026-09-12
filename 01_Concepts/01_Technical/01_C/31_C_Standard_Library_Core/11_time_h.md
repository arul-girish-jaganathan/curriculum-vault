# time.h

> Canonical C topic note — chapter 31.

## Definition
`time.h` provides calendar-time and processor-time facilities including `time_t`, `struct tm`, `clock_t`, `time`, `clock`, `difftime`, `gmtime`, `localtime`, `mktime`, `strftime`, and related functions. The C standard intentionally leaves important representation details implementation-defined: the range and representation of `time_t`, epoch conventions, calendar range, and relationship to the host's real-time clock are not universal.

## Mechanism and language rules
```c
#include <time.h>

time_t now = time(NULL);
struct tm *utc = gmtime(&now);
```

`time` obtains the implementation's current calendar time when available. `gmtime` converts it to a broken-down UTC representation and `localtime` converts it according to the implementation's local-time rules. `mktime` converts a broken-down local time back to `time_t`. `strftime` formats a `struct tm` into text.

`clock` measures processor time consumed by the program according to the implementation, not necessarily elapsed wall-clock time. `difftime` is the portable way to compute differences between `time_t` values.

### What to reason about
- `time_t` is not guaranteed to be a signed 32-bit Unix timestamp.
- `clock_t` and `CLOCKS_PER_SEC` describe processor-time measurement, not a universal hardware timer.
- `struct tm` fields have defined ranges and semantics; `tm_year` is years since 1900 and `tm_mon` is zero-based.
- `mktime` normalizes fields and can therefore accept values outside their nominal ranges.
- `gmtime`/`localtime` return implementation-managed storage; later calls may overwrite it.
- Time zones, daylight-saving rules, and leap-second behavior are largely implementation/environment concerns.

## Embedded implications
Many MCUs have no battery-backed real-time clock or OS time service. A freestanding libc may implement only a subset of `time.h`, or provide hooks that the application must connect to an RTC/OS clock.

For periodic scheduling, use a monotonic hardware/RTOS tick rather than calendar time. Calendar time can jump because of synchronization, user changes, RTC correction, or rollover. Protocol timestamps should specify width, epoch, timezone, and units explicitly rather than assuming `time_t` layout.

### Firmware review angle
Determine the source of wall-clock time, resolution, rollover behavior, startup validity, synchronization method, and interrupt/RTOS interaction. Measure formatting cost if `strftime` is enabled, and verify behavior when the clock is invalid or unavailable.

## Edge cases and failure modes
Do not use `difftime`-style calendar arithmetic as a replacement for a monotonic deadline mechanism. Local time can move backward or forward. `mktime` can normalize dates unexpectedly, and DST transitions can make local civil times ambiguous or nonexistent.

Never serialize raw `time_t` unless the product contract explicitly defines its representation. Avoid assuming `sizeof(time_t)` or an epoch based only on a particular desktop Unix environment.

## Example pattern
For embedded elapsed-time logic, use an explicitly defined unsigned tick counter and wrap-safe comparison:

```c
static int deadline_reached(uint32_t now, uint32_t deadline)
{
    return (int32_t)(now - deadline) >= 0;
}
```

Use `time.h` calendar functions when actual civil time is required.

## Verification / debugging
Test dates around rollover boundaries, month/year transitions, DST changes where applicable, invalid RTC state, and counter wrap. Verify `time_t` size and semantics on every target. Compare elapsed-time measurements against a known hardware timer and inspect generated code when timing overhead matters.

Staff-level questions:
- Is this wall-clock time or monotonic elapsed time?
- What happens across reset and RTC loss?
- What epoch and width does the protocol define?
- Can time move backward?
- What does the target libc actually implement?

## Staff-level takeaway
The key architectural distinction is **civil time versus monotonic time**. `time.h` is appropriate for calendar representation and formatting, but embedded scheduling, timeout logic, and protocol timing should use explicitly defined monotonic clocks with documented width, resolution, and rollover behavior.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
