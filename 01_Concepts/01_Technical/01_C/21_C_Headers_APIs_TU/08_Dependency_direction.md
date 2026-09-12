# 08: Dependency Direction

## Definition
Dependency direction defines the architectural rule that source files and headers must only depend on modules at equal or lower levels of abstraction. The dependency graph of the entire software system must form a Directed Acyclic Graph (DAG), flowing strictly from high-level application logic downward through middleware, HAL, and physical drivers.

## Scope and Boundaries
Covers: Layered software architecture, DAG enforcement, abstraction boundaries, dependency inversion in C, and callback decoupling.
Does not cover: Runtime dynamic module loading.

## Why Does It Exist
Uncontrolled dependencies result in cyclic spaghetti architecture: a motor driver includes an application header to read a setpoint, while the application includes the motor driver to issue commands. This prevents isolated unit testing, breaks module reusability, and causes circular inclusion deadlock.

## Mechanism and Language Rules
1. **Strict Layering:** Layer $N$ may include headers from Layer $N-1$ or lower. Layer $N-1$ must NEVER include headers from Layer $N$.
2. **Dependency Inversion via Callbacks:** If a low-level driver must notify high-level code, it does so through function pointer callbacks registered at runtime, NOT by including high-level headers.
3. **No Upward Inclusions:** Low-level drivers must know nothing about the applications that consume them.

## Examples
```c
/* ================= VIOLATION: Low-level driver includes High-level app = */
/* drv_uart.c */
// #include "app_telemetry.h" /* FORBIDDEN: Upward dependency! */
// void uart_rx_isr(void) { app_telemetry_post_byte(rx); }

/* ================= COMPLIANT: Dependency Inversion via Callback ======= */
/* drv_uart.h (Low Level) */
#ifndef DRV_UART_H
#define DRV_UART_H

#include <stdint.h>

typedef void (*UartRxCallback_t)(uint8_t byte, void *context);

void uart_register_rx_callback(UartRxCallback_t cb, void *context);

#endif

/* app_telemetry.c (High Level) */
#include "drv_uart.h" /* Legal downward dependency */

static void on_uart_byte(uint8_t byte, void *context) {
    /* Process incoming telemetry byte */
}

void app_telemetry_init(void) {
    uart_register_rx_callback(on_uart_byte, NULL);
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Cyclic dependencies often lead to undefined symbol ordering and unresolvable linker circular references.

## Edge Cases and Failure Modes
- **Hidden Upward Dependencies via Macros:** A driver including a configuration header that references an application-specific enum creates a stealth upward dependency.

## Embedded Implications
- **Hardware Portability:** A clean downward dependency architecture allows replacing the target MCU's HAL without modifying a single line of application or protocol stack code.

## Firmware Review Angle
- Audit all `#include` directives in driver and HAL directories: ensure zero inclusions of application-layer headers (`app_*.h`).
- Enforce callback registration mechanisms for asynchronous events.

## Compiler, ABI, and Toolchain Implications
- Acyclic dependencies allow parallel compilation of independent modules across multi-core build systems without lock contention.

## Performance, Memory, Timing, and Power
- Function pointer callbacks introduce a single indirect branch instruction (`BLX R0`), costing 1-2 CPU cycles while delivering total architectural decoupling.

## Verification / Debugging
- Use dependency graphing tools (e.g., `graphviz`, `cinclude2dot`, or Clang tooling) to generate and audit the project DAG during CI builds.

## Safety, Security, and Reliability
- ISO 26262 Part 6 Section 7 mandates hierarchical layered architecture and highly decoupled software units for ASIL certification.

## Trade-offs and Alternatives
- **Callbacks vs Polling:** Callbacks enforce clean downward dependencies and event-driven responsiveness at the cost of indirect call overhead.

## Staff-Level Takeaway
Dependencies must flow in one direction: strictly downward. Drivers must never include application headers. Use dependency inversion via function pointer callbacks to pass asynchronous events upward across architectural layers.

## Related Concepts
- `01_Public_headers`
- `09_Circular_include_avoidance`
- `12_Embedded_module_boundaries`
