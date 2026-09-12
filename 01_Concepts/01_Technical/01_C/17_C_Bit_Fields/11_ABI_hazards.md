# 11: ABI Hazards

## Definition
ABI (Application Binary Interface) hazards represent binary incompatibilities that emerge when object files, precompiled third-party libraries, or disparate toolchains disagree on the size, alignment, container width, or parameter-passing conventions of structures containing bit fields.

## Scope and Boundaries
Covers: ARM AAPCS rules for bit fields, compiler flag mismatches (`-fshort-enums`, `-mstructure-size-boundary`), cross-compiler library linking, and register-passing conventions.
Does not cover: High-level language bindings (e.g., C to Python FFI).

## Why Does It Exist
C standards deliberately do not specify the ABI. Microprocessor vendors and software consortiums define ABIs (e.g., ARM AAPCS, System V AMD64), but toolchains frequently introduce proprietary command-line switches or default configuration variations that alter how bit fields are laid out in memory.

## Mechanism and Language Rules
1. **Container Alignment:** Under ARM AAPCS, a bit-field container has the alignment of its declared type. A struct with `uint32_t a : 1;` has 4-byte alignment, while `uint8_t a : 1;` has 1-byte alignment.
2. **Container Overlap:** Some compilers allow bit fields of different types (e.g., `uint8_t` followed by `uint16_t`) to share a single storage container, while others force alignment to the larger type's boundary.
3. **Parameter Passing Conventions:** Small structs are passed in CPU core registers (e.g., `R0-R3` on ARM). If two compilers disagree on whether a bit-field struct is 4 bytes or 8 bytes, registers are improperly assigned during function calls.

## Examples
```c
#include <stdint.h>
#include <assert.h>

/* ABI Hazard Example across different compilers */
struct DeviceStatus {
    uint8_t  flag_a : 4;
    uint32_t flag_b : 20; /* Mixed types: triggers ABI layout divergence */
};

/* 
 * Toolchain A (GCC with standard AAPCS):
 *   Aligns struct to 4 bytes. flag_b starts at bit 4 of Word 0.
 *   sizeof = 4 bytes.
 * 
 * Toolchain B (Strict legacy compiler):
 *   flag_a allocated in 8-bit container at offset 0.
 *   3 padding bytes inserted.
 *   flag_b allocated in 32-bit container at offset 4.
 *   sizeof = 8 bytes.
 */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Linking two object files compiled with incompatible bit-field alignment flags does not trigger linker errors; it fails silently at runtime through memory corruption.

## Edge Cases and Failure Modes
- **Vendor SDK Linking:** Linking your firmware application compiled with GCC against a closed-source binary blob (e.g., a Bluetooth Low Energy or WiFi stack) compiled with IAR or Keil ARMCC can corrupt shared status structures if bit-field layouts diverge.
- **Structure-Size Boundary Flags:** Compiling with flags like `-mstructure-size-boundary=8` versus `-mstructure-size-boundary=32` alters structure padding across the entire codebase.

## Embedded Implications
- **RTOS Context Passing:** Passing a bit-field struct to an RTOS task parameter (`void *pvParameters`) will result in invalid data reading if the task handler expects a different layout than the caller.

## Firmware Review Angle
- Audit all shared header files that define public API interfaces: bit fields must never appear in public header structs exposed to external libraries or users.
- Verify that compiler optimization and ABI flags are identical across all translation units in the build system (e.g., CMake / Makefile).

## Compiler, ABI, and Toolchain Implications
- ARM AAPCS §7.1.7 specifically defines the "Containerized Bit-Field Allocation Algorithm." Diverging from AAPCS breaks inter-toolchain compatibility.
- GCC option `-fpack-struct` globally packs all structures, breaking compatibility with standard C libraries.

## Performance, Memory, Timing, and Power
- ABI mismatches lead to catastrophic failures rather than performance degradation; debugging them consumes significant engineering hours.

## Verification / Debugging
- Use `_Static_assert(sizeof(struct S) == EXPECTED_SIZE)` and `_Static_assert(offsetof(...) == ...)` to protect any structure crossing ABI boundaries.
- Inspect symbol tables and object file layouts with `objdump -g` or `readelf -w`.

## Safety, Security, and Reliability
- Silent parameter misinterpretation caused by ABI layout divergence can bypass security checks, allow memory out-of-bounds writes, and violate safety standards.

## Trade-offs and Alternatives
- **Bit Fields vs. Fixed-Width Scalars:** Using standard types (`uint32_t`, `uint8_t`) in public interfaces guarantees 100% stable ABI layouts across all standard-compliant toolchains.

## Staff-Level Takeaway
Never expose bit fields across ABI boundaries or in public library interfaces. Restrict bit fields entirely to internal private translation units (`.c` files) where the compiler, flags, and target architecture are strictly homogeneous.

## Related Concepts
- `01_Bit_field_declaration`
- `05_Implementation_defined_layout`
- `12_Safe_bit_field_policy`
