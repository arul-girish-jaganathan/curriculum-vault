# Embedded ABI review

> Canonical C topic note — chapter 36.

## Definition
An **embedded ABI review** is a deliberate verification that every binary boundary in a firmware system agrees on symbol identity, calling convention, type representation, object layout and execution assumptions. It connects C source contracts to the actual linked image.

## Mechanism and language rules
Start by inventorying boundaries:

1. application ↔ driver;
2. application ↔ bootloader;
3. C ↔ assembly;
4. C ↔ C++/Rust/other languages;
5. vendor libraries ↔ application;
6. secure ↔ non-secure or privilege-domain boundaries;
7. compiler-generated startup/runtime ↔ application.

For each boundary record function prototypes, data structures, alignment, ownership, calling convention, register preservation, symbol visibility, versioning and build options.

Compile-time checks are useful:

```c
_Static_assert(sizeof(packet_t) == 16, "ABI packet size changed");
_Static_assert(offsetof(packet_t, payload) == 4, "ABI payload offset changed");
```

But a complete ABI review also requires binary inspection.

## Embedded implications
ABI defects are often catastrophic because the linker may succeed while the CPU executes an incompatible contract. Symptoms can include corrupted stacks, wrong register values, sporadic faults, only-release failures, incorrect floating-point values, or failures that depend on optimization.

Review should cover:

- architecture and ISA selection;
- hard/soft floating-point mode;
- endianness and data representation;
- stack alignment;
- register preservation;
- structure packing/alignment;
- interrupt/exception entry conventions;
- linker script and section placement;
- startup/runtime assumptions;
- LTO and compiler optimization settings.

### Firmware review angle
Treat the **toolchain configuration** as part of the ABI. Pin compiler family/version where required, record flags, and prevent incompatible object files from entering the image. Keep a known-good ABI probe and build it in CI.

## Edge cases and failure modes
Do not limit review to function prototypes. A function can have the correct source declaration while the surrounding ABI is wrong. Examples include a structure whose packing differs between producer and consumer, a function compiled with a different floating-point convention, or assembly that fails to preserve a nonvolatile register.

Another subtle issue is version drift: a bootloader compiled months earlier may expect an old application header or structure layout. Source compatibility in the current tree does not validate the deployed binary relationship.

## Example pattern
```c
typedef struct {
    uint32_t version;
    uint32_t length;
    uint8_t payload[8];
} image_header_t;

_Static_assert(sizeof(image_header_t) == 16, "header ABI changed");
_Static_assert(offsetof(image_header_t, payload) == 8, "header ABI changed");
```

Pair these checks with an explicit version field and runtime validation at the image boundary.

## Verification / debugging
A practical ABI review uses four evidence layers:

1. **source** — prototypes, typedefs, qualifiers and contracts;
2. **compiler** — record layouts, warnings and generated assembly;
3. **linker** — symbol table, relocations, section placement and map;
4. **hardware** — register/stack inspection, fault capture and timing measurements.

When a fault occurs at a boundary, capture PC/LR, stack pointer, relevant argument/return registers and fault status. Compare them with the ABI specification before changing application logic.

## Staff-level takeaway
For embedded systems, ABI review is a **binary-contract audit**. A Staff engineer should be able to trace an interface from C declaration → compiler classification → object symbols → linker placement → CPU registers/stack → deployed image, and identify exactly where an assumption is guaranteed or merely toolchain-specific.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
