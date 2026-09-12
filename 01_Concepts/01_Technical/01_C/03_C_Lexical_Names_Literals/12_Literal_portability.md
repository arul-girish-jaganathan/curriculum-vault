# Literal portability review

## Review method
For every literal in portable embedded C, classify its contract: numeric value, resulting C type, representation, encoding, storage, and interface role. Never assume that visual spelling uniquely determines all of those properties.

## High-risk areas
- Integer suffix and width assumptions.
- Signed/unsigned interactions.
- Floating constants on targets with different FP implementations.
- Character and string encoding.
- Escape-sequence boundaries.
- Literal storage and qualification.

## Embedded review example
Instead of assuming a protocol field can be written as a character literal, document the actual protocol byte. Instead of assuming `1000` has a desired unsigned width, compare the expression type and conversion at the API boundary.

## Evidence
Use compiler warnings, `sizeof`/type checks where useful, generated assembly, linker maps, raw-byte tests, and cross-compiler builds. For ABI-facing code, inspect symbols and calling conventions.

## Staff-level takeaway
Portability is not achieved by avoiding exotic syntax alone. It comes from identifying every implementation-sensitive assumption and turning important ones into explicit contracts or tests.
