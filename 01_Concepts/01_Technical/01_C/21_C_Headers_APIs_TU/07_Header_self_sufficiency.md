# 07: Header Self-Sufficiency

## Definition
Header self-sufficiency is the architectural requirement that any header file must successfully compile on its own when included in an otherwise empty translation unit. A self-sufficient header explicitly includes all prerequisite headers (`<stdint.h>`, `<stdbool.h>`, external types) required for its own declarations.

## Scope and Boundaries
Covers: Standalone compilation verification, prerequisite inclusion discipline, and avoiding order-dependent includes.
Does not cover: Implementation `.c` file inclusion rules.

## Why Does It Exist
When a header depends on types declared in another header without including it, callers are forced to discover and maintain fragile inclusion chains:
`#include <stdint.h>` followed by `#include "foo.h"` followed by `#include "bar.h"`.
If the order is altered, compilation breaks with bizarre syntax errors.

## Mechanism and Language Rules
1. **Self-Sufficiency Principle:** If `header_a.h` uses `uint32_t`, `header_a.h` MUST explicitly include `<stdint.h>`.
2. **Order Independence:** Any client should be able to include headers in any arbitrary sequence without triggering errors.
3. **Idempotency Integration:** Combined with include guards, self-sufficient headers prevent duplicate declaration issues regardless of inclusion order.

## Examples
```c
/* ================= NON-COMPLIANT: Fragile Header ================= */
/* sensor_data.h */
#ifndef SENSOR_DATA_H
#define SENSOR_DATA_H

/* BUG: Uses uint32_t and bool without including stdint.h or stdbool.h! */
typedef struct {
    uint32_t timestamp; /* Unknown type if included alone! */
    bool     is_valid;  /* Unknown type if included alone! */
} SensorReading_t;

#endif

/* ================= COMPLIANT: Self-Sufficient Header ============= */
/* sensor_data.h */
#ifndef SENSOR_DATA_H
#define SENSOR_DATA_H

#include <stdint.h>  /* Explicit dependency */
#include <stdbool.h> /* Explicit dependency */

typedef struct {
    uint32_t timestamp;
    bool     is_valid;
} SensorReading_t;

#endif /* SENSOR_DATA_H */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Order-dependent headers lead to brittle, implementation-defined build failures depending on which system headers were transitively pulled in by earlier inclusions.

## Edge Cases and Failure Modes
- **Hidden Dependencies via PCH:** Using Precompiled Headers (PCH) masks missing include dependencies during development; builds fail immediately when compiled in clean CI environments without PCH.

## Embedded Implications
- In cross-platform firmware projects targeting multiple MCUs, order-dependent headers frequently break when switching between toolchains (e.g., GCC vs Keil ARMCC) due to differing system header transitive inclusions.

## Firmware Review Angle
- **The Compile-Alone Test:** Verify that every header passes compilation when compiled alone:
  `gcc -xc -c header.h -o /dev/null`.
- Reject any header that relies on the caller including prerequisite headers first.

## Compiler, ABI, and Toolchain Implications
- Self-sufficient headers trigger compiler MIOpt optimizations cleanly across all translation units.

## Performance, Memory, Timing, and Power
- Negligible impact on compilation time due to include guard caching; zero runtime or binary footprint impact.

## Verification / Debugging
- Automated CI test script:
  ```bash
  for header in $(find include/ -name "*.h"); do
      echo "#include "$header"" | gcc -xc -c -Iinclude - -o /dev/null || exit 1
  done
  ```

## Safety, Security, and Reliability
- Enhances codebase maintainability and eliminates fragile order-dependent compile breaks across safety-critical teams.

## Trade-offs and Alternatives
- Self-sufficiency requires slightly more `#include` lines per header, but entirely eliminates order-dependent build failures.

## Staff-Level Takeaway
Every header file must compile cleanly on its own in an empty translation unit. Automate the "compile-alone" test in your CI pipeline to guarantee that developers never push order-dependent headers.

## Related Concepts
- `01_Public_headers`
- `03_Include_guards`
- `08_Dependency_direction`
