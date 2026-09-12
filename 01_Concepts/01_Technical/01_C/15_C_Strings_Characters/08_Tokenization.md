# 08: Tokenization

## Definition
Tokenization is the lexical analysis process of breaking a contiguous string of text into discrete substrings (tokens) separated by specified delimiter characters. In ISO C, tokenization is traditionally provided by `strtok` (defined in `<string.h>`), POSIX re-entrant variant `strtok_r`, or manual pointer-scanning parsers.

## Scope and Boundaries
*   **Covers:** `strtok` mechanics, internal static state, buffer mutation, re-entrancy issues, thread safety, and safe re-entrant alternatives (`strtok_r`, `strsep`).
*   **Does not cover:** Lexical analysis engines (Lex/Flex), regular expression parsing, or non-destructive string searching (`strstr`, `strchr`).

## Why Does It Exist
Embedded systems and system utilities frequently parse structured text:
*   **Protocol Parsers:** Decoding AT commands (`AT+CWMODE=1`), NMEA GPS sentences (`$GPGGA,123519,...`), or HTTP headers.
*   **Configuration Files:** Parsing key-value pairs (`baud=115200;parity=none`).
*   **Command Line Interpreters:** Splitting CLI shell arguments into `argc` and `argv` structures.

## Mechanism and Language Rules
1.  **In-Place Mutation:** `strtok` replaces each encountered delimiter character in the source string with a null character (`'\0'`). **The input buffer must be mutable.**
2.  **Internal Static State:** `strtok` maintains an internal, unshielded static pointer between calls to track its parsing position across subsequent invocations:
    *   First call: `strtok(str, delim)` begins scanning `str`.
    *   Subsequent calls: `strtok(NULL, delim)` continues scanning where the previous call left off.
3.  **Non-Reentrant:** Because of this global/static state, `strtok` is **not thread-safe** and **cannot be used in re-entrant or nested loops**.
4.  **Consecutive Delimiters:** `strtok` treats multiple consecutive delimiter characters as a single delimiter; it never returns empty tokens.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <string.h>
#include <stdint.h>

/* Correct: Parsing a mutable buffer using re-entrant strtok_r */
static uint32_t example_tokenize(char *command_line)
{
    uint32_t token_count = 0;
    char *saveptr = NULL;
    const char *delimiters = " ,=";

    /* strtok_r maintains state explicitly in saveptr, ensuring thread safety */
    char *token = strtok_r(command_line, delimiters, &saveptr);
    while (token != NULL) {
        token_count++;
        token = strtok_r(NULL, delimiters, &saveptr);
    }

    return token_count;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Passing a string literal or read-only memory buffer to `strtok` (invokes UB upon attempting to write `'\0'`). Calling `strtok` concurrently from multiple threads or an ISR.
*   **Implementation-Defined:** Presence of `strtok_r` (standardized in POSIX, not ISO C99, but supported across GCC/Clang embedded toolchains; C11 Annex K defines `strtok_s`).

## Edge Cases and Failure Modes
*   **The String Literal Crash:**
    ```c
    char *tok = strtok("key=value", "="); /* HARD CRASH: attempts to write '\0' into Flash ROM */
    ```
*   **Nested Loop Desynchronization:** If an outer loop tokenizes lines with `strtok`, and an inner loop tokenizes fields within each line using `strtok`, the inner loop silently overwrites the single global state pointer, corrupting the outer loop permanently.
*   **Discarded Empty Fields:** In CSV parsing (`val1,,val3`), `strtok` skips the empty field and returns `val3` immediately, desynchronizing column indices.

## Embedded Implications
*   **RTOS Multithreading Violations:** Calling `strtok` across multiple FreeRTOS/Zephyr tasks causes race conditions that corrupt the static state pointer.
*   **Interrupt Context Hazards:** Calling `strtok` inside an ISR interrupts any task currently running `strtok`, corrupting the task's parser state.
*   **Destructive Mutation of DMA Buffers:** Because `strtok` injects `'\0'`, original packet buffers are permanently altered, preventing subsequent CRC verification or retransmission without re-copying.

## Firmware Review Angle
1.  **Ban `strtok` Project-Wide:** Mandate `strtok_r` or custom non-destructive parsers; reject bare `strtok`.
2.  **Verify Buffer Mutability:** Ensure the buffer passed to tokenization functions is allocated in mutable RAM, never `.rodata`.
3.  **Check Empty Field Handling:** If protocol specifications require tracking empty fields (e.g., NMEA GPS or CSV), verify that `strsep` or custom scanning is used instead of `strtok_r`.

## Compiler, ABI, and Toolchain Implications
*   **Thread-Local Storage (TLS):** Some standard C libraries (newlib, glibc) implement `strtok` using TLS (`__thread`), but bare-metal MCUs lacking TLS support will fall back to shared static memory.
*   **Optimization Barriers:** In-place modification of strings through external pointers forces the compiler to invalidate all cached memory reads.

## Performance, Memory, Timing, and Power
*   **Zero Dynamic Memory Overhead:** In-place tokenization requires zero dynamic memory allocation (`malloc`), making it fast and memory-efficient.
*   **Predictable Traversal:** Single-pass linear scan ($O(N)$) minimizes CPU cycle consumption.

## Verification / Debugging
*   **Static Analysis:** Analyzers flag `strtok` as a thread-safety violation (CERT C rule CON33-C).
*   **GDB Inspection:** Inspect `saveptr` to track parsing progress during live hardware debugging.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 21.6:* Standard library input/output functions shall not be used.
    *   *Rule 21.1:* Unsafe string manipulation routines shall not be used.
*   **Security Vulnerabilities:**
    *   CWE-676: Use of Potentially Dangerous Function.
    *   State corruption in concurrent networking tasks causes parser desynchronization, enabling denial-of-service or privilege-escalation exploits.

## Trade-offs and Alternatives
*   **`strtok` vs. `strtok_r` vs. `strsep` vs. Custom Index Parser:**
    *   `strtok`: Never use (non-reentrant, destructive).
    *   `strtok_r`: Re-entrant, thread-safe, destructive, skips empty fields.
    *   `strsep`: Re-entrant, handles empty fields, destructive (BSD/POSIX).
    *   *Custom Parser (`strcspn`/`strspn`):* Non-destructive, 100% MISRA compliant, supports immutable buffers.

## Staff-Level Takeaway
`strtok` is obsolete and dangerous due to its hidden static state and destructive buffer modification. Staff engineers must ban `strtok` across all codebases, enforce `strtok_r` for mutable in-place parsing, and mandate non-destructive index scanning (`strspn`/`strcspn`) when parsing packets that must remain intact for logging or checksum verification.

## Related Concepts
*   [[03_String_literals]]
*   [[04_Null_termination]]
*   [[12_Embedded_string_handling]]
*   [[Storage Duration and Lifetime]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
