# Endianness, Encoding and Serialization

## Chapter purpose
A deep-reference chapter in the C language knowledge base. Use it to understand the rule, reason about compiler and ABI effects, and apply it safely in embedded firmware.

## Topics
- [[01_Host_endianness|Host endianness]]
- [[02_Byte_order_conversion|Byte order conversion]]
- [[03_Integer_serialization|Integer serialization]]
- [[04_Structure_serialization_pitfalls|Structure serialization pitfalls]]
- [[05_Explicit_field_encoding|Explicit field encoding]]
- [[06_Bit_level_protocols|Bit-level protocols]]
- [[07_Floating_serialization|Floating serialization]]
- [[08_Unaligned_access|Unaligned access]]
- [[09_Versioned_wire_formats|Versioned wire formats]]
- [[10_Checksums_and_framing|Checksums and framing]]
- [[11_DMA_descriptors|DMA descriptors]]
- [[12_Portable_serialization_helpers|Portable serialization helpers]]

## Review prompts
- What is guaranteed by ISO C?
- What depends on the implementation, ABI, compiler, libc, or target?
- What failure mode would appear on an embedded system?
- What test or inspection would prove the behavior?
