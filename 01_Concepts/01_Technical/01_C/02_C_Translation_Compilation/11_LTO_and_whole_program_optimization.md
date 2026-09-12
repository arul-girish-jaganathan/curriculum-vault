# LTO and Whole-Program Optimization

Link-time optimization (LTO) allows the compiler to retain or reconstruct enough intermediate information across translation-unit boundaries for broader optimization. It changes what the compiler can see; it does not change the C language contract.

## Why LTO matters
Without LTO, many compiler decisions are constrained by the current translation unit. With LTO, the implementation may inline functions across files, remove unreachable code, propagate constants and improve interprocedural analysis.

## Embedded benefits
LTO can reduce flash and improve performance, especially in small utility-heavy firmware. It can also expose stack and timing changes because inlining and code layout change. Therefore binary size and timing must be measured rather than assumed.

## Interaction with UB
Optimization assumes the program satisfies the language rules. LTO can make an existing undefined-behavior bug more visible because more information is available to the optimizer. A failure that appears only under LTO is a reason to investigate the program contract, not automatically to disable LTO.

## Debugging
Compare builds with and without LTO, inspect map files and disassembly, and identify the smallest source-level assumption that differs. Preserve the exact production compiler and linker configuration in the investigation.

## Staff-level view
LTO is an architecture-level build optimization because it changes code generation globally. Establish reproducible build inputs and regression budgets for image size, timing, stack and debugging quality before enabling it in a safety- or timing-critical product.

## Related
- [[06_Object_code_generation]]
- [[07_Assembly_inspection]]
- [[12_Reproducible_builds]]
- [[37_C_Compiler_Optimization]]
