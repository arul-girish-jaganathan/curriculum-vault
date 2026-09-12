# Compiler Driver Stages

The compiler driver coordinates multiple tools and phases rather than being synonymous with the C front end. A typical native or cross-compilation flow may involve preprocessing, compilation, assembly, linking and post-link image generation.

## Why the distinction matters
A command such as `gcc file.c` can invoke a compiler, assembler and linker behind the scenes. Cross compilers add target-specific startup objects, libraries and linker options. Build systems can alter all of these through flags and environment configuration.

## Debugging builds
Capture the complete command line. When a build fails, determine whether the problem is preprocessing, compilation, assembly, linking, missing startup/runtime objects, incompatible libraries, or post-link image generation.

## Embedded chain
A firmware pipeline commonly adds linker scripts, startup code, section placement, binary/hex conversion, signing, checksum generation and flashing. These steps are outside ISO C but are essential to the shipped artifact.

## Reproducibility
Tool versions, flags, target triple, sysroot, linker script and environment variables should be controlled. “Works on my machine” often means the driver selected a different header, library or linker configuration.

## Staff-level view
The build command is part of the program's specification. Source review without build-configuration review is incomplete for systems where compiler and linker behavior affects correctness.

## Related
- [[02_Preprocessing_phase]]
- [[06_Object_code_generation]]
- [[09_Linking_overview]]
- [[12_Reproducible_builds]]
- [[38_C_Build_Toolchain]]
