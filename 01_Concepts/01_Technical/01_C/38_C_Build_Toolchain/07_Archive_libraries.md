# Archive libraries

## Definition
A static **archive library** is a collection of relocatable object files, commonly stored in an archive such as `.a`. During linking, the linker can extract members needed to satisfy unresolved references. Unlike a shared library, the selected object code becomes part of the final executable image.

## Scope and boundaries
Archive format and extraction behavior are toolchain/object-format details. C only defines the source-level declarations and program semantics. Library headers define the API contract; the archive and linker define how implementations are incorporated.

## Mechanism and language rules
A typical flow is:

```text
module1.c -> module1.o
module2.c -> module2.o
                 \
                  -> libdriver.a -> linker -> firmware
```

A library may contain many object files. Linkers commonly extract an object member when it resolves an unresolved symbol, rather than blindly copying every member.

### Link order
For traditional static linking, order can matter. If `libA.a` depends on `libB.a`, placing A before B often allows unresolved symbols from A to trigger extraction from B. Cyclic dependencies may require grouping or redesign.

## Embedded implications
Archives are widely used for HALs, board support, protocol stacks, middleware, and vendor SDKs. They allow reusable modules while section-level garbage collection can remove unused functions if objects are compiled with appropriate section options.

Library ABI compatibility must include compiler mode, target CPU, floating-point ABI, structure layout, calling convention, packing/alignment assumptions, and runtime library dependencies—not just matching function names.

## Edge cases and failure modes
- Wrong library version selected from the search path.
- Archive order causes unresolved or unexpectedly resolved symbols.
- A registration object is discarded because no direct reference exists.
- Mixed optimization/LTO modes produce unsupported combinations.
- Duplicate weak/strong definitions hide which implementation is active.

## Verification / debugging
Inspect archive members with `ar` or equivalent tools and inspect final symbols with `nm`/`readelf`. Record exact library provenance and build options. Review link maps to identify which archive member supplied a symbol and which members were not extracted.

## Performance, memory, timing and power
Static linking can eliminate runtime loader overhead and allows aggressive dead-code removal, but every retained object contributes to image size. A poorly modularized archive can pull in more code than intended. Library choices also affect floating-point, formatting, allocation, and syscall/runtime costs.

## Staff-level takeaway
A static library is a binary dependency with an ABI contract. Pin its provenance, understand extraction/link-order behavior, and verify exactly what entered the firmware image.