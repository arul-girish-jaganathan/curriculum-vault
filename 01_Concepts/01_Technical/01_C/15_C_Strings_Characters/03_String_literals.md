# 03: String Literals

## Definition
A string literal is a sequence of zero or more multibyte characters enclosed in double quotes (e.g., `"hello"`). In ISO C (C99 §6.4.5), a string literal has static storage duration, is stored as an array of characters initialized with the given characters plus an implicit terminating null character (`\0`), and attempting to modify it invokes undefined behavior.

## Scope and Boundaries
*   **Covers:** String literal syntax, static storage duration, array decay, string pooling/deduplication, write protection in `.rodata`, and concatenation of adjacent literals.
*   **Does not cover:** Modifiable character arrays (see [[14_C_Arrays_VLA/01_Array_declaration]]), character pointers (see [[13_C_Pointers/01_Pointer_declarations]]), or string manipulation functions (see [[06_String_copying]]).

## Why Does It Exist
Programs require static text representations:
*   **Human Interface:** Diagnostic logs, user interface text, error messages, and AT command strings.
*   **Zero Startup Overhead:** Instantiated directly in non-volatile memory (Flash/ROM) at compile time without requiring dynamic allocation or boot-time initialization loops.
*   **Literal Concatenation:** Allowing preprocessor macros and long strings to span multiple lines cleanly.

## Mechanism and Language Rules
1.  **Type and Storage:** In ISO C, `"abc"` has type `char[4]` (array of 4 `const`-less `char`s, including `\0`), with static storage duration.
2.  **Immutability Rule (C99 §6.4.5p6):** If the program attempts to modify the memory where a string literal is stored, the behavior is undefined.
3.  **Automatic Concatenation:** Adjacent string literals separated only by whitespace or newlines are concatenated into a single string literal at translation phase 6:
    ```c
    const char *p = "Hello, " "World!"; /* Evaluates to "Hello, World!" */
    ```
4.  **Array Initialization Special Case:**
    *   `char str[] = "abc";`: Allocates a **mutable** 4-byte automatic array on the stack, copied from the literal.
    *   `const char *str = "abc";`: Allocates a pointer variable pointing directly to the immutable literal in Flash/ROM.
5.  **String Pooling / Merging:** Compilers are permitted to share identical string literals (or suffixes of literals) in memory to reduce storage.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>

/* Correct: Pointer to const ensuring immutability contract */
static const char * const g_firmware_version = "v1.2.3";

/* Correct: Mutable local copy initialized by string literal */
static void example_literal_usage(void)
{
    char mutable_buf[] = "CONFIG"; /* Safe to modify: lives on stack */
    mutable_buf[0] = 'c';
    (void)mutable_buf;
}

/* Incorrect: Attempting to modify a string literal */
static void invalid_literal_write(void)
{
    char *p = "immutable";
    /* *p = 'I'; */ /* Undefined Behavior: hardware bus fault / crash */
    (void)p;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Undefined Behavior:** Modifying a string literal (e.g., `((char *)"literal")[0] = 'x'`). Passing a string literal to a function that casts away `const` and mutates the buffer.
*   **Unspecified Behavior:** Whether identical string literals represent distinct objects or point to shared memory addresses (string pooling).
*   **Implementation-Defined:** The memory section where string literals are allocated (typically `.rodata` in Flash).

## Edge Cases and Failure Modes
*   **The Non-Const Pointer Trap:** In C (unlike C++), string literals are typed as `char[]` rather than `const char[]`. Assigning a literal to a non-const pointer (`char *p = "read_only";`) compiles without error in C, but writing to `*p` triggers an immediate runtime HardFault.
*   **Accidental Missing Commas in Array Tables:**
    ```c
    const char *cmds[] = { "START", "STOP" "RESET" }; /* Bug: "STOP" and "RESET" merge! */
    ```

## Embedded Implications
*   **Flash vs. RAM Placement:** String literals are allocated in the `.rodata` section (Flash/ROM). Accessing string literals directly via `const char *` consumes zero SRAM.
*   **DMA Transfer Hazards:** Some low-power MCUs cannot perform DMA transfers directly out of Flash memory (`.rodata`). If a UART DMA driver is passed a string literal pointer directly, the DMA engine may hang or fault.
*   **Printf Logging Bloat:** Excessive string literals in logging macros (`printf("Error at step %d\n", i);`) inflate Flash ROM usage rapidly.

## Firmware Review Angle
1.  **Mandate `const char *`:** Strictly prohibit declaring pointers to string literals as plain `char *`; enforce `const char *`.
2.  **Audit Array Initializers:** Inspect arrays of string pointers for missing commas that cause inadvertent string literal concatenation.
3.  **DMA Sourced from Flash:** Check whether hardware communication drivers attempting DMA transfers accept pointers to `.rodata` string literals.

## Compiler, ABI, and Toolchain Implications
*   **String Deduplication:** Compilers with `-fmerge-constants` merge identical string literals across the entire translation unit or binary (via LTO).
*   **Section Allocation:** Placed in the `.rodata` section, enforced as read-only by the MPU/MMU.

## Performance, Memory, Timing, and Power
*   **Zero SRAM Footprint:** Directly referenced literals consume zero RAM; they execute directly from Flash memory.
*   **Cache Line Efficiency:** Merged string literals reduce instruction and data cache pressure.

## Verification / Debugging
*   **Compiler Flags:** Use `-Wwrite-strings` to treat string literals as `const char[]`, triggering warnings on non-const assignments.
*   **Map File Inspection:** Verify `.rodata` segment growth caused by string literals in the linker `.map` file.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 11.8:* A cast shall not remove any `const` or `volatile` qualification.
*   **Security Vulnerabilities:** Attempting to write to string literals crashes the system, causing Denial of Service (DoS).

## Trade-offs and Alternatives
*   **`const char *p = "..."` vs. `char p[] = "..."`:**
    *   `const char *`: Zero RAM usage, immutable, Flash-resident.
    *   `char []`: Consumes stack RAM, mutable, requires Flash-to-RAM copy on function entry.

## Staff-Level Takeaway
String literals are immutable, Flash-resident arrays. Staff engineers must enforce `-Wwrite-strings` across build systems to enforce `const char *` typing, prevent accidental literal mutations, audit arrays of strings for missing comma concatenation bugs, and verify DMA controllers can physically access Flash memory when transmitting string literals.

## Related Concepts
*   [[01_Character_types]]
*   [[04_Null_termination]]
*   [[13_C_Pointers/06_const_pointer_combinations]]
*   [[Linker Scripts and Memory Sections]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
