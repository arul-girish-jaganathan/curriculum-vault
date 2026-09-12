# 02: Private Headers

## Definition
A private header (`_priv.h`, `_internal.h`) is an interface file internal to a specific subsystem or driver. It shares internal structures, register layouts, and utility function prototypes between multiple translation units that comprise a single module, while strictly forbidding inclusion by external clients.

## Scope and Boundaries
Covers: Subsystem-internal declarations, shared private structs, hardware register overlays, and translation unit firewalls.
Does not cover: Public client APIs (see `01_Public_headers`) or single-file private `static` functions.

## Why Does It Exist
Complex embedded drivers (such as a complete USB stack or BLE controller) are too large for a single `.c` file. Splitting the driver across multiple translation units requires sharing internal function signatures and complete struct layouts without exposing them in public API headers.

## Mechanism and Language Rules
1. **Directory Isolation:** Stored in source directories (`src/`) rather than public include paths (`include/`).
2. **Completing Opaque Types:** Private headers define the concrete body of structs declared opaquely in public headers.
3. **Internal Linkage Symbols:** Declares functions that have `extern` linkage across module translation units, but must never be called by outside code.

## Examples
```c
/* hal_uart_priv.h - Private Driver Header */
#ifndef HAL_UART_PRIV_H
#define HAL_UART_PRIV_H

#include "hal_uart.h" /* Public interface */
#include <stdint.h>

/* Concrete definition of the opaque struct */
struct UartDevice {
    volatile uint32_t *base_reg;
    uint32_t           baud;
    uint32_t           rx_overflow_count;
    bool               is_initialized;
};

/* Internal driver functions shared across uart_tx.c and uart_rx.c */
void uart_hw_reset(struct UartDevice *dev);
void uart_irq_enable(struct UartDevice *dev);

#endif /* HAL_UART_PRIV_H */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Defining conflicting concrete bodies for the same struct tag across different private headers violates the One Definition Rule, invoking Undefined Behavior.

## Edge Cases and Failure Modes
- **Client Header Leakage:** An application developer notices a useful internal function in `hal_uart_priv.h` and includes it directly in `main.c`, violating module encapsulation and binding application logic to private driver internals.

## Embedded Implications
- **Silicon Revision Isolation:** Private headers allow hardware workarounds and errata registers to be isolated completely within driver source trees, preventing silicon bugs from polluting application logic.

## Firmware Review Angle
- Verify build system compiler include paths (`-I`): the directory containing private headers must NEVER be added to the include search path of client applications.
- Enforce naming conventions: name internal headers with explicit suffixes (`*_priv.h` or `*_internal.h`).

## Compiler, ABI, and Toolchain Implications
- Hiding concrete struct definitions in private headers means changing member variables requires recompiling only the module's `.c` files, leaving the rest of the firmware untouched.

## Performance, Memory, Timing, and Power
- Facilitates multi-file driver partitioning without incurring runtime indirection overhead within the module itself.

## Verification / Debugging
- CI check: Disallow inclusion of any `*_priv.h` file from files outside its designated subsystem directory.

## Safety, Security, and Reliability
- Enforces modular encapsulation mandated by functional safety standards (ISO 26262 Part 6, Architecture and Design Principles).

## Trade-offs and Alternatives
- **Private Header vs Single Monolithic `.c` File:** A monolithic `.c` file keeps everything truly `static` (zero visibility to anyone else), but becomes unmaintainable when drivers exceed 2,000 lines.

## Staff-Level Takeaway
Use private headers to share data structures and helper APIs across multi-file modules. Shield them behind build-system include path barriers so external applications cannot bypass public API encapsulation.

## Related Concepts
- `01_Public_headers`
- `06_Opaque_interfaces`
- `12_Embedded_module_boundaries`
