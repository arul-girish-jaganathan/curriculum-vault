# Name decoration

> Canonical C topic note — chapter 36.

## Definition
**Name decoration** (often called name mangling or symbol decoration) is the transformation of source-level identifiers into linker symbol names by a compiler/toolchain. C generally has comparatively simple external names, but the exact spelling, prefixes, suffixes, leading underscores, case rules, object-file encoding and platform ABI are implementation-specific.

C source code therefore cannot safely assume that a linker symbol has a particular textual spelling unless the toolchain contract explicitly guarantees it.

## Mechanism and language rules
A source declaration such as:

```c
int calculate(int x);
```

has a C-level identifier `calculate`. The compiler emits an object symbol representing that entity. On one target the symbol may appear as `calculate`; another ABI may add decoration. C itself does not standardize `nm` output or object-file symbol spelling.

This becomes especially important at language boundaries. C++ commonly encodes function signatures into symbols for overloads and namespaces. `extern "C"` in C++ requests C linkage for interoperable declarations, but it is a C++ feature, not C syntax.

Calling convention and name decoration are separate concerns. Two objects can have matching names yet incompatible parameter/return conventions, or differently decorated names despite representing intendedly related APIs.

Assembly interfaces may explicitly reference linker names:

```asm
    bl uart_write
```

That assembly is tied to the selected ABI/toolchain. If the compiler changes symbol naming, the assembly must change or use a stable assembler/linker interface.

## Embedded implications
Startup code, vector tables, bootloaders, DSP libraries, vendor assembly, RTOS ports and hand-written context-switch code often cross this boundary. A naming mismatch can cause an unresolved symbol, but a worse failure is a successfully resolved symbol with an incompatible ABI.

### Firmware review angle
Whenever C calls assembly or another language, document:

- exact symbol names;
- calling convention;
- parameter/return representation;
- register preservation rules;
- stack alignment;
- floating-point convention;
- structure layout;
- endianness where binary data crosses the boundary.

Do not infer the contract from a single compiler's generated assembly.

## Edge cases and failure modes
Common traps include assuming all C compilers emit identical names, copying an `nm` spelling into portable source, forgetting a C/C++ linkage boundary, and mixing object files from incompatible ABI modes.

A particularly dangerous case is a manually declared foreign function with the right source name but wrong prototype. The linker sees a symbol; it does not validate the C type contract. The callee may interpret registers or stack slots incorrectly.

## Example pattern
A stable C API intended for C and C++ consumers can be expressed through a C header:

```c
/* api.h */
#ifdef __cplusplus
extern "C" {
#endif

int device_read(void *dst, unsigned len);

#ifdef __cplusplus
}
#endif
```

The `extern "C"` portion is interpreted only by C++.

## Verification / debugging
Inspect object symbols with `nm`/`objdump`/`readelf` or the platform equivalent. Compare compiler-generated assembly at the boundary. For mixed-language builds, compile a tiny ABI test and link it in CI.

Staff-level questions:
- Which exact toolchain defines the symbol spelling?
- Is the boundary C↔C++, C↔assembly, or compiler↔compiler?
- Is the ABI documented independently of implementation names?
- Can a wrapper isolate unstable decoration from the public interface?

## Staff-level takeaway
A linker name is **not the C identifier contract**. Treat name decoration as an ABI artifact, isolate mixed-language boundaries behind stable interfaces, and verify both symbol spelling and calling convention.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
