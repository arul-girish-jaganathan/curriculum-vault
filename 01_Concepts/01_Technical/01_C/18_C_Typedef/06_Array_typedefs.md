# 06: Array Typedefs

## Definition
An array `typedef` defines an alias for an array of a specific element type and fixed dimension (e.g., `typedef uint8_t mac_address_t[6];`). While providing convenient shorthand for fixed-size buffers, array typedefs alter standard `sizeof` and parameter-decay mechanics in ways that often confuse developers.

## Scope and Boundaries
Covers: Array alias syntax, multidimensional array typedefs, parameter decay behavior, `sizeof` calculations, and copy restrictions.
Does not cover: Dynamically allocated arrays or flexible array members.

## Why Does It Exist
Array typedefs allow systems engineers to define fixed-width domain entities (e.g., UUIDs, MAC addresses, cryptographic keys, hashes) as distinct types with guaranteed byte dimensions.

## Mechanism and Language Rules
1. **Declaration Syntax:** The bracket dimension attaches to the alias name:
   `typedef element_type alias_t[dimension];`
2. **Sizeof Behavior:** In variable declarations, `sizeof(alias_t)` computes the total size of the array: `dimension * sizeof(element_type)`.
3. **Array Decay in Parameters:** When an array typedef is used as a function parameter, ISO C decay rules apply: the parameter silently decays into a pointer to the first element.
   ```c
   typedef uint8_t sha256_t[32];
   void process_hash(sha256_t hash); 
   /* Decays to: void process_hash(uint8_t *hash) */
   ```
4. **No Direct Assignment:** Just like raw arrays, an array typedef instance cannot be assigned using `=`:
   `sha256_t a, b; a = b; /* ILLEGAL C: Constraint violation */`

## Examples
```c
#include <stdint.h>
#include <string.h>
#include <assert.h>

/* Array typedefs for cryptographic primitives */
typedef uint8_t ipv4_bytes_t[4];
typedef uint8_t mac_addr_t[6];
typedef uint8_t aes128_key_t[16];

static void print_mac(const mac_addr_t mac) {
    /* Trap: sizeof(mac) here is sizeof(uint8_t *), NOT 6! */
    // size_t len = sizeof(mac); // Returns 4 or 8 bytes depending on CPU!
    (void)mac;
}

static void test_array_typedef(void) {
    mac_addr_t local_mac = {0x00, 0x1A, 0x2B, 0x3C, 0x4D, 0x5E};
    
    /* Correct: sizeof on the actual instance evaluates to 6 bytes */
    static_assert(sizeof(local_mac) == 6, "MAC must be 6 bytes");
    static_assert(sizeof(mac_addr_t) == 6, "Type must be 6 bytes");

    mac_addr_t backup;
    // backup = local_mac; /* ERROR: Arrays cannot be assigned! */
    memcpy(backup, local_mac, sizeof(mac_addr_t));
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- Passing an undersized array buffer to a function expecting an array typedef compiles without error (due to pointer decay), but causes out-of-bounds reads/writes (Undefined Behavior).

## Edge Cases and Failure Modes
- **The Sizeof Parameter Trap:** Calling `sizeof(param)` inside a function that took an array typedef returns the size of the pointer (4 or 8 bytes), NOT the dimension of the array.
- **Pass-by-Value Illusion:** Developers mistakenly assume that because the type looks like a scalar (`mac_addr_t`), it is passed by value. It is actually passed by reference (decayed pointer), meaning the function can mutate caller memory.

## Embedded Implications
- **Memory Footprint Safety:** Array typedefs inside structures retain their full dimensions and do not decay, making them safe for framing packed communication packets or flash descriptors.

## Firmware Review Angle
- Audit any function taking an array typedef: verify that `sizeof(param)` is not called on the parameter.
- If true value semantics (direct assignment and pass-by-value) are required, wrap the array in a `struct`:
  `typedef struct { uint8_t bytes[6]; } MacAddress;`.

## Compiler, ABI, and Toolchain Implications
- ABI passing rules treat a parameter declared with an array typedef as a standard pointer in core registers (`R0` on ARM).

## Performance, Memory, Timing, and Power
- Passing array typedefs incurs zero copy overhead since only a pointer is passed.

## Verification / Debugging
- Static analyzers (Clang-Tidy `bugprone-sizeof-expression`) catch `sizeof` evaluations on decayed array parameters.

## Safety, Security, and Reliability
- MISRA C:2012 Rule 17.5: The function argument corresponding to a parameter declared as an array shall have an appropriate number of elements.

## Trade-offs and Alternatives
- **Array Typedef vs. Struct Wrapping:** Wrapping the array inside a `struct` allows direct assignment (`a = b`), true pass-by-value, prevents pointer decay, and fixes `sizeof` traps, at the cost of requiring `.bytes` member access.

## Staff-Level Takeaway
Array typedefs are convenient for sizing variables, but treacherous when used as function parameters due to implicit pointer decay. When designing architectural interfaces, prefer struct-wrapped arrays to preserve value semantics, prevent pointer decay, and eliminate `sizeof` bugs.

## Related Concepts
- `01_Basic_typedefs`
- `02_Struct_typedefs`
- `05_Pointer_typedefs`
