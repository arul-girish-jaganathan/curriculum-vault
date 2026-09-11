# Escape sequences and source/execution character mapping

## Core idea
Escape sequences let source text denote characters and values that are awkward or impossible to write directly. They are interpreted as part of translation; their meaning is distinct from runtime string parsing.

## Important distinctions
Simple escapes such as `\n` denote members of the execution character set with specified semantics; octal and hexadecimal escapes denote character values and can have surprising boundary behavior because the consumed digits are determined lexically. An escape sequence inside a string is part of the literal's contents, not a two-character runtime sequence.

## Embedded consequences
Escape mistakes can corrupt protocol frames, terminal output, logging, test vectors, or register initialization tables. Hex escapes deserve special care when a following hexadecimal digit can become part of the same escape; split literals or explicit byte arrays when the boundary must be unambiguous.

## Failure modes
- Confusing `"\\n"` with `"\n"`.
- Accidentally consuming more hex digits than intended.
- Treating source encoding as the same thing as wire encoding.
- Assuming terminal or host display behavior proves byte values.

## Verification
Dump raw bytes in tests, not only rendered text. For protocol data, compare explicit byte sequences and document the required encoding.

## Staff-level takeaway
Escape syntax is a translation rule, not a serialization specification. Make byte-level contracts explicit at external interfaces.
