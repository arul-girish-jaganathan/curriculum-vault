# 07: Floating Serialization

## Definition
Floating serialization is the process of converting IEEE 754 floating-point numbers (`float` and `double`) into portable byte streams and reconstructing them across heterogeneous CPU architectures.

## Scope and Boundaries
- **Covers:** IEEE 754 representation, bit-casting via `memcpy`, endianness conversion for floats, and denormalized numbers.
- **Does not cover:** Integer serialization ([[03_Integer_serialization]]) or arbitrary-precision math.

## Why Does It Exist
Serializing floating-point values presents unique challenges:
- **Representational Divergence:** Although modern hardware universally implements IEEE 754 floating-point standards, older or specialized architectures used different floating-point layouts (e.g., VAX, IBM hexadecimal floating point).
- **Strict Aliasing Prohibitions:** Casting a `float *` directly to a `uint32_t *` to manipulate its bit pattern violates strict aliasing rules ([[../26_C_Lifetime_Aliasing/06_Strict_aliasing]]).

## Mechanism and Language Rules
- **The `memcpy` Solution:** To serialize a float safely without violating strict aliasing, copy its object representation into an integer of identical width (`uint32_t` for `float`, `uint64_t` for `double`) using `memcpy`, serialize the integer using network byte order, and reverse the process upon deserialization.

## Examples
```c
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <arpa/inet.h>

/* Serialize a float into a 4-byte big-endian buffer */
void serialize_float(float f, uint8_t *buf) 
{
    uint32_t u32;
    /* Safe bit-cast via memcpy adhering to strict aliasing rules */
    memcpy(&u32, &f, sizeof(float));
    
    u32 = htonl(u32); /* Convert to network byte order */
    
    buf[0] = (uint8_t)(u32 >> 24);
    buf[1] = (uint8_t)(u32 >> 16);
    buf[2] = (uint8_t)(u32 >> 8);
    buf[3] = (uint8_t)u32;
}

/* Deserialize a float from a 4-byte big-endian buffer */
float deserialize_float(const uint8_t *buf) 
{
    uint32_t u32 = ((uint32_t)buf[0] << 24) |
                   ((uint32_t)buf[1] << 16) |
                   ((uint32_t)buf[2] << 8)  |
                   (uint32_t)buf[3];

    u32 = ntohl(u32); /* Convert from network byte order */

    float f;
    memcpy(&f, &u32, sizeof(float));
    return f;
}

int main(void) 
{
    uint8_t wire[4];
    float original = 3.14159f;

    serialize_float(original, wire);
    float restored = deserialize_float(wire);

    printf("Original Float: %f -> Restored Float: %f
", original, restored);
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Pointer type-punning (`*(uint32_t *)&my_float`) violates strict aliasing rules. Always use `memcpy` for bit-casting floating-point representations.

## Edge Cases and Failure Modes
- **Signaling NaNs & Trap Representations:** Deserializing corrupted bit patterns into floats can introduce trap representations on strict FPU architectures.

## Embedded Implications
- **Sensor Telemetry:** IoT sensors transmitting temperature or pressure floating-point readings must serialize floats via integer bit-casting to ensure endian-independent wire transmission.

## Firmware Review Angle
- **Audit Float Casts:** Flag any pointer casts between `float *` and integer pointers; require `memcpy` bit-casting.

## Compiler, ABI, and Toolchain Implications
- **Builtin Optimization:** Compilers optimize `memcpy`-based bit casts into direct register moves (`movd` on x86, `vmov` on ARM) with zero performance penalty.

## Performance, Memory, Timing, and Power
- **Efficiency:** `memcpy` bit-casting compiles into instantaneous register transfers while maintaining 100% standards compliance.

## Verification / Debugging
- **Precision Checks:** Verify that IEEE 754 round-trip conversions preserve exact floating-point bit patterns without rounding degradation.

## Safety, Security, and Reliability
- **Portability:** Guarantees that floating-point telemetry remains consistent across heterogeneous computing nodes.

## Trade-offs and Alternatives
- **Fixed-Point Arithmetic:** For high-reliability embedded systems where floating-point serialization overhead or precision loss is unacceptable, fixed-point integer arithmetic is often preferred over floats.

## Staff-Level Takeaway
Never type-pun floats using direct pointer casts. Always use `memcpy` to bit-cast floats into fixed-width integers (`uint32_t`/`uint64_t`), convert endianness, and serialize.

## Related Concepts
- [[00_Chapter_Index]]
- [[03_Integer_serialization]]
- [[../26_C_Lifetime_Aliasing/06_Strict_aliasing]]
- [[../30_C_Floating_Point/05_IEEE_754_assumptions]]
