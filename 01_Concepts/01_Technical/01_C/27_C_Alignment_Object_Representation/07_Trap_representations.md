# 07: Trap Representations

## Definition
A trap representation is an object representation that does not correspond to any valid value of the object type. Accessing or evaluating an object whose storage contains a trap representation (even by simple lvalue evaluation) can trigger hardware exceptions, processor traps, or undefined behavior.

## Scope and Boundaries
- **Covers:** Invalid bit patterns, floating-point signaling NaNs, integer trap representations, and uninitialized reads.
- **Does not cover:** Normal padding bytes ([[06_Padding_bytes]]), valid bit-fields, or strict aliasing violations ([[../26_C_Lifetime_Aliasing/06_Strict_aliasing]]).

## Why Does It Exist
Hardware architectures and C language semantics permit certain bit patterns to be reserved or invalid:
- **Signaling NaNs (sNaN):** In IEEE 754 floating-point arithmetic, certain bit patterns represent signaling NaNs which trigger hardware floating-point exceptions when loaded or operated upon.
- **Legacy Integer Representations:** On obsolete or specialized hardware (e.g., ones' complement or sign-magnitude architectures), invalid bit patterns (like negative zero in certain contexts or parity error bits) served as trap representations.

## Mechanism and Language Rules
- **Lvalue Evaluation Hazard:** If an object's storage holds a trap representation, evaluating it as an lvalue (e.g., `int x = my_var;`) can invoke undefined behavior immediately.
- **Uninitialized Variables:** Reading an uninitialized automatic variable whose bit pattern happens to form a trap representation causes catastrophic undefined behavior.

## Examples
```c
#include <stdio.h>
#include <stdint.h>
#include <string.h>

int main(void) 
{
    float f;
    /* Constructing a signaling NaN or invalid bit pattern in float */
    uint32_t invalid_bits = 0x7FA00000; /* Signaling NaN bit pattern */
    memcpy(&f, &invalid_bits, sizeof(f));

    /* Evaluating f can trigger hardware float exceptions on strict FP units */
    printf("Loaded float representation successfully.\n");
    
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Evaluating an expression that yields a trap representation.
- **Implementation-Defined:** Whether standard integer types contain trap representations (in modern two's complement architectures, all bit patterns for integer types typically represent valid values, eliminating integer trap representations, but floating-point trap representations remain possible).

## Edge Cases and Failure Modes
- **Bitwise Deserialization:** Deserializing corrupted data from a storage medium or network stream into specialized types can accidentally inject trap representations into application memory.

## Embedded Implications
- **DSP / FPU Traps:** Digital Signal Processors (DSPs) with specialized arithmetic units can hard-fault instantly if an invalid floating-point trap representation is fed into an ALU pipeline.

## Firmware Review Angle
- **Sanitize External Inputs:** Never copy raw untrusted external byte streams directly into floating-point variables without validation, as invalid bit patterns can introduce trap representations.

## Compiler, ABI, and Toolchain Implications
- **Optimizer Assumptions:** Compilers assume that variables never hold trap representations. If optimization passes detect code that could produce or load trap representations, optimizer assumptions can cause unpredictable control flow divergence.

## Performance, Memory, Timing, and Power
- **Hardware Traps:** Triggering a floating-point trap representation invokes OS trap handlers, causing massive execution stalls.

## Verification / Debugging
- **Floating-Point Exceptions:** Enable hardware floating-point exception traps (`fesetenv`) during debugging to catch invalid FP operations instantly.

## Safety, Security, and Reliability
- **Safety Standards:** Safety-critical software (DO-178C) strictly mandates initializing all variables upon declaration to prevent uninitialized trap representation hazards.

## Trade-offs and Alternatives
- **Raw Bytes vs. Typed Values:** Always ingest untrusted data into `unsigned char` buffers first, validate value ranges, and only then assign to typed variables.

## Staff-Level Takeaway
Trap representations represent illegal bit states in memory. Modern two's complement integer types rarely have trap representations, but floating-point and specialized hardware types remain vulnerable. Always sanitize external data before casting or assigning to typed variables.

## Related Concepts
- [[00_Chapter_Index]]
- [[04_Object_representation]]
- [[06_Padding_bytes]]
- [[09_Serialization_hazards]]
