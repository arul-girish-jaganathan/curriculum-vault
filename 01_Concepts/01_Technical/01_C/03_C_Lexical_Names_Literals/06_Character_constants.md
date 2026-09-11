# Character constants and execution character set

## Core idea
A character constant such as `'A'` is an integer constant whose value is determined using the execution character set and C's character-constant rules. Do not equate its value with an ASCII code unless the target implementation guarantees that mapping.

## Embedded consequences
Character constants often enter protocol parsers, register fields, state machines, diagnostics, and wire formats. ASCII is common, but a protocol contract should state its encoding explicitly instead of relying on source character assumptions.

## Traps
- Assuming `'A' == 0x41` without an implementation/protocol guarantee.
- Confusing a character constant with a string literal such as "A".
- Using multicharacter constants as portable protocol values.
- Mixing source, execution, and external wire encodings.

## Verification
For wire-level code use explicit integer constants or encoding helpers where appropriate. Add compile-time checks when a platform contract requires a particular character-code mapping.

## Staff-level takeaway
Character semantics and wire-format semantics are different contracts. Make encoding boundaries explicit.
