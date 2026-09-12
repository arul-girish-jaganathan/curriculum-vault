# 06: Opaque Interfaces

## Definition
An opaque interface is an API design pattern that exposes a pointer to an incomplete structure type (`struct Device*` or `typedef struct Device* DeviceHandle`) in public headers, while withholding the struct's member definitions inside private driver files. Clients can pass and store the handle, but cannot inspect, size, or dereference it.

## Scope and Boundaries
Covers: Incomplete types, handle patterns, information hiding, compilation firewalls, and memory allocation strategies for opaque objects.
Does not cover: `void *` pointers (which strip type checking entirely).

## Why Does It Exist
Without opaque interfaces, client code dereferences driver internals directly (`dev->regs->CR1 |= 1`). If the hardware layout, buffer size, or RTOS mutex implementation changes, client code breaks and must be recompiled. Opaque interfaces provide true compile-time encapsulation in pure C.

## Mechanism and Language Rules
1. **Incomplete Type Declaration:** `typedef struct GpioPort* GpioHandle;` declares the tag `struct GpioPort` without specifying its size or fields.
2. **Prohibited Operations:** Clients cannot evaluate `sizeof(struct GpioPort)` or write `handle->pin`. Attempting to do so triggers a compile-time constraint violation.
3. **Type Safety:** Unlike `void *`, the compiler enforces strict type identity: a `TimerHandle` cannot be passed to a function expecting a `GpioHandle`.

## Examples
```c
/* ================= PUBLIC API: drv_gpio.h ================= */
#ifndef DRV_GPIO_H
#define DRV_GPIO_H

#include <stdint.h>
#include <stdbool.h>

/* Opaque pointer handle */
typedef struct GpioInstance* GpioHandle;

GpioHandle gpio_open(uint8_t pin_index);
void       gpio_write(GpioHandle handle, bool state);
void       gpio_close(GpioHandle handle);

#endif /* DRV_GPIO_H */

/* ================= PRIVATE IMPLEMENTATION: drv_gpio.c ===== */
#include "drv_gpio.h"
#include <stdlib.h>

struct GpioInstance {
    volatile uint32_t *port_reg;
    uint32_t           pin_mask;
    bool               current_state;
};

/* Statically allocated instance pool for bare-metal systems */
static struct GpioInstance s_gpio_pool[4];

GpioHandle gpio_open(uint8_t pin_index) {
    if (pin_index >= 4) return NULL;
    s_gpio_pool[pin_index].pin_mask = (1UL << pin_index);
    return &s_gpio_pool[pin_index];
}

void gpio_write(GpioHandle handle, bool state) {
    if (!handle) return;
    handle->current_state = state;
    /* Direct hardware mutation safely encapsulated inside driver */
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Dereferencing a NULL or dangling opaque handle is Undefined Behavior; driver functions must guard against invalid handles.

## Edge Cases and Failure Modes
- **Stack Allocation Prevention:** Clients cannot declare opaque objects on their stack (`struct GpioInstance my_gpio;` fails to compile). The driver must manage storage via static pools, arena allocators, or dynamic memory.

## Embedded Implications
- **Zero-Heap Compatibility:** Opaque handles do NOT require `malloc`. Drivers in safety-critical firmware allocate handle structs from pre-allocated static BSS arrays, returning pointers to pool entries.

## Firmware Review Angle
- Ensure that public APIs never expose internal hardware registers or private state structures; convert them to opaque handles.
- Reject public interfaces that use `void *` for handles; enforce incomplete struct pointer typedefs.

## Compiler, ABI, and Toolchain Implications
- Passing opaque handles is ABI-equivalent to passing standard pointers in CPU core registers (`R0` on ARM).

## Performance, Memory, Timing, and Power
- Incurs one pointer indirection per API call. Prevents cross-translation-unit inlining unless Link-Time Optimization (LTO) is enabled.

## Verification / Debugging
- In GDB: `print *handle` fails in client files without debug symbols from the driver TU, preventing unauthorized state dependencies.

## Safety, Security, and Reliability
- Complies with ISO 26262 modular encapsulation mandates. Precludes memory corruption of driver internal states by external tasks.

## Trade-offs and Alternatives
- **Opaque Handle vs Public Struct:** Opaque handles prevent stack allocation and inlining, but provide 100% encapsulation, zero header leakage, and ABI stability.

## Staff-Level Takeaway
Opaque handles are the gold standard for C architecture. They provide true information hiding without sacrificing type safety. Allocate them from static driver pools in embedded systems, and never let clients inspect internal driver fields.

## Related Concepts
- `01_Public_headers`
- `02_Private_headers`
- `../18_C_Typedef/03_Opaque_typedefs`
