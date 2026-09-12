# 17: C Bit Fields — Chapter Index

## Definition
Bit fields are members of a structure or union declared with an explicit bit-width specifier. They instruct the compiler to pack multiple variables into discrete sub-byte bit allocations within underlying integer storage units. In embedded systems and low-level firmware engineering, bit fields represent a double-edged sword: offering syntactically concise sub-byte flag packing while introducing severe non-portability, concurrency races, and ABI alignment hazards.

## Scope and Boundaries
Covers: Bit-field declarations, width rules, zero-length padding fields, allocation/endianness order, signed/unsigned trap representations, implementation-defined layouts, packed attributes, protocol serialization risks, MMIO peripheral hazards, mask-and-shift patterns, non-atomic memory access, toolchain ABI boundaries, and safety-critical coding policies (MISRA C).
Does not cover: Standard full-word bitwise operators outside the context of struct members, software bit-arrays/bitmaps, or C++ bitset abstractions.

## Topics in This Chapter
1. `01_Bit_field_declaration.md`: Basic syntax, standard types (`_Bool`, `signed int`, `unsigned int`), unnamed fields, and alignment units.
2. `02_Bit_field_widths.md`: Width limits, storage boundaries, zero-width bit fields for alignment forcing, and truncation rules.
3. `03_Allocation_order.md`: Endianness vs. bitfield allocation order (LSB-to-MSB vs. MSB-to-LSB), and target ABI divergence.
4. `04_Signed_bit_fields.md`: Two's complement representation, the 1-bit signed bit-field trap (`-1` vs `1`), and sign-extension hazards.
5. `05_Implementation_defined_layout.md`: Standard ambiguities, boundary crossing rules, padding behavior, and compiler variations.
6. `06_Packed_structs.md`: Combining bit fields with `__attribute__((packed))` or `#pragma pack`, bus alignment faults, and code bloat.
7. `07_Protocol_fields.md`: Network headers, telemetry frames, cross-endian deserialization failures, and why bit fields fail wire protocols.
8. `08_MMIO_bit_fields.md`: Hardware registers, read-modify-write hazards, unintended side-effect writes, clear-on-read bits, and `-fstrict-volatile-bitfields`.
9. `09_Mask_and_shift_alternatives.md`: Type-safe macros, inline functions, bit manipulation idioms, and deterministic byte-exact register access.
10. `10_Atomicity_limitations.md`: Concurrent multi-threaded or ISR access to adjacent bit fields, cache-line and bus-word data races, and lock-free failures.
11. `11_ABI_hazards.md`: ARM AAPCS bit-field rules, GCC vs. Clang vs. IAR differences, and cross-compilation linkage breaks.
12. `12_Safe_bit_field_policy.md`: MISRA C:2012 guidelines (Rules 6.1, 6.2), defense-in-depth architectural rules, static assertions, and review checklists.

## Staff-Level Takeaway
Bit fields provide syntactic sugar for sub-byte memory packing at the expense of deterministic hardware and ABI contracts. In high-reliability firmware, bit fields are acceptable only for internal, single-threaded, RAM-constrained flag structures. They are strictly disqualified from memory-mapped hardware peripheral registers (MMIO), concurrency boundaries, and over-the-wire communication protocols.

## Related Concepts
- `../16_C_Struct_Union_Enum/01_Structure_layout`
- `../16_C_Struct_Union_Enum/02_Structure_members`
- `../16_C_Struct_Union_Enum/12_Protocol_and_register_layouts`
- `../00_Complete_Topic_Map`
