# Universal character names

## Core idea
Universal character names (UCNs) provide a portable source-level notation for characters that may not be directly available in the source character set. Their use is constrained by C's identifier, character, and string-literal rules; valid source notation does not imply identical external encoding.

## Portability boundary
Separate source representation from execution character set and from any UTF encoding used by a protocol. A compiler may accept a UCN while the generated execution representation depends on the implementation.

## Embedded consequences
UCNs can improve source portability for selected character data, but they are a poor substitute for an explicitly specified wire encoding. Cross-toolchain builds must test both acceptance and resulting runtime bytes where text crosses a hardware or communication boundary.

## Failure modes
- Assuming UCN spelling means UTF-8 bytes at runtime.
- Using UCNs in contexts with additional lexical restrictions.
- Mixing source portability with protocol portability.

## Verification
Compile the same source with supported toolchains and inspect literal bytes when the target encoding matters. Add protocol-level tests against known byte sequences.

## Staff-level takeaway
Text has at least three contracts: source syntax, execution representation, and external encoding. Keep them separate in design and documentation.
