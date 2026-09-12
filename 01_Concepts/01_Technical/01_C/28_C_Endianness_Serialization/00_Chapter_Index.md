# 28_C_Endianness_Serialization: Chapter Index

## Overview
C Endianness and Serialization covers the transmission, representation, and interpretation of multi-byte data across memory architectures and communication links. Because different CPU architectures (little-endian x86/ARM vs. big-endian network protocols and legacy processors) store bytes in divergent orders, robust systems software requires disciplined serialization techniques, byte-order conversion functions, unaligned access mitigation, and versioned wire formats.

## Chapter Directory
- [[01_Host_endianness]] — Little-endian vs. big-endian fundamentals and runtime detection
- [[02_Byte_order_conversion]] — `htons`, `htonl`, `ntohs`, `ntohl`, and standard byte-swapping utilities
- [[03_Integer_serialization]] — Portable multi-byte integer packing and unpacking via byte shifts
- [[04_Structure_serialization_pitfalls]] — Padding holes, alignment hazards, and raw struct dumping dangers
- [[05_Explicit_field_encoding]] — Field-by-field protocol encoding and explicit layout contracts
- [[06_Bit_level_protocols]] — Bitfields, bit-packing, and mask-based protocol extraction
- [[07_Floating_serialization]] — IEEE 754 float/double serialization across divergent representation formats
- [[08_Unaligned_access]] — Handling unaligned network buffers safely without hardware traps
- [[09_Versioned_wire_formats]] — Backward compatibility, forward evolution, and extensible protocol design
- [[10_Checksums_and_framing]] — Packet framing, CRC16/CRC32 checksums, and error detection
- [[11_DMA_descriptors]] — Hardware descriptor rings, scatter-gather lists, and peripheral memory layouts
- [[12_Portable_serialization_helpers]] — Building robust, zero-dependency serialization macro libraries

## Related Chapters
- [[../00_Complete_Topic_Map]]
- [[../27_C_Alignment_Object_Representation]]
- [[../25_C_Dynamic_Memory]]
