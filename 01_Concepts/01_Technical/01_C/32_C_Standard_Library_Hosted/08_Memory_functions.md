# Memory functions

## Definition
The C library provides byte-oriented memory functions in `<string.h>` including `memcpy`, `memmove`, `memcmp`, `memset`, and `memchr`. They operate on raw object representations through `void *`/`const void *` and explicit byte counts rather than null-terminated strings. These functions are foundational for buffers, serialization, initialization, and block movement, but their contracts do not override C's lifetime, bounds, alignment, or effective-type rules.

## Scope and Boundaries
* **Covers:** `memcpy`, `memmove`, `memset`, `memcmp`, `memchr`, byte counts, overlap, object representation, and embedded optimization concerns.
* **Does not cover:** string functions such as `strcpy`/`strlen` in depth or dynamic allocation.

## Why Does It Exist
Typed C operations are not always the right abstraction for copying or initializing raw storage. Memory functions provide a standard byte-level interface for arrays, buffers, structures, communication frames, and object representations.

## Mechanism and language rules
`memcpy(dst, src, n)` copies `n` bytes from the source object into the destination; source and destination must not overlap for a valid call. `memmove` supports overlapping regions by defining the result as if the source bytes were first copied to a temporary array. `memset` writes the low-order `unsigned char` value of its integer argument to each byte, so `memset(x, 1, sizeof x)` does not generally initialize an integer object to numeric value 1.

`memcmp` compares byte representations lexicographically. Equal numeric values need not have identical object representations for every type, so `memcmp` is not a universal equality test for structs or floating-point values. `memchr` searches the first `n` bytes for a byte matching the converted `unsigned char` value.

### What to reason about
- `n` is a byte count and must not exceed the accessible source/destination regions.
- `memcpy` overlap is invalid; choose `memmove` when overlap is possible by design.
- A byte copy does not magically make arbitrary typed access legal; destination lifetime, alignment, effective type, and representation still matter.
- `memset` is appropriate for byte patterns such as all-zero storage when the type's representation makes that meaningful, but it is not a general typed initializer.
- `memcmp` observes object representation, including padding bytes, which can be indeterminate or differ despite logically equal field values.
- The functions return destination/search pointers as specified; they do not report buffer-size correctness for you.

## Embedded implications
Compilers and libc implementations often replace small memory operations with inline loads/stores, loop sequences, or optimized library routines. On MCUs, alignment, cache behavior, bus width, DMA interaction, and memory attributes can strongly affect performance.

### Firmware review angle
Do not use generic `memcpy` on MMIO regions unless the hardware abstraction explicitly permits it; volatile register semantics and access width requirements can make ordinary memory functions inappropriate. For DMA buffers, verify cache maintenance and memory-region accessibility before and after the copy.

## Edge cases and failure modes
- `memcpy(buf, buf + 1, n)` is invalid if the ranges overlap; use `memmove`.
- A `size_t` calculation that wraps before reaching `memcpy` can turn a seemingly bounded operation into a massive out-of-bounds access.
- `memset(&value, 0, sizeof value)` is common but should not be generalized to arbitrary nonzero typed initialization.
- `memcmp` of structures can disagree because of padding bytes.
- Passing a null pointer with a nonzero size is invalid; even zero-size calls should be reviewed carefully rather than relying on folklore about null pointers.
- Copying bytes into storage and immediately accessing them through an incompatible type can violate alignment/effective-type rules.

## Example pattern
```c
#include <string.h>

static int move_bytes(unsigned char *buf, size_t size,
                      size_t from, size_t to, size_t count)
{
    if (from > size || to > size || count > size - from || count > size - to) {
        return -1;
    }

    memmove(buf + to, buf + from, count);
    return 0;
}
```

## Verification / debugging
Test zero, one, exact-boundary, overlapping, adjacent, and maximum-size transfers. Use AddressSanitizer/UndefinedBehaviorSanitizer on host tests where available. For embedded performance, inspect compiler output at each optimization level and benchmark aligned versus unaligned cases on the actual MCU.

Review size arithmetic separately from the memory call; proving that `count <= destination_capacity` is more important than recognizing that `memcpy` itself is a standard function.

## Staff-level takeaway
Memory functions are simple interfaces over difficult correctness boundaries. A Staff engineer should treat every call as a proof obligation: prove source bounds, destination bounds, overlap policy, object lifetime, representation assumptions, and hardware-memory compatibility before optimizing the implementation.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
[[13_C_Pointers/05_void_pointers]]
[[26_C_Lifetime_Aliasing/00_Chapter_Index]]
[[27_C_Alignment_Object_Representation/00_Chapter_Index]]
