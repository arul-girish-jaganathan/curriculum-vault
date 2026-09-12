# 06: String Copying

## Definition
String copying is the process of transferring a sequence of characters from a source memory location to a destination buffer, including or establishing a terminating null character. In ISO C, string copying is provided by standard functions (`strcpy`, `strncpy`, `memcpy`), as well as modern bounded interfaces (`snprintf`, `strlcpy`).

## Scope and Boundaries
*   **Covers:** `strcpy`, `strncpy`, `memcpy`, `snprintf`, buffer bounds enforcement, truncation semantics, and guaranteed null termination.
*   **Does not cover:** String concatenation (see [[07_String_concatenation]]), memory moving with overlapping buffers (`memmove`), or wide character copying (`wcscpy`).

## Why Does It Exist
Applications must duplicate and manipulate text:
*   **Message Formatting:** Staging outbound telemetry, protocol payloads, and user interface messages.
*   **State Isolation:** Duplicating incoming network or UART packets into local storage for asynchronous processing.
*   **Safety Requirements:** Preventing buffer overflow exploits while guaranteeing deterministic null termination.

## Mechanism and Language Rules
1.  **`strcpy(dest, src)`:** Copies `src` to `dest` until `'\0'` is encountered. It performs **no bounds checking**; if `dest` is too small, a buffer overflow occurs.
2.  **`strncpy(dest, src, n)` (Dangerous):**
    *   If `strlen(src) < n`, copies characters and pads the remainder of `dest` with zeroes up to `n` bytes.
    *   If `strlen(src) >= n`, copies exactly `n` characters and **omits the terminating null character**.
3.  **`snprintf(dest, n, "%s", src)`:**
    *   Safely copies at most `n - 1` characters and **always** appends a terminating `'\0'` (if $n > 0$).
    *   Returns the total length of the string that *would* have been written, enabling truncation detection.
4.  **No Buffer Overlap:** In `strcpy`, `strncpy`, and `snprintf`, source and destination buffers must not overlap (violates `restrict` qualification).

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define DEST_CAPACITY 8U

/* Correct: Safe string copy using snprintf with truncation detection */
static bool safe_copy_example(char *dest, size_t dest_size, const char *src)
{
    if (dest == NULL || src == NULL || dest_size == 0) {
        return false;
    }

    int written = snprintf(dest, dest_size, "%s", src);
    if (written < 0 || (size_t)written >= dest_size) {
        dest[dest_size - 1] = '\0'; /* Guaranteed null-terminated */
        return false; /* Truncation occurred */
    }

    return true;
}

/* Incorrect: Classical buffer overflow vulnerability */
static void unsafe_copy(char *dest, const char *src)
{
    /* DANGER: No bounds checking */
    /* strcpy(dest, src); */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Destination buffer overflow using `strcpy`. Passing overlapping buffers to `strcpy` or `strncpy`. Passing `NULL` pointers.
*   **Performance Pitfall (Implementation-Defined):** `strncpy` zeroes out all remaining bytes up to `n`. If `n = 4096` and string length is 5, `strncpy` writes 4091 zero bytes to RAM on every call!

## Edge Cases and Failure Modes
*   **The Unchecked `strncpy` Bug:** Assuming `strncpy` null-terminates when the string is truncated, leaving `dest` non-terminated and triggering subsequent buffer over-reads.
*   **Zero-Padding Latency:** Using `strncpy` on large buffers inside communication loops degrades performance due to unnecessary zero-fill writes.

## Embedded Implications
*   **`snprintf` Code Bloat:** `snprintf` includes formatting engines and float conversions, potentially adding 5-15 KB of Flash ROM overhead on small microcontrollers.
*   **Custom Bounded Copier:** Resource-constrained embedded systems often implement a lightweight, bounded copy routine:
    ```c
    size_t my_strlcpy(char *dst, const char *src, size_t dsize) {
        size_t i = 0;
        if (dsize > 0) {
            while (i < dsize - 1 && src[i] != '\0') { dst[i] = src[i]; i++; }
            dst[i] = '\0';
        }
        while (src[i] != '\0') { i++; }
        return i;
    }
    ```

## Firmware Review Angle
1.  **Ban `strcpy` Completely:** Reject any pull request containing `strcpy`.
2.  **Audit `strncpy` Null-Termination:** Verify that any invocation of `strncpy` is immediately followed by explicit termination: `dest[sizeof(dest) - 1] = '\0'`.
3.  **Detect Truncation:** Check return values of `snprintf` to detect and handle data truncation gracefully.

## Compiler, ABI, and Toolchain Implications
*   **Fortify Source (`-D_FORTIFY_SOURCE=2`):** Modern toolchains substitute `strcpy` calls with compiler-checked built-ins (`__strcpy_chk`) that abort execution if buffer bounds are violated.
*   **Instruction Lowering:** Compilers replace small static `strcpy` calls with vectorized register load/store pairs.

## Performance, Memory, Timing, and Power
*   **Memory Bandwidth Waste:** `strncpy` zero-padding wastes memory write cycles and evicts cache lines.
*   **Cycle Latency:** `memcpy` is generally 2-4x faster than `strcpy` because it transfers data in aligned 32-bit/64-bit words without checking for zero bytes on each byte.

## Verification / Debugging
*   **Compiler Diagnostics:** Use `-Wformat-truncation -Wstringop-overflow`.
*   **Sanitizers:** Compile with AddressSanitizer (`-fsanitize=address`) to trap off-by-one writes immediately.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 21.18:* The `size_t` argument passed to bounded string functions shall not exceed the size of the target buffer.
*   **Security Vulnerabilities:**
    *   CWE-120: Buffer Copy without Checking Size of Input.
    *   CWE-121: Stack-based Buffer Overflow.

## Trade-offs and Alternatives
*   **`strcpy` vs. `strncpy` vs. `snprintf` vs. `memcpy`:**
    *   `strcpy`: Never use.
    *   `strncpy`: Avoid due to missing null-termination and zero-padding overhead.
    *   `snprintf`: Safe, portable, guaranteed null-termination; heavier Flash footprint.
    *   `memcpy`: Fastest possible copy; requires knowing exact lengths beforehand.

## Staff-Level Takeaway
`strcpy` is an unacceptable security hazard; `strncpy` is a flawed legacy API. Staff engineers must ban `strcpy`, restrict `strncpy`, mandate `snprintf` or BSD `strlcpy` for text strings, and enforce `memcpy` for known-length binary/ASCII records to maximize performance and guarantee deterministic null termination.

## Related Concepts
*   [[04_Null_termination]]
*   [[05_strlen_and_sizeof]]
*   [[07_String_concatenation]]
*   [[11_Buffer_sizing]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
