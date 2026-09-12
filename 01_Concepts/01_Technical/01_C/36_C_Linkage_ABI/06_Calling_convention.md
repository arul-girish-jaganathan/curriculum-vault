# Calling convention

> Canonical C topic note — chapter 36.

## Definition
A **calling convention** is the ABI contract describing how a function call transfers control and communicates arguments, return values, registers, stack state and preserved machine state between caller and callee. ISO C specifies function semantics but does not prescribe a CPU register allocation or stack layout.

Typical ABI properties include argument registers, return registers, stack alignment, caller/callee-saved registers, stack growth, variadic handling, floating-point register use, structure passing and exception/unwind metadata where supported.

## Mechanism and language rules
At the C level:

```c
int add(int a, int b)
{
    return a + b;
}
```

The compiler chooses an ABI-compliant machine-level sequence. A caller evaluates arguments, prepares the required locations, performs the call, and later observes the return representation. The callee must preserve exactly the registers and stack state the ABI requires.

The C compiler normally guarantees the ABI automatically when compatible translation units are compiled with compatible settings. Problems appear when objects are mixed across incompatible compiler options, hand-written assembly, foreign languages, incompatible libraries, or incorrect prototypes.

Important dimensions:

- integer/pointer argument registers;
- floating-point registers and hard/soft-float mode;
- stack alignment;
- volatile versus nonvolatile registers;
- return-value registers or hidden return pointers;
- tail-call eligibility;
- variadic register-save areas;
- structure/union classification.

## Embedded implications
Calling convention directly affects interrupt latency, context switching, assembly wrappers, RTOS ports and performance-critical drivers. A context switcher must save the architectural state required by the ABI and execution environment, not merely the registers it happens to observe in one compiler build.

Function-call cost can include argument moves, stack traffic, register spills, prologue/epilogue instructions and pipeline effects. In a hard real-time path, changing optimization or ABI mode can change both timing and stack depth.

### Firmware review angle
For every C↔assembly boundary, keep a written ABI contract. Verify stack alignment, preserved registers, return registers and floating-point state. Never infer the contract from source syntax alone.

## Edge cases and failure modes
An incorrect prototype is particularly dangerous:

```c
/* Caller believes this. */
extern int read_value(void);

/* Actual implementation differs. */
long read_value(int channel) { /* ... */ }
```

If the toolchain does not diagnose the mismatch across translation units, the linker may still resolve the same symbol. The result can be register/stack corruption or incorrect return interpretation.

Other failures include compiling one library with a different floating-point ABI, breaking required stack alignment in assembly, failing to preserve callee-saved registers, and assuming a C function pointer is compatible with a differently attributed calling convention.

## Example pattern
```c
/* Assembly boundary: keep the prototype canonical. */
uint32_t crc32_update(const uint8_t *data, size_t len);
```

The implementation must obey the selected target ABI exactly.

## Verification / debugging
Compile a small ABI probe and inspect disassembly. Use debugger register/stack inspection at the call boundary. Compare compiler options across all objects. Link-time and CI checks should prevent mixing incompatible ABI variants.

Staff-level questions:
- Which ABI document is authoritative?
- Which registers are caller/callee saved?
- What is the required stack alignment at a call site?
- How are aggregates and floating-point values transferred?
- Does LTO or optimization change the observable boundary assumptions?

## Staff-level takeaway
A calling convention is the **machine-level contract behind a C function call**. Treat it as an explicit integration contract whenever code crosses compiler, assembly, language, binary or execution-context boundaries.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
