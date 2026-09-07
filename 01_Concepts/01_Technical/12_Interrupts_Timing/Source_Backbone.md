# Source Backbone

Primary references:

- Arm Cortex-M Technical Reference Manuals: exception handling, NVIC, priority, stacking, tail-chaining and late arrival.
  https://developer.arm.com/documentation/100166/latest
- Linux kernel generic IRQ documentation: irq_desc, IRQ flow handlers, request_irq(), request_threaded_irq(), affinity and IRQ synchronization.
  https://docs.kernel.org/core-api/genericirq.html
- Zephyr documentation: ISR execution model, kernel clocks, system timer drivers and timers.
  https://docs.zephyrproject.org/latest/kernel/services/interrupts.html
  https://docs.zephyrproject.org/latest/kernel/services/timing/clocks.html
  https://docs.zephyrproject.org/latest/kernel/services/timing/timers.html
- FreeRTOS documentation: interrupt-safe APIs, scheduler interaction and software timers.
  https://www.freertos.org/

Notes are original explanatory material; exact guarantees and API legality remain target-specific.
