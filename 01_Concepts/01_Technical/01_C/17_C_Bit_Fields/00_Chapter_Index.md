# Bit-fields and Packed Representations

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Bit_field_declaration|Bit-field declaration]]
- [[02_Bit_field_widths|Bit-field widths]]
- [[03_Allocation_order|Allocation order]]
- [[04_Signed_bit_fields|Signed bit-fields]]
- [[05_Implementation_defined_layout|Implementation-defined layout]]
- [[06_Packed_structs|Packed structs]]
- [[07_Protocol_fields|Protocol fields]]
- [[08_MMIO_bit_fields|MMIO bit-fields]]
- [[09_Mask_and_shift_alternatives|Mask-and-shift alternatives]]
- [[10_Atomicity_limitations|Atomicity limitations]]
- [[11_ABI_hazards|ABI hazards]]
- [[12_Safe_bit_field_policy|Safe bit-field policy]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
