# 06: errno.h

## Definition
`<errno.h>` defines the `errno` error-reporting mechanism and symbolic error macros used by selected C library functions. `errno` is a modifiable integer object or macro designating thread-local error state in hosted implementations; it is meaningful only when a function's contract says an error may be reported through it.

## Scope and Boundaries
* **Covers:** `errno`, error macros, checking patterns, preservation rules, and concurrency concerns.
* **Does not cover:** application-specific error enums, POSIX-only `strerror_r` variants, or C++ exception handling.

## Why Does It Exist
Many C library functions return a value that cannot simultaneously carry both a normal result and a detailed failure reason. `errno` provides a side channel for selected error information while keeping the primary return-value contract intact.

## Mechanism and Language Rules
1. A library function that documents `errno` may set it when an error occurs.
2. A successful call is not generally required to clear `errno`; therefore inspect `errno` only after detecting the documented error return.
3. `errno` may be implemented as thread-local state so concurrent threads do not overwrite one another's values.
4. Error macros such as `EDOM`, `ERANGE`, and `EILSEQ` identify error classes where supported by the implementation.
5. Applications must save `errno` before calling another function if the original value must survive subsequent calls.

## Examples
```c
#include <errno.h>
#include <stdlib.h>
#include <limits.h>

static int parse_u32(const char *text, unsigned long *out)
{
    char *end = NULL;
    unsigned long value;

    errno = 0;
    value = strtoul(text, &end, 10);

    if (end == text || errno == ERANGE || value > UINT_MAX) {
        return -1;
    }

    *out = value;
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
* Reading `errno` after a call that did not specify it may produce stale information; this is a contract error, not automatically undefined behavior.
* Calling another library function before consuming a required `errno` value can destroy diagnostic information if that second function changes it.
* Treating a particular numerical `errno` value as universal across all C implementations is non-portable.
* Functions that are not documented to set `errno` cannot be assumed to do so.

## Edge Cases and Failure Modes
* Clearing `errno` before the operation is useful when the API can legitimately return a value that overlaps an error indicator, as with conversion functions.
* `errno` is not a general-purpose global status variable.
* Logging code can accidentally overwrite `errno` before the caller records it.
* Libraries layered on top of libc may need to preserve and restore `errno` across instrumentation or callback calls.

## Embedded Implications
Freestanding firmware may provide little or no conventional `errno` support. A custom libc can implement only the subset needed by the application. Thread-local `errno` can impose RAM and context-management overhead under an RTOS, while a global implementation is unsafe for concurrent tasks.

## Firmware Review Angle
Verify the target libc's `errno` implementation and reentrancy guarantees. Search for code that checks `errno` without first checking the documented function return. Audit logging/error hooks because they often execute between failure detection and error capture.

## Compiler, ABI, and Toolchain Implications
`errno` may expand to a macro or an accessor function, and TLS support depends on the ABI/runtime. Optimization can inline or fold the accessor, but compiler transformations must preserve observable behavior according to the library contract. Mixing incompatible libc runtimes can produce confusing error-state behavior.

## Performance, Memory, Timing, and Power
Accessing thread-local `errno` may be more expensive than reading a normal global on small RTOS systems. High-rate error paths should not rely on expensive formatting or allocation. Since normal success paths should usually avoid touching `errno`, design APIs so expected failures are represented directly in return values.

## Verification / Debugging
* Unit-test both return-value and `errno` behavior.
* Capture `errno` immediately after the documented failure.
* Inspect map files or libc configuration to determine whether `errno` is TLS-backed.
* Run concurrent tests under the actual RTOS/libc combination when reentrancy matters.

## Safety, Security, and Reliability
Failure handling is part of the security boundary. Do not continue as though an operation succeeded because only `errno` was checked. Validate primary returns first, preserve the diagnostic value, and translate low-level errors into bounded application-level failure contracts.

## Trade-offs and Alternatives
* **Use `errno`:** when calling standard APIs whose contract explicitly uses it.
* **Return status codes:** preferred for application APIs where failure is expected and common.
* **Tagged result structures:** useful when both data and rich failure context are required.

## Staff-Level Takeaway
`errno` is not an exception system. It is a narrowly scoped diagnostic side channel whose correctness depends on reading it at exactly the right point and knowing the implementation's concurrency model. Staff-level API design should prefer explicit status returns for application logic and confine `errno` to the boundary where C library contracts require it.

## Related Concepts
* [[00_Chapter_Index]]
* [[../42_C_Error_Handling/00_Chapter_Index]]
* [[../24_C_Threads_C11/00_Chapter_Index]]
* [[../47_C_Safety_Security_Coding/00_Chapter_Index]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*