# Archive libraries

> Canonical C topic note — chapter 38.

## Definition
An archive library is a collection of relocatable object files, commonly packaged as a static library. The linker extracts members to satisfy unresolved references rather than automatically copying every member into the image.

## Mechanism and language rules
Traditional archive linking is demand-driven: a member is pulled when it provides a currently unresolved symbol. This makes library order significant in many linkers. Options such as grouping, whole-archive, or explicit object references change extraction behavior.

## Embedded implications
Static libraries are common for drivers, middleware, BSPs, and vendor SDKs. Section garbage collection can further reduce unused code when objects/functions are organized appropriately. Library objects must agree with the application's ABI, compiler options, CPU ISA, floating-point ABI, and runtime assumptions.

## Edge cases and failure modes
- Wrong library order.
- Duplicate symbols from multiple libraries.
- Pulling an entire large archive unexpectedly.
- Mixing incompatible floating-point or CPU ABIs.
- Library startup hooks being removed by section garbage collection.

## Verification / debugging
Inspect the linker map to see which archive members were extracted and why. Use symbol tools to verify definitions and undefined references. Rebuild libraries with the same ABI/toolchain contract as the application.

## Staff-level takeaway
A static library is not merely a bag of code. Its extraction rules, ABI, section organization, and dependency assumptions directly affect the final firmware image.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
