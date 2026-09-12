# 03: Opaque Typedefs

## Definition
An opaque typedef (also known as an incomplete type typedef or handle pattern) defines a type alias for a pointer to an incomplete structure type whose definition is hidden inside a private source file (`.c`). External callers can allocate, store, and pass the handle, but cannot dereference it or inspect its internal members.

## Scope and Boundaries
Covers: Incomplete structure pointers, handle patterns, compilation firewalls (Pimpl in C), encapsulation boundaries, and lifetime management.
Does not cover: Generic `void *` handles (which discard type safety entirely).

## Why Does It Exist
C does not have access specifiers (`public`, `private`, `protected`). Opaque typedefs provide true compile-time encapsulation and information hiding. They protect internal module state from unauthorized client mutation, decouple public APIs from internal driver memory layouts, and eliminate rebuild cascades when private structures change.

## Mechanism and Language Rules
1. **Incomplete Type Declaration:** Declaring `typedef struct DeviceInstance *DeviceHandle;` in a header declares `struct DeviceInstance` as an incomplete type.
2. **Dereference Prohibition:** Because the structure's size and members are unknown to translation units that only include the public header, any attempt to dereference `handle->member` or evaluate `sizeof(*handle)` triggers a compile-time constraint violation.
3. **Type Safety over `void *`:** Unlike `void *`, an opaque pointer maintains full compiler type checking. A `TimerHandle` cannot be accidentally passed to an API expecting a `UartHandle`.
4. **Concrete Definition:** The private `.c` implementation file defines the complete struct: `struct DeviceInstance { ... };`.

## Examples
```c
/* ================= File: uart_driver.h (Public API) ================= */
#ifndef UART_DRIVER_H
#define UART_DRIVER_H

#include <stdint.h>
#include <stdbool.h>

/* Opaque Handle declaration: Type-safe compile-time encapsulation */
typedef struct UartDevice *UartHandle;

UartHandle uart_init(uint32_t base_addr, uint32_t baud_rate);
bool uart_transmit(UartHandle handle, const uint8_t *data, uint16_t len);
void uart_deinit(UartHandle handle);

#endif

/* ================= File: uart_driver.c (Private Implementation) ===== */
#include "uart_driver.h"
#include <stdlib.h>

struct UartDevice {
    volatile uint32_t *base_reg;
    uint32_t baud;
    uint32_t tx_errors;
    bool     is_busy;
};

UartHandle uart_init(uint32_t base_addr, uint32_t baud_rate) {
    static struct UartDevice dev_instance; /* Static allocation for bare-metal */
    dev_instance.base_reg = (volatile uint32_t *)base_addr;
    dev_instance.baud = baud_rate;
    return &dev_instance;
}

bool uart_transmit(UartHandle handle, const uint8_t *data, uint16_t len) {
    if (!handle || !data) return false;
    /* Full access to private members inside this compilation unit */
    handle->is_busy = true;
    // ... hardware transmission ...
    handle->is_busy = false;
    return true;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Dangling Handles:** Dereferencing an opaque handle after the underlying instance has been destroyed/de-initialized is Undefined Behavior.

## Edge Cases and Failure Modes
- **Stack Allocation Limitation:** Clients cannot allocate opaque structures on their own stack or statically in BSS because `sizeof(struct UartDevice)` is unknown. Allocation must be handled by the driver (via static pools, arenas, or heap).
- **Pointer-to-Pointer Confusion:** APIs returning newly created handles often require `handle_create(UartHandle *out_handle)`, leading to triple-pointer complexity if pointer typedefs are misused.

## Embedded Implications
- **ABI Stability:** Adding a field to `struct UartDevice` inside `uart_driver.c` does NOT require recompiling external client modules. This is critical for ROM bootloaders, shared libraries, and modular firmware frameworks.
- **Zero Heap Requirement:** Opaque handles do not require dynamic memory (`malloc`). Drivers can allocate instances from internal statically allocated pools while still returning opaque handles.

## Firmware Review Angle
- Confirm that drivers exposing public handles use opaque struct pointers rather than raw `void *`.
- Check that client code never attempts to bypass opaque boundaries by casting handles back to ad-hoc structs.

## Compiler, ABI, and Toolchain Implications
- Passing an opaque handle is ABI-equivalent to passing a standard scalar pointer (e.g., in register `R0` on ARM).

## Performance, Memory, Timing, and Power
- Accessing members inside the driver involves a single pointer indirection.
- Prevents cross-module inlining unless Link-Time Optimization (LTO) is enabled.

## Verification / Debugging
- Debuggers cannot inspect opaque handle members in client stack frames unless debug symbols from the implementation `.c` file are loaded.

## Safety, Security, and Reliability
- Strongly aligns with encapsulation mandates in ISO 26262 and DO-178C. Precludes clients from directly corrupting hardware registers or driver state flags.

## Trade-offs and Alternatives
- **Opaque Pointers vs. Public Structs:** Opaque pointers provide 100% encapsulation and ABI stability, but forfeit caller stack allocation and compiler inlining.

## Staff-Level Takeaway
Opaque typedefs represent the premier architectural abstraction pattern in C. Use them across module boundaries to enforce information hiding and maintain type safety, while rejecting `void *` handles which compromise the compiler's type checking.

## Related Concepts
- `02_Struct_typedefs`
- `05_Pointer_typedefs`
- `../16_C_Struct_Union_Enum/05_Pointer_to_structure`
