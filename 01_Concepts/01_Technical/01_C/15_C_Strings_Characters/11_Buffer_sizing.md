# 11: Buffer Sizing

## Definition
Buffer sizing is the engineering calculation and declaration of character array capacities to ensure that memory storage is sufficient to hold worst-case character payloads, formatting expansion, and the mandatory terminating null character without memory overruns or excessive memory waste.

## Scope and Boundaries
*   **Covers:** Capacity sizing formulas, the $+1$ null-terminator rule, integer-to-string buffer limits, formatting expansions, and compile-time capacity validation.
*   **Does not cover:** Dynamic heap reallocation (see [[Dynamic Memory Allocation]]), array declarations in isolation (see [[14_C_Arrays_VLA/01_Array_declaration]]), or DMA buffer alignments (see [[14_C_Arrays_VLA/12_DMA_friendly_array_layouts]]).

## Why Does It Exist
Buffer miscalculations represent the single greatest source of security vulnerabilities in C:
*   **Overflow Prevention:** Ensuring buffers can accommodate worst-case numerical values and text strings.
*   **Stack Protection:** Preventing stack-allocated buffers from overflowing and corrupting return addresses or task frames.
*   **SRAM Budgeting:** Allocating only what is strictly necessary on RAM-constrained embedded devices.

## Mechanism and Language Rules
1.  **The $+1$ Rule:** A buffer must always be sized to at least:
    $$\text{BufferSize} = \text{MaxCharacters} + 1\text{ (for '\0')}$$
2.  **Integer-to-String Sizing Formula:** For an integer type of $B$ bits, the maximum number of decimal digits is calculated mathematically by:
    $$\text{Digits} = \lceil B \times \log_{10}(2) \rceil \approx \lceil B \times 0.30103 \rceil$$
    *   Add 1 byte for optional negative sign (`-`).
    *   Add 1 byte for the terminating null character (`\0`).
    *   *Standard Capacities:*
        *   `int8_t`: $-128$ -> 4 chars + 1 null = **5 bytes**.
        *   `uint8_t`: $255$ -> 3 chars + 1 null = **4 bytes**.
        *   `int16_t`: $-32768$ -> 6 chars + 1 null = **7 bytes**.
        *   `uint16_t`: $65535$ -> 5 chars + 1 null = **6 bytes**.
        *   `int32_t`: $-2147483648$ -> 11 chars + 1 null = **12 bytes**.
        *   `uint32_t`: $4294967295$ -> 10 chars + 1 null = **11 bytes**.
        *   `int64_t`: $-9223372036854775808$ -> 20 chars + 1 null = **21 bytes**.
        *   `uint64_t`: $18446744073709551615$ -> 20 chars + 1 null = **21 bytes**.
3.  **Float / Double Sizing:** Converting IEEE-754 floats (`float`) to string safely requires at least **16 bytes**; doubles require at least **32 bytes** (up to **320+ bytes** for worst-case non-scientific notation).

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stdio.h>
#include <stddef.h>
#include <stdbool.h>

/* Worst-case decimal buffer sizing for int32_t:
 * -2147483648 (11 chars) + '\0' (1 char) = 12 bytes */
#define INT32_STR_BUFFER_SIZE 12U

static bool format_int32(char *out_buf, size_t buf_size, int32_t value)
{
    if (out_buf == NULL || buf_size < INT32_STR_BUFFER_SIZE) {
        return false; /* Buffer insufficient for worst-case payload */
    }

    (void)snprintf(out_buf, buf_size, "%ld", (long)value);
    return true;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Writing past the allocated buffer bounds when formatted data exceeds buffer capacity (e.g., using `sprintf` instead of `snprintf`).
*   **Implementation-Defined:** String length formatting behavior of floats with extreme exponents (`printf("%f", 1e38)`).

## Edge Cases and Failure Modes
*   **The Sprintf Guessing Game:** Guessing buffer sizes arbitrarily (`char buf[10]; sprintf(buf, "%d", val);`). If `val = -2147483648`, `sprintf` writes 12 bytes, overflowing the 10-byte stack buffer and causing immediate memory corruption.
*   **Truncation Oblivion:** Calling `snprintf` prevents buffer overflow, but failing to check the return value means downstream systems process truncated, malformed commands or file paths.

## Embedded Implications
*   **Stack Budget Inflation:** Declaring overly defensive buffers (`char buf[1024];`) inside FreeRTOS tasks with 2 KB stacks blows through the stack budget, causing silent stack overflow. Buffers must be sized strictly to mathematical worst-case bounds.
*   **Static Compile-Time Sizing:** Sizing buffers using symbolic constants allows compile-time verification using `_Static_assert`:
    ```c
    _Static_assert(sizeof(g_tx_buf) >= (MAX_PAYLOAD + 1), "TX Buffer too small");
    ```

## Firmware Review Angle
1.  **Audit Integer Buffer Sizes:** Verify that all integer-to-string buffers match standard mathematical capacities (e.g., 12 bytes for 32-bit signed ints).
2.  **Verify Suffix Storage:** Check that string builders leave room for protocol framing (e.g., `\r\n\0`).
3.  **Ban Arbitrary Powers of 2:** Challenge arbitrary buffer declarations like `char buf[256];` if the data model only requires 16 bytes.

## Compiler, ABI, and Toolchain Implications
*   **Stack Canaries:** Modern compilers insert canaries next to local character arrays (`-fstack-protector-strong`) to trap overflows resulting from undersized buffers.
*   **Format String Diagnostics:** Compilers analyze `snprintf` format strings and warn if the destination buffer is statically too small to hold the formatted output (`-Wformat-truncation`).

## Performance, Memory, Timing, and Power
*   **SRAM Optimization:** Exact-fit buffer sizing preserves limited SRAM on microcontrollers.
*   **Execution Determinism:** Correctly sized buffers ensure `snprintf` never truncates, eliminating error handling branches.

## Verification / Debugging
*   **Compiler Warnings:** Enforce `-Wformat -Wformat-truncation=2`.
*   **Static Assertions:** Validate struct and buffer capacity limits at compile time.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 18.1:* A pointer resulting from arithmetic shall address elements of the same array.
*   **Security Vulnerabilities:**
    *   CWE-120: Classic Buffer Overflow.
    *   CWE-131: Incorrect Calculation of Buffer Size.

## Trade-offs and Alternatives
*   **Worst-Case Fixed Sizing vs. Dynamic Heap Allocation:**
    *   *Worst-Case Fixed:* Predictable, zero heap fragmentation, statically verifiable; consumes worst-case memory continuously.
    *   *Dynamic Heap (`malloc`):* Conserves memory when payloads are small; introduces heap fragmentation, latency, and allocation failure states.

## Staff-Level Takeaway
Buffer sizing is an exact mathematical science, not a guessing game. Staff engineers must eliminate magic buffer sizes across codebases, mandate formal mathematical sizing formulas for integer and telemetry buffers, enforce compile-time `_Static_assert` capacity checks, and verify all formatted outputs use bounds-checked APIs (`snprintf`).

## Related Concepts
*   [[04_Null_termination]]
*   [[05_strlen_and_sizeof]]
*   [[06_String_copying]]
*   [[14_C_Arrays_VLA/01_Array_declaration]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
