# 11: Enum Portability

## Definition
Enum portability addresses the architectural, ABI, and cross-compiler inconsistencies arising from how different C toolchains choose the underlying integer storage type and signedness for enumeration types.

## Scope and Boundaries
Covers: Enum sizing rules, `-fshort-enums` ABI divergence, signed vs unsigned underlying types, wire serialization, and fixed-width enum emulation.
Does not cover: C++11 explicit underlying enum types (`enum Foo : uint8_t`).

## Why Does It Exist
The ISO C standard gives compilers latitude in determining the underlying integer type of an `enum`. A compiler may choose `char`, `short`, `int`, or an unsigned variant depending on the value range and optimization flags. This flexibility creates severe cross-compiler and cross-module ABI incompatibilities.

## Mechanism and Language Rules
1. **Implementation-Defined Size:** ISO C specifies that the underlying type of an enumeration is an implementation-defined integer type capable of holding all defined values.
2. **Standard ABI Default:** Most ABIs (including ARM AAPCS and System V) mandate that by default, `sizeof(enum)` is equal to `sizeof(int)` (typically 4 bytes).
3. **Packing Flags:** GCC/Clang provide `-fshort-enums`, forcing the compiler to allocate only the minimum number of bytes needed (1 byte for values <= 255).
4. **Signedness Invariance:** If all constants are positive, the underlying type may be signed or unsigned depending on the compiler.

## Examples
```c
#include <stdint.h>
#include <assert.h>

/* Fragile: Size depends on compiler flags (-fshort-enums) */
typedef enum {
    PORT_A = 0,
    PORT_B = 1
} FragilePort;

/* Portable Fixed-Width Pattern for Wire/Storage Protocols */
typedef uint8_t HardwarePort_t;
enum {
    HARDWARE_PORT_A = 0x00u,
    HARDWARE_PORT_B = 0x01u,
    HARDWARE_PORT_MAX = 0xFFu
};

/* Struct using portable fixed-width type */
struct DeviceConfig {
    HardwarePort_t port; /* Strictly 1 byte across all compilers */
    uint8_t        rate;
};

static_assert(sizeof(struct DeviceConfig) == 2, "Config size broken by padding or enum size");
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **ABI Incompatibility:** Linking an object file compiled with `-fshort-enums` against a library compiled without `-fshort-enums` results in catastrophic ABI incompatibility: function parameters and struct offsets mismatch silently at runtime.
- **Signedness Differences:** Printing or shifting an enum whose underlying signedness varies across compilers can introduce unexpected sign-extension bugs.

## Edge Cases and Failure Modes
- **Protocol Deserialization Failure:** Embedding an `enum` inside a packed communication struct shared across an ARM Cortex-M (-fshort-enums) and an x86 server (standard 4-byte enum) causes complete deserialization corruption.
- **Bitwise Shifting Signed Enums:** If the compiler assigns a signed underlying type to an enum, bitwise left shifts on negative or large enum values trigger Undefined Behavior.

## Embedded Implications
- **Memory Footprint vs ABI Stability:** `-fshort-enums` saves significant RAM in large tables on microcontrollers, but breaks compatibility with precompiled commercial libraries (e.g., RTOS, CMSIS, protocol stacks) compiled with standard ABI.
- **Serialization Protocols:** Enums must never appear in raw memory-mapped protocol packets.

## Firmware Review Angle
- Verify that every struct shared across cores, networks, or non-volatile storage uses explicit fixed-width integer types (`uint8_t`, `uint16_t`, `uint32_t`) rather than raw `enum` types.
- Check project-wide compiler build scripts to ensure `-fshort-enums` is either strictly forbidden or universally enforced across all translation units.

## Compiler, ABI, and Toolchain Implications
- The ARM EABI specifies whether a toolchain defaults to short enums. GCC defaults to 32-bit enums unless `-fshort-enums` is passed.
- Keil ARMCC and IAR may use short enums by default in certain optimization profiles.

## Performance, Memory, Timing, and Power
- 32-bit enums match standard register widths on 32-bit CPUs, executing with zero masking overhead.
- 8-bit enums reduce RAM usage but may require extra byte-extension instructions (`UXTB`) when loaded into registers.

## Verification / Debugging
- Add static assertions in headers to lock enum sizes when ABI stability is mandatory:
  `_Static_assert(sizeof(FragilePort) == 4, "ABI mismatch: enum size changed");`

## Safety, Security, and Reliability
- MISRA C:2012 Rule 10.4: Both operands of an operator in an expression shall have the same essential type category.

## Trade-offs and Alternatives
- **Fixed-width Typedefs + Anonymous Enums:** Combines strict 1-byte storage guarantees with symbolic enumeration constants.

## Staff-Level Takeaway
Never use bare `enum` types in wire protocols, register overlays, or public library ABIs. For embedded structures, define fields using explicit fixed-width integers (`uint8_t`) and use anonymous enums solely to provide named value constants.

## Related Concepts
- `10_Enumerations`
- `12_Protocol_and_register_layouts`
