# Static vs Dynamic Libraries

A static library packages object files for selection by the linker. A dynamic library is loaded and linked through a runtime dynamic-linking mechanism. These are build and platform mechanisms, not features defined by ISO C.

## Static linking
Static linking copies selected library code and data into the final image. It simplifies deployment for many embedded products and makes the final artifact self-contained, but can increase flash usage and complicate library updates.

## Dynamic linking
Dynamic linking reduces duplication and permits shared components on systems that support it, but introduces runtime dependencies, loader behavior, versioning concerns and a larger execution environment. It is common in hosted operating systems and uncommon in small bare-metal firmware.

## Embedded implications
Library selection affects code size, initialization, memory use, licensing, security patching and deterministic behavior. A supposedly tiny API can pull in substantial support code if the linker cannot eliminate unused paths.

## ABI boundary
Libraries are coupled to an ABI: calling conventions, object layout, symbol conventions, alignment and other implementation details. Changing compiler, architecture or ABI can invalidate binary compatibility even when source APIs look unchanged.

## Verification
Inspect map files and symbols to understand what was pulled into the image. For shared environments, record loader and library versions. For firmware, verify startup and initialization dependencies of any linked runtime component.

## Staff-level view
Library strategy is a product lifecycle decision. Optimize for total maintenance cost—flash/RAM, updateability, security exposure, toolchain compatibility and reproducibility—not merely initial build convenience.

## Related
- [[09_Linking_overview]]
- [[11_LTO_and_whole_program_optimization]]
- [[36_C_Linkage_ABI]]
- [[38_C_Build_Toolchain]]
