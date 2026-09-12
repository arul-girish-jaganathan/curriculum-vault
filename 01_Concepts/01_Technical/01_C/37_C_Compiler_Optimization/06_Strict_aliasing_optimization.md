# Strict-aliasing optimization

## Definition
**Strict aliasing** is part of C's object-access rules and gives implementations useful assumptions about which lvalue expressions can designate the same stored object. Optimizers exploit those assumptions to keep values in registers, reorder accesses, eliminate loads, and simplify control flow. Violating the underlying language rules can therefore turn into optimization-dependent miscompilation.

## Scope and boundaries
C permits an object's stored value to be accessed through certain compatible or otherwise permitted lvalue types, including character types for examining object representation. It does not generally permit arbitrary reinterpretation of an object's bytes by dereferencing an unrelated typed pointer. `memcpy`/`memmove`, unions where their semantics apply, and carefully designed serialization are different mechanisms from incompatible typed access.

## Mechanism and language rules
A dangerous pattern is:

```c
float f = 1.0f;
uint32_t u = *(uint32_t *)&f; /* not a portable type-punning method */
```

The conversion may produce an inadequately aligned pointer and the dereference violates the permitted access rules. Prefer:

```c
uint32_t u;
memcpy(&u, &f, sizeof u);
```

when the representation is intentionally copied and the destination type is appropriate.

### `restrict`
`restrict` provides an additional aliasing contract for a pointer expression and its associated accesses. When used correctly it can unlock optimization. When the caller violates the contract, behavior is undefined; `restrict` is not merely a performance hint.

## Embedded implications
Firmware often manipulates packet buffers, DMA descriptors, register blocks, and packed protocols, making aliasing mistakes common. An apparent byte buffer may not satisfy the alignment or effective-type requirements needed to dereference it as a structure. Use explicit decoding, `memcpy`, correctly aligned storage, or carefully specified object construction patterns.

Disabling strict-aliasing optimizations globally can sometimes hide defects but is not a substitute for correcting invalid C. Some embedded codebases intentionally use compiler extensions for type punning; those extensions must be documented and constrained to the supported toolchain.

## Edge cases and failure modes
- Casting `uint8_t *` to an unrelated struct pointer and dereferencing without checking alignment or representation.
- Assuming `char *` permission means every typed reinterpretation is legal.
- Using `restrict` when buffers can actually overlap.
- Mixing MMIO register types with unrelated aliases.
- Relying on `-O0` behavior.
- Treating a sanitizer-clean result as proof of full aliasing correctness; some aliasing violations are difficult to detect dynamically.

## Verification / debugging
Enable strict compiler warnings and optimization diagnostics. Compare behavior under different optimization levels and compilers. Use UBSan where applicable, static analysis, and targeted tests with aliasing and alignment edge cases. Inspect assembly when a value unexpectedly remains cached across a write.

## Performance, memory, timing and power
Correct alias information can remove redundant loads/stores and improve vectorization and register allocation. Incorrect aliasing assumptions can produce silent data corruption. The cost of a safe `memcpy` is often lower than feared because compilers recognize small fixed-size copies and lower them to efficient loads/stores.

## Staff-level takeaway
Treat aliasing as a **semantic contract**. Prefer representations and APIs that make legal accesses obvious. If a performance optimization depends on non-overlap or a particular object representation, encode and verify that assumption rather than relying on casts that happen to work on one compiler.