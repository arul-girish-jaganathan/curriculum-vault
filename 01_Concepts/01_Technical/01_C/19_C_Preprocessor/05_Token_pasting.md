# 05: Token Pasting

## Definition
The token-pasting operator `##` (also called the token concatenation operator) merges two preprocessing tokens into a single composite preprocessing token during macro replacement in Translation Phase 4. If the resulting token is not a syntactically valid C preprocessing token, the behavior is undefined.

## Scope and Boundaries
Covers: The `##` operator, identifier generation, register mapping synthesis, placemarker tokens, argument prescan suppression, and two-level concatenation idioms.
Does not cover: String literal concatenation (which occurs automatically in Phase 6).

## Why Does It Exist
Token pasting provides metaprogramming capabilities in C. It enables automated generation of repetitive boilerplate code, synthesizing hardware register names, dispatch tables, and type-specific polymorphic data structures.

## Mechanism and Language Rules
1. **Operand Rule:** The `##` operator must appear between two preprocessing tokens in the replacement list of a macro. It cannot appear as the very first or very last token of the replacement list.
2. **Prescan Suppression:** Like the `#` operator, `##` disables argument prescan for its immediate operands. If an operand is itself a macro, it will NOT be expanded before pasting unless passed through an indirection macro.
3. **Validity Requirement:** The concatenated result must be a valid preprocessing token (e.g., pasting `var_` and `1` yields `var_1`). Pasting `+` and `-` does not form a single token and invokes Undefined Behavior.
4. **Placemarker Tokens (C99+):** If an operand is empty, it is treated as a "placemarker" token; pasting a placemarker with a token yields the original token.

## Examples
```c
#include <stdint.h>
#include <assert.h>

/* Two-level token pasting indirection */
#define CONCAT_IMPL(a, b)   a ## b
#define CONCAT(a, b)        CONCAT_IMPL(a, b)

/* Automated Hardware Register Synthesizer */
#define USART_REG(port, reg) CONCAT(USART, CONCAT(port, CONCAT(_, reg)))

/* Generates: USART1_CR1 */
#define USART1_CR1  0x40011000UL

/* Type-Specific Vector Struct Generator (C Metaprogramming Pattern) */
#define DECLARE_BUFFER(type, name, size)     typedef struct {                             type data[size];                         uint32_t head;                           uint32_t tail;                       } CONCAT(name, _buffer_t)

DECLARE_BUFFER(uint8_t, uart_rx, 128);
/* Synthesizes: typedef struct { ... } uart_rx_buffer_t; */

static void test_token_paste(void) {
    uint32_t addr = USART_REG(1, CR1);
    assert(addr == 0x40011000UL);

    uart_rx_buffer_t rx_buf = { .head = 0, .tail = 0 };
    assert(sizeof(rx_buf.data) == 128);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Invalid Token Generation:** Pasting two tokens that do not form a single valid C token (such as pasting `foo` and `?`) invokes Undefined Behavior (ISO C99 §6.10.3.3).

## Edge Cases and Failure Modes
- **The Direct Pasting Trap:**
  ```c
  #define PIN 4
  #define PORT GPIO_ ## PIN /* Expands to: GPIO_PIN, NOT GPIO_4! */
  ```
  Because `##` suppresses prescan, `PIN` is not expanded to `4`. You must use two-level indirection `CONCAT(GPIO_, PIN)`.
- **Leading/Trailing Operator Placement:** Placing `##` at the boundary of a replacement list (`#define BAD(x) ## x`) is a constraint violation and will not compile.

## Embedded Implications
- **Pin & Peripheral Multiplexing:** Microcontroller HALs heavily use `CONCAT` to bind generic driver code to concrete hardware pins (e.g., `GPIO_PIN_ ## n`, `DMA_STREAM_ ## x`).
- **Code Size Optimization:** Token pasting allows generating dense, type-safe ring buffers and data structures without relying on heavy C++ templates.

## Firmware Review Angle
- Confirm that token pasting is wrapped in two-level indirection macros (`CONCAT(a, b)`).
- Ensure generated identifiers do not violate project naming conventions or shadow existing symbols.

## Compiler, ABI, and Toolchain Implications
- Token pasting occurs in the lexical phase; the generated identifiers are placed directly into the symbol table without any runtime cost.

## Performance, Memory, Timing, and Power
- Absolute zero runtime or memory overhead.

## Verification / Debugging
- Inspect generated tokens with `gcc -E` to ensure valid identifier formation.
- Static analyzers may struggle to trace symbols synthesized via heavy token pasting; use macro-aware tools.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 20.10: The `#` and `##` preprocessor operators should not be used. (Restricted because token pasting can obscure symbol origins and hinder static analysis; use only where approved by architectural design).

## Trade-offs and Alternatives
- **Token Pasting vs. Explicit Code:** Token pasting reduces boilerplate dramatically, but makes searching codebases (`grep`) difficult because the synthesized identifier names do not appear verbatim in source files.

## Staff-Level Takeaway
Token pasting is C's native metaprogramming engine. Always implement it using a two-tier macro architecture (`CONCAT(a, b)`) to ensure argument expansion, verify that synthesized tokens form strictly valid C identifiers, and balance boilerplate reduction against code searchability.

## Related Concepts
- `02_Macro_expansion`
- `04_Stringification`
- `12_Preprocessor_architecture`
