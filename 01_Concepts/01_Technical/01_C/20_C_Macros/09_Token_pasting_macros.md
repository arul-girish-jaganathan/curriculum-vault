# 09: Token Pasting Macros

## Definition
A token-pasting macro is a function-like macro that uses the `##` preprocessor operator to concatenate two separate preprocessing tokens into a single composite token during Translation Phase 4. It enables compile-time metaprogramming, synthetic identifier construction, and automated code generation.

## Scope and Boundaries
Covers: The `##` operator, identifier synthesis, hardware pin/register binding, placemarker tokens, and the two-level concatenation idiom.
Does not cover: String literal concatenation or runtime string formatting.

## Why Does It Exist
C does not support templates or dynamic reflection. Token pasting provides a macro-level metaprogramming mechanism to generate type-specific functions, build peripheral register lookups, and bind abstract HAL drivers to physical silicon pins without manual boilerplate.

## Mechanism and Language Rules
1. **Operator Placement:** The `##` operator must appear between two preprocessing tokens in the replacement list.
2. **Prescan Suppression:** Like `#`, the `##` operator suppresses argument prescan. Arguments adjacent to `##` are NOT expanded before pasting unless routed through a two-level indirection macro.
3. **Valid Token Requirement:** Concatenating two tokens must yield a syntactically valid C token (e.g., `pin_` and `5` yields `pin_5`). Concatenations that form invalid tokens (e.g., `foo` and `%`) invoke Undefined Behavior.
4. **Two-Level Indirection Pattern:**
   ```c
   #define CONCAT(a, b)        CONCAT_IMPL(a, b)
   #define CONCAT_IMPL(a, b)   a ## b
   ```

## Examples
```c
#include <stdint.h>
#include <assert.h>

/* The Canonical Two-Tier Token-Pasting Macro */
#define CONCAT(a, b)        CONCAT_IMPL(a, b)
#define CONCAT_IMPL(a, b)   a ## b

/* Automated Hardware Register Mapping */
#define PORT_A              A
#define PIN_LED             5

/* Generates: GPIOA_PIN_5 */
#define LED_PIN_ID          CONCAT(GPIO, CONCAT(PORT_A, CONCAT(_PIN_, PIN_LED)))

#define GPIOA_PIN_5         0x0020U

/* Generic Type-Safe Queue Implementation Pattern */
#define DECLARE_STATIC_QUEUE(type, name, depth)     typedef struct {         type     buffer[depth];         uint32_t head;         uint32_t tail;     } CONCAT(name, _queue_t)

DECLARE_STATIC_QUEUE(uint8_t, uart_rx, 64);
/* Synthesizes: typedef struct { ... } uart_rx_queue_t; */

static void test_token_pasting(void) {
    assert(LED_PIN_ID == 0x0020U);

    uart_rx_queue_t q = { .head = 0, .tail = 0 };
    assert(sizeof(q.buffer) == 64);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Merging tokens that do not form a valid preprocessing token invokes Undefined Behavior (§6.10.3.3).

## Edge Cases and Failure Modes
- **The Direct Pasting Trap:**
  ```c
  #define PIN 4
  #define GET_REG(p) GPIO_ ## p
  GET_REG(PIN); /* Expands to: GPIO_PIN, NOT GPIO_4! */
  ```
  Because `##` suppresses prescan, `PIN` is not expanded. The two-tier `CONCAT(GPIO_, PIN)` must be used.
- **Operator at Boundary:** Placing `##` as the first or last token in a replacement list is a compiler constraint violation.

## Embedded Implications
- **Pin Multiplexing & Port Abstraction:** Embedded architectures use token pasting to map abstract board functions (e.g., `STATUS_LED`) to concrete vendor register definitions (`GPIOB->ODR`).
- **Code Searchability Trade-off:** Synthesized identifiers cannot be located via simple text search tools (`grep`), complicating codebase navigation for new team members.

## Firmware Review Angle
- Ensure all token pasting uses the two-tier indirection (`CONCAT(a, b)`).
- Verify that every synthesized token forms a valid, standardized identifier conforming to project naming rules.
- Balance macro generation against code searchability: document synthesized symbol names clearly.

## Compiler, ABI, and Toolchain Implications
- Token pasting occurs purely in the front-end lexical analyzer; generated identifiers enter the compiler's symbol table identically to hand-written symbols.

## Performance, Memory, Timing, and Power
- Absolute zero runtime or memory overhead.

## Verification / Debugging
- Use `gcc -E` to inspect generated identifiers.
- Ensure static analysis tools have macro expansion enabled so synthesized symbols can be checked for type correctness.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 20.10: The `#` and `##` preprocessor operators should not be used. (Deviations required for register generation and templated structures).

## Trade-offs and Alternatives
- **Token Pasting vs Explicit Declarations:** Token pasting drastically reduces code duplication across repetitive peripheral channels, but impairs `grep`-ability and IDE symbol indexing.

## Staff-Level Takeaway
Token pasting is C's macro metaprogramming tool. Always wrap it in two-tier indirection (`CONCAT(a, b)`), verify that synthesized tokens produce valid identifiers, and document generated names thoroughly so developers can navigate the codebase effectively.

## Related Concepts
- `02_Function_like_macros`
- `08_Stringification_macros`
- `19_C_Preprocessor/05_Token_pasting`
