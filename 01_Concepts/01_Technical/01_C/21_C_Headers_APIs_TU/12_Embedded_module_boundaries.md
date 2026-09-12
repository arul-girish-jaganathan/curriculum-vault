# 12: Embedded Module Boundaries

## Definition
Embedded module boundaries are architectural encapsulation planes that isolate low-level physical silicon drivers (MMIO, registers, DMA, interrupts) from application business logic, state machines, and communication protocols. A robust boundary guarantees that silicon-specific details never bleed across the HAL (Hardware Abstraction Layer).

## Scope and Boundaries
Covers: Hardware Abstraction Layers (HAL), Board Support Packages (BSP), interrupt decoupling, mockability for host unit testing, and MISRA C interface compliance.
Does not cover: Operating system virtual device trees or Linux kernel VFS layers.

## Why Does It Exist
Microcontroller silicon vendors (ST, NXP, TI, Silicon Labs) provide vendor HALs that vary wildly in quality, API design, and portability. If application code calls vendor HAL APIs directly, porting the product to an alternative microcontroller (e.g., during supply chain silicon shortages) requires rewriting the entire codebase.

## Mechanism and Language Rules
1. **Three-Tier Architecture:**
   - **Application Layer:** Pure C business logic, zero hardware awareness.
   - **System HAL Layer:** Generic interface contracts (`hal_spi.h`, `hal_gpio.h`).
   - **Target BSP Driver:** Concrete implementation for specific silicon (`stm32_spi.c`, `nrf_spi.c`).
2. **Interrupt Decoupling:** Hardware Interrupt Service Routines (ISRs) live inside the BSP driver; they notify application layers via registered callbacks or RTOS message queues, never by calling application logic directly.

## Examples
```c
/* ================= ARCHITECTURAL BOUNDARY ================= */

/* 1. HAL Interface Contract (hal_timer.h) */
#ifndef HAL_TIMER_H
#define HAL_TIMER_H

#include <stdint.h>
typedef void (*TimerCallback_t)(void *context);

void hal_timer_init(uint32_t frequency_hz);
void hal_timer_register_cb(TimerCallback_t cb, void *ctx);

#endif /* HAL_TIMER_H */

/* 2. Concrete Silicon Driver (bsp_stm32_timer.c) */
#include "hal_timer.h"
#include <stm32f4xx.h> /* Vendor silicon header ISOLATED here */

static TimerCallback_t s_app_cb = NULL;
static void           *s_app_ctx = NULL;

void TIM2_IRQHandler(void) {
    if (TIM2->SR & TIM_SR_UIF) {
        TIM2->SR = ~TIM_SR_UIF; /* Clear hardware flag */
        if (s_app_cb) {
            s_app_cb(s_app_ctx); /* Notify across boundary */
        }
    }
}

void hal_timer_init(uint32_t frequency_hz) {
    /* Concrete register manipulation */
    RCC->APB1ENR |= RCC_APB1ENR_TIM2EN;
    // ... configure registers ...
}

void hal_timer_register_cb(TimerCallback_t cb, void *ctx) {
    s_app_cb = cb;
    s_app_ctx = ctx;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Allowing vendor CMSIS headers to leak into application files makes application code non-portable and undefined on standard host test simulators.

## Edge Cases and Failure Modes
- **Interrupt Context Leaks:** A driver callback executing inside an ISR calls an application function that attempts to acquire a blocking RTOS mutex, triggering an immediate RTOS crash or HardFault.

## Embedded Implications
- **Supply Chain Resilience:** When a chip becomes unavailable, a well-bounded architecture requires rewriting only the BSP `.c` files matching the HAL contracts, saving months of re-engineering.

## Firmware Review Angle
- Reject any application-layer file (`app_*.c`) that includes vendor chip headers (`stm32*.h`, `nrf*.h`).
- Ensure all ISR implementations reside strictly within the low-level BSP driver tier.

## Compiler, ABI, and Toolchain Implications
- Strict module boundaries enable compiling the application layer with standard desktop GCC/Clang on Linux/macOS for instantaneous native unit testing (e.g., Unity/CMock).

## Performance, Memory, Timing, and Power
- The HAL interface abstraction introduces a negligible 1-2 instruction overhead per hardware transaction, while yielding massive improvements in architectural maintainability.

## Verification / Debugging
- Automated CI pipeline rule: grep for vendor header strings across all application directories; fail the build if any are found.

## Safety, Security, and Reliability
- Complies with ISO 26262 Part 6 architectural modularity and safety segregation requirements.

## Trade-offs and Alternatives
- Thin wrapper HALs require upfront API design time, but pay massive dividends during testing, porting, and maintenance.

## Staff-Level Takeaway
Never let silicon vendor headers cross into your application code. Encapsulate hardware manipulation behind pure, portable HAL interface contracts. This guarantees hardware independence, enables host-based unit testing, and insulates your firmware from supply chain disruptions.

## Related Concepts
- `01_Public_headers`
- `02_Private_headers`
- `08_Dependency_direction`
- `11_Linkage_hygiene`
