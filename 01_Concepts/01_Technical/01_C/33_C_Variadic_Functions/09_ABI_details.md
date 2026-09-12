# ABI details

## Definition
The ABI (Application Binary Interface) defines how compiled functions exchange data at machine-code boundaries: calling conventions, register usage, stack layout, argument classification, return-value rules, alignment, and object representation. Variadic functions depend heavily on these rules because unnamed arguments have no declared parameter types at the callee boundary.

ISO C specifies the language-level semantics of variadic functions but does not specify a universal register or stack layout. The target ABI and compiler implement the machinery behind `<stdarg.h>`.

## Scope and Boundaries
* **Covers:** argument classification, register/stack passing, floating-point differences, `va_list` representation, and ABI portability.
* **Does not cover:** general C linkage and calling conventions in Chapter 36.

## Why Does It Exist
A compiler needs a concrete machine-level agreement so separately compiled functions can call each other. Variadic functions make this particularly visible because the callee must reconstruct argument locations without a complete parameter list.

## Mechanism and Language Rules
At source level:

```c
int log_message(const char *fmt, ...);
```

At machine level, the ABI may place the fixed `fmt` pointer and unnamed arguments in integer registers, floating-point registers, stack slots, or combinations thereof. `va_start` and `va_arg` hide those details from portable C source.

A common conceptual model is:

`source argument type` → `default promotion` → `ABI classification` → `register/stack location` → `va_arg(type)`.

The model is conceptual rather than a promise that a particular ABI uses a linear stack.

### What to reason about
- Which argument registers exist?
- Are integer and floating-point arguments classified separately?
- When do arguments spill to the stack?
- What alignment does each argument require?
- How are aggregates passed?
- Does the ABI use a register-save area for variadic functions?
- Do hard-float and soft-float configurations use different conventions?

## Examples

### ABI-independent source
```c
#include <stdarg.h>

static int get_int(int count, ...)
{
    va_list ap;
    va_start(ap, count);
    int value = va_arg(ap, int);
    va_end(ap);
    return value;
}
```

The source does not need to know whether `value` was passed in a register or on the stack.

### ABI-sensitive mistake
```c
/* Never implement va_arg by guessing a stack offset. */
```

Hand-written traversal is tied to one compiler/ABI configuration and can fail after optimization or a compiler option change.

## Undefined, Unspecified, and Implementation-Defined Behavior
* The physical argument layout is not specified by ISO C and is therefore an implementation/toolchain concern.
* Source code that assumes a particular stack/register layout is non-portable.
* A valid ABI does not rescue an invalid `va_arg` type contract.
* Changing the floating-point ABI, architecture mode, compiler, or calling-convention options can change how variadic calls are generated.

## Edge Cases and Failure Modes
* **Register exhaustion:** later arguments can move from registers to stack memory.
* **Mixed register classes:** integer and floating-point values can follow separate paths.
* **Large alignment:** an aligned aggregate may force padding before its storage location.
* **Aggregates:** structures can be split, copied, or passed indirectly depending on the ABI.
* **Variadic versus fixed functions:** the same apparent parameter list can have different ABI handling when `...` is present.
* **Cross-language calls:** another language must follow the exact C ABI if it calls a C variadic function.

## Embedded Implications
On ARM Cortex-M and similar MCUs, ABI details directly affect register pressure, stack usage, exception boundaries, and interoperability with assembly or RTOS code. A variadic logger may require more state than a fixed function and can increase stack consumption.

Firmware that changes compiler flags such as floating-point ABI settings must rebuild all affected interfaces. Mixing incompatible object files can cause failures that look like ordinary application bugs.

## Firmware Review Angle
For an unexplained variadic crash, compare the declaration seen by the caller and callee, compiler options, target architecture, floating-point ABI, optimization level, and library build. Do not assume a debugger's argument display is proof of the C-level contract.

## Compiler, ABI, and Toolchain Implications
`<stdarg.h>` is normally implemented using compiler builtins because only the compiler knows enough about the current target ABI to generate correct traversal operations. The libc headers form a source-level bridge to those builtins.

ABI compatibility must include data representation, calling convention, alignment, exception/unwind assumptions where applicable, and compiler options—not merely identical function names.

## Performance, Memory, Timing, and Power
Variadic functions can require extra prologue work to make argument registers available to the traversal mechanism. The cost varies substantially by architecture and ABI.

On resource-constrained firmware, measure stack high-water marks and execution time rather than assuming the cost from source syntax.

## Verification / Debugging
Build small ABI probes for each supported target: pass mixed integer/floating-point arguments, inspect registers and stack in a debugger, and compare optimized/unoptimized output.

Use disassembly to answer concrete questions such as where the third argument lives and how `va_arg` advances to the next argument. Keep compiler and ABI settings under version control and reproduce the exact production toolchain during investigation.

## Safety, Security, and Reliability
ABI mismatches can corrupt control data, produce incorrect diagnostics, or cause hard faults. Cross-module and cross-language variadic interfaces should be minimized because they combine weak type checking with ABI sensitivity.

## Trade-offs and Alternatives
* **Use:** standard `<stdarg.h>` interfaces for portable source-level variadic functions.
* **Avoid:** hand-coded stack/register traversal.
* **Prefer:** fixed typed structures across long-lived or cross-language boundaries.
* **Document:** compiler, architecture, floating-point ABI, and calling-convention assumptions where the interface crosses binary boundaries.

## Staff-Level Takeaway
For variadic C, the ABI is the hidden half of the type contract. A Staff engineer should be able to move from source types to promotions to machine-level argument classification and explain why the standard macros—not guessed stack offsets—are the only portable abstraction. ABI settings are part of the product interface when binary interoperability matters.

## Related Concepts
* [[00_Chapter_Index]]
* [[01_va_list]]
* [[02_va_start]]
* [[03_va_arg]]
* [[05_Default_argument_promotions]]
* [[10_Type_safety_limitations]]
