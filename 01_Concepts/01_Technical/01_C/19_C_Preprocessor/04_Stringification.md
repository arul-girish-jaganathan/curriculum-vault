# 04: Stringification

## Definition
The stringification operator `#` (also known as the stringize operator) is a unary preprocessor operator that converts a function-like macro's argument into a string literal. It is evaluated during Translation Phase 4 before the replacement list is rescanned for further macros.

## Scope and Boundaries
Covers: The `#` operator, token stringizing mechanics, whitespace collapsing, quote and escape sequence injection, and the canonical two-level stringification idiom.
Does not cover: Runtime string formatting (`sprintf`) or wide/Unicode stringification (`L#` is not standard ISO C).

## Why Does It Exist
Stringification allows developers to capture code identifiers, macro expressions, and line numbers as readable strings for assertions, diagnostic logging, symbol lookup tables, and automated debugging frameworks.

## Mechanism and Language Rules
1. **Operand Rule:** The `#` operator can ONLY be used inside the replacement list of a function-like macro, immediately preceding a macro parameter.
2. **Escape Character Injection:** The preprocessor automatically inserts backslashes before internal quotation marks `"` and backslashes `\` contained within the stringized argument.
3. **Whitespace Normalization:** Leading and trailing whitespaces are stripped; sequences of internal whitespace characters are collapsed into a single space.
4. **No Argument Prescan:** The `#` operator disables argument prescan for its operand. To stringify the *expansion* of a macro rather than its raw identifier, a two-level macro indirection is required.

## Examples
```c
#include <stdio.h>
#include <assert.h>

#define STRINGIFY_NAIVE(x)      #x
#define STRINGIFY(x)            STRINGIFY_IMPL(x)
#define STRINGIFY_IMPL(x)       #x

#define MAJOR_VERSION           2
#define MINOR_VERSION           4

/* Diagnostic Assertion Pattern */
#define ASSERT_LOG(expr)     do {         if (!(expr)) {             log_fault("Assertion failed: " #expr " at " __FILE__ ":" STRINGIFY(__LINE__));             fault_handler();         }     } while(0)

static void test_stringification(void) {
    /* Naive stringification prints the literal macro name */
    assert(strcmp(STRINGIFY_NAIVE(MAJOR_VERSION), "MAJOR_VERSION") == 0);

    /* Two-level stringification expands the macro before stringizing */
    assert(strcmp(STRINGIFY(MAJOR_VERSION), "2") == 0);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Using the `#` operator on a token sequence that does not form a valid string literal element produces undefined or ill-formed output.

## Edge Cases and Failure Modes
- **The Single-Level Trap:** Writing `#x` directly on a macro like `__LINE__` results in the literal string `"__LINE__"` rather than the line number `"42"`. Always use the two-level `STRINGIFY(x)` helper pattern.
- **Embedded Comments:** Comments inside arguments are replaced by a single space before the `#` operator executes.

## Embedded Implications
- **Firmware Build Metadata:** Stringification is universally used to bake build timestamps, Git commit hashes, and semantic versions into flash strings for bootloader identification:
  `-DGIT_COMMIT=0x3f4a2e` -> `STRINGIFY(GIT_COMMIT)` creates `"0x3f4a2e"`.

## Firmware Review Angle
- Confirm that any macro performing stringification uses the two-tier indirection (`STRINGIFY` -> `STRINGIFY_IMPL`).
- Verify that stringized tokens do not inadvertently leak private variable names or internal passwords into production flash strings.

## Compiler, ABI, and Toolchain Implications
- Adjacent string literals resulting from stringification concatenate automatically during Translation Phase 6:
  `"Version: " STRINGIFY(MAJOR) "." STRINGIFY(MINOR)` seamlessly forms `"Version: 2.4"`.

## Performance, Memory, Timing, and Power
- String literals created by `#` reside in read-only data segments (`.rodata` in Flash). Excessive stringification in assertions can rapidly exhaust microcontroller Flash memory.

## Verification / Debugging
- Use `gcc -E` to verify that stringification produces valid, well-escaped string literals.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 20.10: The `#` and `##` preprocessor operators should not be used. (Advisory rule; safety-critical systems restrict stringification to approved diagnostic macros to prevent obfuscation).

## Trade-offs and Alternatives
- **Compile-Time Stringification vs. Runtime Buffers:** Stringification produces zero-overhead compile-time constants in ROM, avoiding `snprintf` execution cycles and RAM buffer allocations.

## Staff-Level Takeaway
Never use single-level stringification on parameterized macros. Adopt standard two-level indirection macros (`STRINGIFY(x)`) across your firmware infrastructure, and remain vigilant of the Flash memory consumption of stringized debug assertions.

## Related Concepts
- `02_Macro_expansion`
- `05_Token_pasting`
- `06_Predefined_macros`
