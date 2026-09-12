# 09: Readable API Typedefs

## Definition
Readable API typedefs are domain-driven type aliases established to express business logic, engineering units, or subsystem responsibilities directly within function signatures and data contracts. They communicate semantic intent and reduce developer cognitive load without introducing runtime overhead.

## Scope and Boundaries
Covers: Semantic aliasing, domain modeling (time, error, physical units), API usability, and cognitive load reduction.
Does not cover: Strong type enforcement systems or compiler-checked unit dimensions.

## Why Does It Exist
A function declared as `int update(int a, int b, int c);` conveys zero intent. Does it take coordinates? Timeouts? Error codes? Rewriting it with semantic typedefs:
`status_t update(device_id_t dev, timeout_ms_t timeout, retry_count_t retries);`
makes the API self-documenting and significantly reduces human error during integration.

## Mechanism and Language Rules
1. **Semantic Layering:** Aliases map basic fixed-width types to real-world domain concepts.
2. **Zero Runtime Cost:** Because ISO C resolves typedefs at compile-time, semantic layering introduces zero instruction, memory, or cycle penalties.
3. **Interchangeability Warning:** Remember that semantic typedefs sharing the same base type are interchangeable to the compiler. Readability is an engineering documentation aid, not a type-checker guarantee.

## Examples
```c
#include <stdint.h>
#include <stdbool.h>

/* Architectural Domain Typedefs */
typedef uint32_t system_tick_t;
typedef uint16_t millivolts_t;
typedef int16_t  celsius_centi_t; /* Temperature in 0.01 °C steps */

typedef enum {
    STATUS_OK = 0,
    STATUS_ERROR_TIMEOUT,
    STATUS_ERROR_BUSY,
    STATUS_ERROR_INVALID_PARAM
} status_t;

/* Highly readable, self-documenting API contract */
status_t battery_read_telemetry(millivolts_t     *out_voltage,
                                celsius_centi_t *out_temp,
                                system_tick_t    timeout_ticks);

static void test_call(void) {
    millivolts_t v;
    celsius_centi_t temp;
    
    /* Clear semantics at the call-site */
    status_t res = battery_read_telemetry(&v, &temp, 1000u);
    if (res == STATUS_OK) {
        // ... process telemetry ...
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- No undefined behavior; semantic typedefs adhere strictly to the rules of their underlying base types.

## Edge Cases and Failure Modes
- **False Sense of Security:** Developers may assume the compiler will catch swapping two arguments of the same underlying type (e.g., passing `timeout_ticks` where `out_voltage` was expected).
- **Over-Typedefing Bloat:** Creating a typedef for every single variable in a system creates visual clutter and mental fatigue (e.g., `typedef int counter_t; typedef int loop_index_t;`).

## Embedded Implications
- **Time Base Clarity:** One of the greatest sources of bugs in firmware is unit ambiguity (milliseconds vs. microseconds vs. RTOS clock ticks). Defining explicit typedefs (`timeout_ms_t` vs `tick_t`) prevents catastrophic timing miscalculations.

## Firmware Review Angle
- Ensure that time-related parameters always use explicit unit typedefs (`timeout_ms_t`, `timestamp_us_t`).
- Verify that status/error returns use an explicit `status_t` or `err_code_t` rather than raw `int`.

## Compiler, ABI, and Toolchain Implications
- Transparent to the ABI and code generator; optimizes completely down to primitive registers.

## Performance, Memory, Timing, and Power
- Absolute zero performance impact.

## Verification / Debugging
- Modern IDEs and language servers (Clangd, VS Code, CLion) display semantic typedef names in autocomplete tooltips, improving developer velocity and preventing API misuse.

## Safety, Security, and Reliability
- Reduces human error during cross-team module integration in mission-critical firmware.

## Trade-offs and Alternatives
- **Lightweight Typedef vs. Struct-Wrapped Unit:** Typedefs are lightweight and fast but lack compiler type-enforcement. Struct-wrapped units provide 100% compile-time enforcement at the cost of slight syntax verbosity.

## Staff-Level Takeaway
Use readable API typedefs to self-document interfaces and clarify engineering units—especially for time, error codes, and physical measurements. Balance semantic clarity with pragmatism: do not typedef every primitive scalar, but never leave ambiguous `int` parameters in public APIs.

## Related Concepts
- `01_Basic_typedefs`
- `03_Opaque_typedefs`
- `12_Naming_strategy`
