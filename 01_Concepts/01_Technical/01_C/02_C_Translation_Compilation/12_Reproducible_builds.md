# Reproducible Builds

A reproducible build is one where the same controlled inputs produce the same intended artifact, subject to the reproducibility guarantees of the toolchain and environment. For firmware, reproducibility supports debugging, release integrity, supply-chain confidence and field-forensics.

## Inputs that matter
Record source revision, compiler and binutils versions, target triple, language mode, compiler flags, linker script, libraries/sysroot, generated sources, build tools and relevant environment variables. Timestamps, paths and nondeterministic metadata may also affect artifacts.

## Why byte identity is useful
Bit-for-bit identity makes artifact comparison simple, but reproducibility can also be defined at a weaker semantic level when toolchains insert unavoidable metadata. The chosen definition should be explicit.

## Embedded workflow
A release should retain the exact image, map file, symbol information and build manifest. If a field device crashes months later, engineers should be able to reconstruct the code and configuration that produced its firmware.

## Security and safety
Reproducibility improves supply-chain review because unexpected artifact differences become visible. It also supports safety evidence by making the relationship between reviewed source and released binary easier to demonstrate.

## Common failures
- unpinned toolchain versions;
- build timestamps embedded in binaries;
- host-dependent generated files;
- uncontrolled environment variables;
- different linker scripts or startup objects;
- downloaded dependencies that changed without version pinning.

## Staff-level view
Reproducibility is an organizational capability, not just a compiler flag. Define the artifact identity contract, preserve build inputs, and continuously verify representative releases.

## Related
- [[08_Compiler_driver_stages]]
- [[09_Linking_overview]]
- [[11_LTO_and_whole_program_optimization]]
- [[38_C_Build_Toolchain]]
