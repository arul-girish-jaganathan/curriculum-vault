# 01: Public Headers

## Definition
A public header is an interface specification file (`.h`) intentionally exposed to external subsystems, clients, or third-party integrators. It contains the minimal set of function prototypes, types, enumerations, and constants necessary to consume a module's capabilities without exposing internal data structures, register definitions, or implementation dependencies.

## Scope and Boundaries
Covers: Public API contracts, interface minimalism, header isolation, and binary compatibility surfaces.
Does not cover: Internal intra-module headers (see `02_Private_headers`) or compiler-specific intrinsics.

## Why Does It Exist
C enforces no language-level visibility access controls (e.g., `public`/`private`). Without strict conventions for public headers, implementation details leak into client code, tightly coupling consumers to internal driver layouts and forcing widespread rebuilds or runtime failures whenever internals change.

## Mechanism and Language Rules
1. **Minimal Surface Area:** Public headers declare only what callers must call or configure.
2. **No Storage Allocation:** Never define non-const variables or allocate memory in public headers.
3. **Pure Declarations:** Functions must be declared with prototypes (`ret_t func(param_t p);`).
4. **Exported Symbols:** All public functions implicitly have external linkage (`extern`).

## Examples
```c
/* hal_uart.h - Clean Public API Header */
#ifndef HAL_UART_H
#define HAL_UART_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

/* Opaque handle pattern hides silicon register structures */
typedef struct UartDevice* UartHandle;

typedef enum {
    UART_BAUD_9600   = 9600,
    UART_BAUD_115200 = 115200
} UartBaud_t;

typedef struct {
    UartBaud_t baud;
    bool       parity_enable;
} UartConfig_t;

UartHandle uart_init(uint8_t port_index, const UartConfig_t *config);
bool       uart_write(UartHandle handle, const uint8_t *data, size_t length);
void       uart_deinit(UartHandle handle);

#endif /* HAL_UART_H */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Including implementation-defined hardware types (e.g., vendor MMIO register maps) in public headers makes client compilation implementation-defined and non-portable.

## Edge Cases and Failure Modes
- **Leaking Hardware Headers:** `#include <stm32f4xx.h>` in a public header couples application business logic to specific chip silicon, making software emulation on desktop hosts impossible.
- **Accidental Static Function Inlining:** Placing non-trivial `static inline` functions in public headers bloats client translation units and exposes implementation algorithms.

## Embedded Implications
- **Host Testing & Emulation:** Keeping public headers hardware-agnostic allows application code to be compiled against mock driver libraries on x86 CI pipelines without cross-compilers or hardware.

## Firmware Review Angle
- Confirm the public header contains zero `#include` directives to vendor silicon SDKs or private driver internals.
- Verify that every public function parameter is properly `const`-qualified for read-only pointer inputs.

## Compiler, ABI, and Toolchain Implications
- Changes to public headers trigger rebuilds of all dependent translation units across the build system.

## Performance, Memory, Timing, and Power
- Opaque public headers eliminate compile-time inlining across modules (unless LTO is enabled), trading micro-optimizations for total architectural decoupling.

## Verification / Debugging
- Static analysis: Enforce that application layer `.c` files only include headers from the `include/public/` directory tree.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 8.5: An external object or function shall be declared once in one and only one file.

## Trade-offs and Alternatives
- Public headers sacrifice direct field access for long-term ABI stability and maintainability.

## Staff-Level Takeaway
A public header is an immutable contract. Keep it clean, minimal, and completely free of silicon-specific register layouts or private state structs. Use opaque handles to achieve absolute modular encapsulation.

## Related Concepts
- `02_Private_headers`
- `06_Opaque_interfaces`
- `07_Header_self_sufficiency`
