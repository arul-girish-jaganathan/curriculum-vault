# 12: Embedded String Handling

## Definition
Embedded string handling is the architectural discipline of processing, parsing, and formatting text strings within resource-constrained, real-time, and safety-critical firmware without triggering stack overflows, unbounded execution latencies, dynamic memory fragmentation, or security vulnerabilities.

## Scope and Boundaries
*   **Covers:** Safe zero-allocation string parsing, bounded execution time, Flash-based string storage, real-time logging, and defensive string architectures.
*   **Does not cover:** General desktop C string libraries, graphical font rendering, or operating system localization.

## Why Does It Exist
Standard C string library functions are fundamentally ill-suited for bare-metal and RTOS environments:
*   **Unbounded Latencies:** Routines like `strlen`, `strcpy`, and `strcmp` execute unbounded memory scans, violating real-time determinism.
*   **Stack Bloat:** Heavy formatting routines like `sprintf` pull in massive floating-point and formatting engines, exhausting Flash and blowing small task stacks.
*   **Lack of Heap:** Embedded systems generally ban dynamic memory allocation (`malloc`/`free`), requiring static or bounded in-place text manipulation.

## Mechanism and Language Rules
1.  **Flash Memory Conservation:** Immutable text strings must be declared `static const char * const` or placed in `.rodata` to ensure zero RAM consumption.
2.  **Bounded String Primitives:** All string operations must be bounded by explicit buffer capacities (e.g., `strnlen`, `strncmp`, `snprintf`). Unbounded functions (`strcpy`, `strcat`, `gets`, `sprintf`) are banned.
3.  **Lightweight Formatters:** Replace full standard library `printf`/`snprintf` with minimalist, non-allocating embedded implementations (e.g., `tiny-printf`, `mpb-printf`) that omit floating point and locale overhead.
4.  **String Spans / Slices:** Representing strings via pointer-and-length structures:
    ```c
    struct StringSpan {
        const char *data;
        size_t length;
    };
    ```
    This enables non-destructive tokenization and substring extraction without injecting `'\0'` characters or copying memory blocks.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

/* String Span: Zero-copy, non-destructive embedded string view */
struct StringView {
    const char *data;
    size_t len;
};

/* Compare string view without null termination or memory mutation */
static bool string_view_equals(struct StringView view, const char *literal)
{
    size_t i = 0;
    while (i < view.len && literal[i] != '\0') {
        if (view.data[i] != literal[i]) {
            return false;
        }
        i++;
    }
    return (i == view.len && literal[i] == '\0');
}

static bool example_embedded_parse(const char *rx_stream, size_t rx_len)
{
    /* Zero-copy view into RX stream */
    struct StringView cmd = { .data = rx_stream, .len = (rx_len > 4) ? 4 : rx_len };
    return string_view_equals(cmd, "PING");
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Passing non-null-terminated buffers to standard string APIs. Attempting to modify Flash-resident string literals during in-place tokenization.
*   **Implementation-Defined:** Calling conventions and register parameter usage for string pointers across RTOS context switches.

## Edge Cases and Failure Modes
*   **The Interrupt `printf` Disaster:** Calling `printf` inside an Interrupt Service Routine (ISR). Standard `printf` is non-reentrant, uses locks, takes unpredictable CPU cycles, and causes priority inversions or deadlocks.
*   **Flash-to-RAM Duplication:** Declaring string tables as `const char *table[] = {...};` places the string literals in Flash, but allocates the array of pointers in RAM. To keep both in Flash, use `const char * const table[]`.

## Embedded Implications
*   **Asynchronous Circular Logging:** Modern firmware logs text by pushing formatted message IDs and integer arguments into a lock-free circular ring buffer in RAM, deferring string expansion and UART transmission to a low-priority background thread.
*   **DMA Packet Alignment:** When sending text strings over UART via DMA, buffers must be aligned to hardware DMA and cache-line boundaries (see [[14_C_Arrays_VLA/12_DMA_friendly_array_layouts]]).

## Firmware Review Angle
1.  **Zero-Tolerance for Unbounded APIs:** Ban `sprintf`, `vsprintf`, `strcpy`, `strcat`, and `gets` via automated CI linting.
2.  **No Strings in ISRs:** Strictly prohibit string formatting and logging inside interrupt handlers.
3.  **Flash Qualifiers:** Ensure all static string tables are double-const qualified (`const char * const`).
4.  **No Heap Usage:** Verify string operations allocate memory exclusively from static pools or verified stack buffers.

## Compiler, ABI, and Toolchain Implications
*   **Linker Garbage Collection:** Use `-ffunction-sections -fdata-sections -Wl,--gc-sections` to eliminate unused string tables and formatting engines from the final ELF binary.
*   **Nano-Specs:** Linking against `-specs=nano.specs` (in ARM GCC) replaces the full standard C library with a stripped-down implementation lacking bloated floating-point printf logic.

## Performance, Memory, Timing, and Power
*   **ROM Savings:** Replacing standard `printf` with integer-only `snprintf` saves 10-30 KB of Flash memory.
*   **Cycle Determinism:** Bounded string spans and pointer-walking algorithms execute in bounded, predictable cycle counts, preventing real-time deadline misses.
*   **Power Optimization:** Eliminating quadratic string re-scans reduces CPU active time, allowing faster returns to low-power Sleep/Stop modes.

## Verification / Debugging
*   **Compiler Flags:** Enforce `-Wformat=2 -Wformat-security -Werror=format-security`.
*   **Stack Monitoring:** Use GCC `-fstack-usage` to track stack frame footprints of functions handling string formatting.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 21.6:* The Standard Library input/output functions shall not be used in production code.
    *   *Rule 21.1:* Standard library string handling functions shall be bounded and validated.
*   **Security Hazards:**
    *   CWE-134: Use of Externally-Controlled Format String.
    *   CWE-120: Classic Buffer Overflow.

## Trade-offs and Alternatives
*   **Standard C Strings vs. String Views / Spans:**
    *   *Standard C Strings (`char *`):* Universally supported, requires null terminators, prone to destructive mutation and out-of-bounds reads.
    *   *String Views (`{ptr, len}`):* Zero-copy, non-destructive, supports binary slices, safe for non-terminated buffers; requires custom or modernized helper functions.

## Staff-Level Takeaway
Standard C string handling is fundamentally incompatible with safe, deterministic embedded systems. Staff engineers must ban unbounded string functions project-wide, mandate double-const qualifiers for Flash string tables, enforce non-blocking asynchronous logging architectures, and adopt zero-copy string span patterns to guarantee memory safety and real-time execution determinism.

## Related Concepts
*   [[03_String_literals]]
*   [[04_Null_termination]]
*   [[06_String_copying]]
*   [[08_Tokenization]]
*   [[11_Buffer_sizing]]
*   [[14_C_Arrays_VLA/12_DMA_friendly_array_layouts]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
