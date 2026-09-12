# Linking Overview

Linking combines object files and libraries, resolves symbols, applies relocations and produces an executable or another final image according to the target format and linker configuration.

## Symbol resolution
A function or object referenced by one translation unit may be defined in another. The linker matches compatible symbols according to the object format, visibility and linking rules. Multiple-definition and unresolved-symbol failures are often architectural signals about ownership or build composition.

## Relocation
Object code can contain addresses that are not known until placement. The linker assigns final locations and applies relocation information. Embedded linker scripts can place code and data into flash, SRAM, tightly coupled memory, external memory or dedicated sections.

## Static versus dynamic context
Bare-metal firmware usually uses statically linked images, while hosted systems may use dynamic linking. The exact model is platform-specific and should not be assumed from C itself.

## Embedded failure modes
Incorrect linker symbols, section placement, memory-region definitions or startup assumptions can produce binaries that link successfully but fail at boot. Always inspect the linker map and verify section addresses against the MCU memory map.

## Staff-level view
Linking is where source-level ownership meets physical memory and ABI constraints. Treat linker scripts, startup objects and memory placement as version-controlled architecture artifacts, not build trivia.

## Related
- [[08_Compiler_driver_stages]]
- [[10_Static_vs_dynamic_libraries]]
- [[82_C_Linkers_Symbols]]
- [[81_C_Linked_Sections]]
