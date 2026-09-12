# 07: String Concatenation

## Definition
String concatenation is the process of appending one string sequence onto the end of an existing string buffer, maintaining a single terminating null character. In ISO C, concatenation is provided by standard library routines (`strcat`, `strncat`), formatted functions (`snprintf`), and modern bounded APIs (`strlcat`).

## Scope and Boundaries
*   **Covers:** `strcat`, `strncat`, `snprintf` concatenation, buffer capacity tracking, truncation detection, and quadratic traversal pitfalls.
*   **Does not cover:** Compile-time string literal concatenation (see [[03_String_literals]]), string copying (see [[06_String_copying]]), or wide string concatenation (`wcscat`).

## Why Does It Exist
Dynamic message construction is ubiquitous:
*   **Path Construction:** Building file system paths (`"/mnt/flash/" + "config.bin"`).
*   **Command Building:** Assembling AT modem commands, SQL queries, or HTTP header lines.
*   **Logging:** Appending status strings and timestamps to diagnostic logs.

## Mechanism and Language Rules
1.  **`strcat(dest, src)`:** Appends `src` to `dest`, overwriting the original null terminator of `dest` and appending a new `'\0'`. It performs **no bounds checking**; if `dest` lacks sufficient space, a buffer overflow occurs.
2.  **`strncat(dest, src, n)` (Subtle Rule):**
    *   Appends at most `n` characters from `src`.
    *   **Always appends a terminating null character** (unlike `strncpy`).
    *   Requires that `dest` has room for its existing string, plus at most `n` characters, **plus 1 byte for `'\0'`**.
    *   Parameter `n` is the maximum number of bytes to take from `src`, **NOT** the total capacity of `dest`!
3.  **No Overlap:** Source and destination strings must not overlap in memory.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <string.h>
#include <stdio.h>
#include <stdbool.h>

#define LOG_BUFFER_SIZE 64U

/* Correct: Safe concatenation using snprintf with length tracking */
static bool append_status(char *buf, size_t buf_size, const char *status)
{
    size_t current_len = strlen(buf);
    if (current_len >= buf_size) {
        return false;
    }

    int written = snprintf(buf + current_len, buf_size - current_len, " %s", status);
    return (written >= 0 && (size_t)written < (buf_size - current_len));
}

/* Correct: Classic strncat with correct remaining capacity calculation */
static void example_strncat(char *dest, size_t dest_capacity, const char *suffix)
{
    size_t len = strlen(dest);
    if (dest_capacity > len + 1U) {
        /* Room left excluding the null terminator */
        size_t remaining = dest_capacity - len - 1U;
        strncat(dest, suffix, remaining);
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Buffer overflow via `strcat`. Calculating an invalid negative remaining size for `strncat`. Passing overlapping memory regions.
*   **Algorithmic Hazard (Schlemiel the Painter's Algorithm):** Repeatedly appending with `strcat` repeatedly scans from the beginning of `dest` to find the null terminator on every call, creating quadratic $O(N^2)$ execution latency.

## Edge Cases and Failure Modes
*   **The `strncat` Size Misunderstanding:** Passing `sizeof(dest)` as the third argument to `strncat`:
    ```c
    strncat(dest, src, sizeof(dest)); /* BUG: appends up to sizeof(dest) bytes, causing overflow */
    ```
*   **Quadratic Scaling in Loops:** Appending characters in a loop using `strcat` turns a simple linear build into a high-latency loop that can stall embedded control loops.

## Embedded Implications
*   **RTOS Logging Latency:** Concentrating diagnostic strings via repeated `strcat` calls introduces variable execution latency, inducing jitter in real-time tasks.
*   **Pointer Tracking Idiom:** Instead of `strcat`, track the write pointer and remaining space directly:
    ```c
    char *ptr = buf;
    size_t rem = sizeof(buf);
    // Advance ptr and decrement rem on each append: O(N) performance
    ```

## Firmware Review Angle
1.  **Ban `strcat`:** Reject `strcat` project-wide.
2.  **Audit `strncat` Third Parameter:** Ensure the third argument to `strncat` is `capacity - current_len - 1`, never `sizeof(dest)`.
3.  **Detect $O(N^2)$ Loop Appends:** Flag repeated concatenation inside loops; rewrite to track the tail pointer.

## Compiler, ABI, and Toolchain Implications
*   **Built-in Optimization:** Modern compilers optimize `strcat(dest, "c")` to direct byte store instructions if destination bounds are statically known.
*   **Security Built-ins:** Toolchains replace `strcat` with `__strcat_chk` under `-D_FORTIFY_SOURCE=2`.

## Performance, Memory, Timing, and Power
*   **Quadratic Latency Penalty:** Repeatedly calling `strcat` to append $K$ small fragments of length $M$ costs $O(K^2 \cdot M)$ cycles. Pointer-tracking appending costs $O(K \cdot M)$ cycles.
*   **Cache Thrashing:** Constant re-scanning of the destination string keeps CPU load lines active unnecessarily.

## Verification / Debugging
*   **Compiler Warnings:** Use `-Wstringop-overflow -Wformat-overflow`.
*   **Sanitizers:** Compile with AddressSanitizer (`-fsanitize=address`) to catch off-by-one concatenation overruns.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 21.18:* The size argument to bounded string functions shall not exceed remaining buffer capacity.
*   **Security Vulnerabilities:**
    *   CWE-120: Buffer Copy without Checking Size of Input.
    *   CWE-131: Incorrect Calculation of Buffer Size.

## Trade-offs and Alternatives
*   **`strcat` vs. `strncat` vs. `snprintf` vs. Pointer Tracking:**
    *   `strcat`: Unsafe; never use.
    *   `strncat`: Tricky sizing math; easy to misuse.
    *   `snprintf(buf + len, rem, ...)`: Clean, robust, format-capable.
    *   *Pointer Tracking:* Absolute highest performance; zero redundant memory scans.

## Staff-Level Takeaway
`strcat` is fundamentally unsafe and algorithmically flawed. Staff engineers must mandate pointer-tracking buffers or `snprintf` offset arithmetic for string assembly, completely eliminate bare `strcat`, and audit `strncat` invocations to verify that the length parameter represents *remaining* buffer capacity rather than total buffer size.

## Related Concepts
*   [[04_Null_termination]]
*   [[05_strlen_and_sizeof]]
*   [[06_String_copying]]
*   [[11_Buffer_sizing]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
