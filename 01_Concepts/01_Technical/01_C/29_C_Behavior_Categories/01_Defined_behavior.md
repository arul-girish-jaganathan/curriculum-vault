# 01: Defined Behavior

## Definition
Defined behavior refers to program execution semantics explicitly mandated by the ISO C standard. For any valid program construct exhibiting defined behavior, the standard specifies the exact output, computational result, or operational state that must be produced by every conforming C implementation.

## Scope and Boundaries
- **Covers:** ISO C mandated semantics, standard arithmetic guarantees, library function guarantees, and portable execution outcomes.
- **Does not cover:** Implementation-defined variants ([[02_Implementation_defined_behavior]]), unspecified sequencing ([[03_Unspecified_behavior]]), or undefined behavior ([[04_Undefined_behavior]]).

## Why Does It Exist
Defined behavior forms the bedrock of portable programming:
- **Portability:** Guarantees that code compiled on an x86 server, an ARM Cortex microcontroller, or a RISC-V workstation produces identical logical results for standard operations.
- **Contractual Certainty:** Provides developers with a reliable, predictable foundation for building algorithms without relying on compiler-specific quirks.

## Mechanism and Language Rules
- **Mandated Outcomes:** Standard operations (e.g., unsigned integer arithmetic wrapping semantics, basic assignment, core library functions like `memcpy` with valid arguments) have strictly defined behavior.
- **Unconditional Compliance:** Conforming compilers are legally bound by the ISO C standard to implement defined behaviors exactly as specified.

## Examples
```c
#include <stdio.h>
#include <stdint.h>

int main(void) 
{
    /* Unsigned integer arithmetic wrap-around is STRICTLY DEFINED by ISO C */
    uint32_t a = UINT32_MAX;
    uint32_t b = 1;
    uint32_t c = a + b; /* Guaranteed to wrap around to 0 */

    printf("Unsigned wrap result: %u
", c);
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Contrast:** Unlike undefined behavior where compilers can do anything, defined behavior leaves zero room for compiler variation or optimizer interpretation.

## Edge Cases and Failure Modes
- **False Assumptions of Signed Wrap:** Developers often assume signed integer overflow wraps around like unsigned integers; however, signed overflow is **undefined behavior**, not defined behavior.

## Embedded Implications
- **Deterministic Firmware:** Relying strictly on defined behavior ensures firmware operates predictably across toolchain upgrades and different target silicon vendors.

## Firmware Review Angle
- **Verify Arithmetic Types:** Ensure arithmetic involving potential overflow uses unsigned types where wrap-around behavior is explicitly defined by the standard.

## Compiler, ABI, and Toolchain Implications
- **Strict Adherence:** Compilers generate direct machine instructions implementing standard defined behavior without emitting speculative optimizations.

## Performance, Memory, Timing, and Power
- **Predictable Cost:** Defined behaviors translate directly into deterministic machine instruction sequences with predictable execution cycles.

## Verification / Debugging
- **Unit Testing:** Standard unit tests verify that defined behavior functions produce expected numerical and logical outputs across test matrices.

## Safety, Security, and Reliability
- **Safety Standard Compliance:** Safety-critical standards (ISO 26262, IEC 61508) emphasize relying on defined behavior while strictly banning undefined behavior.

## Trade-offs and Alternatives
- **Portability vs. Speed:** Strict adherence to portable defined behavior ensures maximum portability at the potential cost of leveraging specialized platform instructions.

## Staff-Level Takeaway
Defined behavior is your safe harbor in C. Whenever possible, design algorithms to rely exclusively on defined behavior constructs, eliminating platform dependencies and undefined behavior hazards.

## Related Concepts
- [[00_Chapter_Index]]
- [[02_Implementation_defined_behavior]]
- [[03_Unspecified_behavior]]
- [[04_Undefined_behavior]]
