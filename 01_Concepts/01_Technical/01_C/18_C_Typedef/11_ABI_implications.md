# 11: ABI Implications

## Definition
ABI (Application Binary Interface) implications examine how the compiler treats `typedef` specifiers when generating object code, resolving calling conventions, populating debug symbol tables, and enforcing binary compatibility across translation units and shared libraries.

## Scope and Boundaries
Covers: Binary type equivalence, parameter passing registers, DWARF debug metadata, name mangling (or lack thereof in C), and binary backward compatibility.
Does not cover: High-level language FFI (Foreign Function Interfaces) or C++ ABI specifics.

## Why Does It Exist
Systems engineers often wonder if changing a `typedef` alters the ABI, breaks calling conventions, or creates binary incompatibilities with precompiled libraries. Understanding ABI mechanics ensures safe library refactoring and robust binary boundaries.

## Mechanism and Language Rules
1. **Type Invariance:** A `typedef` is completely transparent to the ABI. The compiler translates the alias to its fundamental underlying type before applying ABI lowering rules.
2. **Calling Conventions (AAPCS / System V):** Whether a parameter is declared as `uint32_t`, `reg32_t`, or `unsigned int`, it is passed in the exact same physical register (e.g., `R0` on ARM, `RDI` on x86_64).
3. **DWARF Debug Information:** While the ABI ignores typedefs, debug metadata formats (DWARF) explicitly record typedef entries (`DW_TAG_typedef`) pointing to base types, enabling debuggers to show domain-specific names.
4. **No Name Mangling in C:** Because C does not mangle function names with parameter types, changing a function signature from `void send(uint32_t val)` to `void send(my_alias_t val)` results in the exact same exported symbol `send`.

## Examples
```c
#include <stdint.h>
#include <assert.h>

/* Translation Unit A */
typedef uint32_t handle_t;
void process_data(handle_t h);

/* Translation Unit B */
typedef unsigned int raw_handle_t;
void process_data(raw_handle_t h);

/* 
 * Binary Analysis:
 * Both compilation units emit the identical symbol:
 * .global process_data
 * Under ARM AAPCS, 'h' is expected in register R0 in both cases.
 * The linker resolves them interchangeably without warning or conflict.
 */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Changing the *underlying type* of a typedef in a public header (e.g., changing `typedef uint32_t timestamp_t` to `typedef uint64_t timestamp_t`) without recompiling all dependent modules breaks the ABI silently, resulting in corrupted register states and stack offsets at runtime.

## Edge Cases and Failure Modes
- **Silent ABI Drift:** Modifying an underlying typedef in an SDK header breaks precompiled binary blobs linked into the firmware, causing heisenbugs where caller and callee disagree on parameter registers.
- **Debug Symbol Redundancy:** Heavy, circular typedef nesting produces deeply nested `DW_TAG_typedef` chains in ELF debug sections, inflating `.debug_info` sizes in large firmware builds.

## Embedded Implications
- **Dynamic Module Linking:** Bare-metal modular systems loading position-independent code (PIC) or ELF binaries into RAM rely on strict ABI matching across shared typedefs.

## Firmware Review Angle
- When refactoring typedefs in public headers, verify whether the change alters the underlying size or alignment. If size/alignment changes, a full rebuild of all dependent modules is mandatory.
- Lock critical ABI typedef sizes with compile-time assertions:
  `static_assert(sizeof(system_event_t) == 8, "ABI Breaking Change Detected");`.

## Compiler, ABI, and Toolchain Implications
- Compilers evaluate type compatibility at the AST level. Typedef identity is erased during intermediate representation (IR) lowering (e.g., in LLVM IR or GCC GIMPLE).

## Performance, Memory, Timing, and Power
- Zero impact on runtime binary performance or memory footprint.

## Verification / Debugging
- Use `readelf --debug-dump=info` to inspect `DW_TAG_typedef` DIEs (Debugging Information Entries).
- Use `abi-compliance-checker` or `libabigail` to verify that typedef changes do not break binary compatibility between firmware releases.

## Safety, Security, and Reliability
- ABI mismatches between statically linked vendor libraries and user code represent critical safety risks that static analysis cannot always catch.

## Trade-offs and Alternatives
- **Typedef Aliasing vs Versioned Wrapper Functions:** When an underlying type must change size, introduce a new versioned function (`process_data_v2`) rather than silently altering the typedef in-place.

## Staff-Level Takeaway
Typedefs are invisible to the linker and machine ABI—they are purely front-end compiler constructs. However, changing the *underlying* type of a typedef alters storage, alignment, and register-passing conventions. Lock critical API typedefs with static size assertions to safeguard your binary contracts.

## Related Concepts
- `01_Basic_typedefs`
- `03_Opaque_typedefs`
- `../16_C_Struct_Union_Enum/11_Enum_portability`
