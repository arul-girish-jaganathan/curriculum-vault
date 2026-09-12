# 12: Naming Strategy

## Definition
A typedef naming strategy is a systematic convention for naming type aliases across an engineering organization. It establishes clear visual distinction between types, objects, and macros, while navigating standardized language reservations such as POSIX `_t` namespace restrictions.

## Scope and Boundaries
Covers: Identifier conventions (`_t`, CamelCase, prefixing), POSIX namespace reservations, MISRA compliance, and cross-team interface consistency.
Does not cover: Formatting whitespace or brace placement.

## Why Does It Exist
Without strict naming guidelines, large embedded codebases devolve into conflicting styles: `uint32`, `u32`, `U32`, `UInt32`, and `uint32_t` appearing in the same file. Inconsistent naming causes namespace collisions, impairs readability, and can violate POSIX standards.

## Mechanism and Language Rules
1. **The POSIX `_t` Reservation:** IEEE Std 1003.1 (POSIX) officially reserves all identifiers ending in `_t` for future standard library expansion.
   * *Strict POSIX conformance:* User code should avoid creating new identifiers ending in `_t` if compiling for POSIX-compliant environments.
   * *Embedded Reality:* In bare-metal and RTOS firmware (FreeRTOS, CMSIS, Zephyr), `_t` is the near-universal convention for typedefs.
2. **Namespace Prefixing:** Module-level prefixing (e.g., `uart_handle_t`, `ble_conn_params_t`) prevents identifier collisions in C's unified global ordinary identifier namespace.
3. **Tag vs Alias Naming:** Maintaining parity between struct tags and their aliases:
   `typedef struct UartDriver UartDriver;` (CamelCase convention) or
   `typedef struct uart_driver_s uart_driver_t;` (Snake_case convention).

## Examples
```c
#include <stdint.h>
#include <stdbool.h>

/* Enterprise Embedded Naming Conventions */

/* 1. Snake_case with Module Prefix and _t (Standard Embedded / FreeRTOS style) */
typedef struct can_filter_config_s {
    uint32_t filter_id;
    uint32_t filter_mask;
    bool     is_extended;
} can_filter_config_t;

/* 2. PascalCase / CamelCase (CMSIS / MISRA friendly) */
typedef struct {
    uint32_t BaudRate;
    uint16_t Parity;
    uint8_t  StopBits;
} UART_ConfigTypeDef;

/* 3. POSIX-Safe Alternative for host tools */
typedef struct memory_pool_s memory_pool_type;
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Defining a type name ending in `_t` on a POSIX-compliant system technically risks colliding with a future system header definition, which results in compilation failure.

## Edge Cases and Failure Modes
- **Suffix Inconsistency:** Mixing `_t`, `_type`, and bare names leads developers to mistake types for variables:
  `status code;` vs `status_t code;`.
- **Clashing with Standard Headers:** Creating custom `bool_t`, `size_t`, or `int8_t` aliases collides with `<stdbool.h>` and `<stdint.h>`.

## Embedded Implications
- In resource-constrained teams working on bare-metal systems (ARM Cortex-M, RISC-V), following the CMSIS convention (`Module_TypeDef`) or the standard C99 snake_case convention (`module_type_t`) establishes consistency across millions of lines of code.

## Firmware Review Angle
- Enforce strict adherence to one naming standard across the repository:
  - Either all types use `_t` suffix, OR all types use `CamelCase`. Never mix both within the same layer.
- Ensure all public types include the module namespace prefix (e.g., `spi_*`, `crypto_*`).

## Compiler, ABI, and Toolchain Implications
- Naming conventions have no impact on generated assembly or ABI registers.

## Performance, Memory, Timing, and Power
- Zero runtime impact.

## Verification / Debugging
- Enforce naming conventions automatically in CI using `clang-tidy` (`readability-identifier-naming`).

## Safety, Security, and Reliability
- Clear naming prevents accidental type shadowing and reduces cognitive load during code audits.
- MISRA C:2012 Rule 5.6 mandates that all typedef names be globally unique identifiers.

## Trade-offs and Alternatives
- **`_t` Suffix vs POSIX Purity:** In pure Linux user-space code, use `_type` or CamelCase to strictly respect POSIX reservations. In embedded/bare-metal firmware, `_t` remains the accepted industry standard.

## Staff-Level Takeaway
Choose a naming convention and enforce it mechanically via linter scripts. For bare-metal firmware, prefix every public typedef with its module namespace and append `_t` or use PascalCase (`Uart_Config_t`). Never allow untagged, un-prefixed generic type names in public interfaces.

## Related Concepts
- `01_Basic_typedefs`
- `02_Struct_typedefs`
- `10_MISRA_oriented_typedef_usage`
