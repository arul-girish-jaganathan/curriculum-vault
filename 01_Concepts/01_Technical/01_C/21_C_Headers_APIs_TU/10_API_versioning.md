# 10: API Versioning

## Definition
API versioning is the engineering practice of managing changes, extensions, and deprecations in public interfaces over time without breaking backward source compatibility (API) or binary compatibility (ABI) for existing consumers.

## Scope and Boundaries
Covers: Semantic versioning macros, compiler deprecation attributes (`__attribute__((deprecated))`), ABI padding, and symbol migration wrappers.
Does not cover: Git branch management or package manager repositories.

## Why Does It Exist
Embedded systems in production cannot tolerate breaking changes. Bootloaders in ROM, external application modules, and communication protocols must maintain long-term compatibility across firmware updates without requiring simultaneous re-flashing of every subsystem.

## Mechanism and Language Rules
1. **Semantic Versioning Macros:** Headers expose compile-time version metadata:
   `#define MODULE_VERSION_MAJOR 2`.
2. **Deprecation Directives:** Compilers provide attributes to warn developers of obsolete functions without breaking the build:
   `__attribute__((deprecated("Use uart_write_v2() instead")))`.
3. **Reserved ABI Padding:** Public structures incorporate reserved padding arrays to allow future expansion without changing structure size or member offsets.

## Examples
```c
/* ================= File: drv_sensor.h ================= */
#ifndef DRV_SENSOR_H
#define DRV_SENSOR_H

#include <stdint.h>

#define SENSOR_API_VERSION_MAJOR 2
#define SENSOR_API_VERSION_MINOR 1

/* Struct with reserved ABI padding for future expansion */
typedef struct {
    uint16_t sample_rate_hz;
    uint8_t  filter_mode;
    uint8_t  _reserved1;      /* Preserves alignment */
    uint32_t _reserved2[3];   /* Expansion reserve: maintains sizeof across versions */
} SensorConfig_t;

/* Modern API function */
int32_t sensor_read_calibrated(int32_t *out_data);

/* Deprecated legacy function with compiler diagnostic notice */
#if defined(__GNUC__) || defined(__clang__)
    #define DEPRECATED(msg) __attribute__((deprecated(msg)))
#else
    #define DEPRECATED(msg)
#endif

DEPRECATED("sensor_read_raw() is deprecated; migrate to sensor_read_calibrated()")
int32_t sensor_read_raw(int16_t *out_data);

#endif /* DRV_SENSOR_H */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Altering the size or member offsets of a struct used by precompiled libraries without updating the library causes binary corruption (Undefined Behavior).

## Edge Cases and Failure Modes
- **Silent Struct Reordering:** Reordering struct members across API revisions preserves source syntax, but silently corrupts data when linked against precompiled object binaries.

## Embedded Implications
- **Bootloader to Application Contracts:** A bootloader calling application entry points must rely on a fixed ABI table (function pointer vectors) that remains stable across all future application releases.

## Firmware Review Angle
- Confirm that any breaking change to an existing public API increments the `MAJOR` version number.
- Verify that deprecated functions trigger compiler warnings and include migration guidance in their warning strings.

## Compiler, ABI, and Toolchain Implications
- Compiler attribute `__attribute__((deprecated))` emits compile-time diagnostics during Translation Phase 7 without generating extra machine code.

## Performance, Memory, Timing, and Power
- Reserving padding words in configuration structures costs a few bytes of RAM/Flash, but protects the architecture from future ABI breakage.

## Verification / Debugging
- Use `abi-compliance-checker` on compiled `.so` / `.a` libraries to detect unintended symbol signature changes between firmware releases.

## Safety, Security, and Reliability
- Controlled API versioning prevents silent parameter mismatches in safety-critical systems (IEC 61508 / ISO 26262).

## Trade-offs and Alternatives
- **Deprecation vs Immediate Removal:** Deprecation temporarily increases codebase size with backward-compatibility shims, but prevents abrupt build breaks across distributed teams.

## Staff-Level Takeaway
Never change an existing public API without a versioning strategy. Use deprecation attributes with actionable migration messages, reserve expansion padding in public structs to preserve ABI offsets, and communicate breaking updates through semantic version macros.

## Related Concepts
- `01_Public_headers`
- `06_Opaque_interfaces`
- `11_Linkage_hygiene`
