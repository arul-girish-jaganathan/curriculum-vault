# C89/C90 heritage

> Canonical C topic note — chapter 01. This note explains the historical baseline that still shapes embedded C code, toolchains, coding standards, and ABI expectations.

## 1. What C89/C90 established

C89 is the 1989 ANSI C standard; ISO adopted the specification as C90 in 1990. It standardized much of the language commonly associated with "traditional ANSI C" and, critically for embedded work, gave implementations a portable semantic baseline instead of leaving compiler behavior to individual vendors.

The important engineering lesson is not to memorize the historical date. It is to recognize that a large body of embedded code, compiler libraries, coding standards, and vendor headers still carries assumptions rooted in the C90-era language model.

C90 introduced or standardized, among other things:

- function prototypes and typed parameter declarations;
- `void` and `void *` usage as standardized language mechanisms;
- `const`, `volatile`, and `signed` qualifiers/specifiers;
- enumerated types;
- standard headers and a defined hosted implementation library interface;
- declarations with a form suitable for portable translation across implementations;
- a formal distinction between what the implementation must diagnose and what the implementation may choose.

A crucial historical constraint is that C90 uses the classic declaration model: within a block, ordinary declarations precede executable statements. C90 also does not provide C99's `//` comments, declarations inside `for` initializers, designated initializers, VLAs, or compound literals.

## 2. The declaration model and why legacy code looks different

In C90-style code, a block commonly looks like this:

```c
void process(void)
{
    int count;
    unsigned char buffer[64];

    count = 0;
    /* executable statements follow declarations */
}
```

A C99-and-later compiler may accept:

```c
void process(void)
{
    int count = 0;

    step();

    unsigned char buffer[64];
    use(buffer);
}
```

but the second form violates the C90 declaration-placement rule.

### Embedded consequence

Many legacy embedded projects intentionally retain C90-compatible source because:

- an old vendor compiler may only implement part of later standards;
- certification or coding-rule baselines may restrict the accepted language subset;
- the same firmware may have to build with multiple compilers;
- automatically generated code may assume an older dialect;
- long-lived product code benefits from a deliberately frozen language baseline.

Therefore, "the compiler accepts it" is not equivalent to "the project language baseline permits it."

## 3. `const` and `volatile`: historical foundation, modern consequences

`const` expresses that an object is not modified through a particular access path. It does **not** mean the storage is physically read-only, immutable across all aliases, or suitable for synchronization.

`volatile` expresses that accesses to an object are observable side effects that the implementation must preserve according to the volatile rules. It is intended for objects such as memory-mapped I/O registers and other implementation-defined externally observable state.

Example:

```c
#define UART_STATUS (*(volatile unsigned int *)0x40000000u)

unsigned int read_status(void)
{
    return UART_STATUS;
}
```

The historical presence of `volatile` is important because embedded engineers still encounter code that incorrectly treats it as a general-purpose concurrency primitive.

It is not a replacement for atomic operations, locks, or the C11 memory model.

## 4. Function prototypes changed how errors are caught

A prototype communicates parameter types and the return type to the caller:

```c
int add(int a, int b);
```

Calling a function through a visible compatible prototype enables the compiler to diagnose many argument mismatches before execution.

Legacy declarations such as:

```c
int add();
```

do **not** mean "takes no arguments" in the modern prototype sense; the empty parameter list denotes an unspecified parameter list in a declaration that is not a prototype.

For new embedded APIs, prefer explicit prototypes:

```c
int add(int a, int b);
```

This reduces interface ambiguity and makes compiler diagnostics useful.

## 5. C90 portability is not the same as machine independence

C90 standardized the language, not every property of a processor or ABI.

Still implementation-dependent or implementation-defined areas include details such as:

- sizes and representations of several integer types;
- signedness of plain `char`;
- alignment requirements;
- byte order and object representation;
- exact widths of implementation types;
- ABI calling conventions;
- whether a target is hosted or freestanding;
- behavior of implementation extensions.

For embedded systems, this means code cannot safely infer target properties from source syntax alone.

Bad assumption:

```c
unsigned long timestamp;
/* assume this is always exactly 32 bits */
```

Better, when a fixed-width integer is required by the design:

```c
#include <stdint.h>

uint32_t timestamp;
```

Even then, the engineer must understand the availability and semantics of the selected type in the target environment.

## 6. Historical language baseline versus modern compiler extensions

Modern compilers commonly accept code beyond the selected language standard. For example, a C90 build may accept C99 constructs under extension mode.

That creates a hidden portability dependency:

```text
source code
    ↓
compiler dialect + extension set
    ↓
ABI + optimization behavior
    ↓
target executable
```

If the source depends on an extension without documenting it, changing compiler, compiler version, warning policy, or optimization mode may break the build or—more dangerously—change behavior while still producing a valid executable.

## 7. Edge cases and failure modes

### Empty parameter list confusion

```c
int f();
```

Do not read this as the same thing as:

```c
int f(void);
```

The latter explicitly states that the function has no parameters.

### Declaration-placement assumptions

A project claiming C90 compatibility can fail when declarations are introduced after statements, even though a modern compiler accepts the source.

### Plain `char`

Do not assume `char` is signed or unsigned across targets. Code that relies on its sign can behave differently between toolchains.

### Integer widths

Do not equate source-level type names with fixed hardware widths unless the language implementation guarantees the required property.

### Vendor-specific extensions

Keywords, pragmas, attributes, address-space qualifiers, packed structures, interrupt declarations, and compiler intrinsics can create dependencies that are invisible in a purely ISO-C discussion.

## 8. Embedded design patterns

### Keep hardware dependencies at boundaries

```c
typedef struct
{
    uint32_t control;
    uint32_t status;
} peripheral_regs_t;

static volatile peripheral_regs_t * const regs =
    (volatile peripheral_regs_t *)0x40000000u;
```

The representation and address are hardware-specific, but the rest of the firmware can be isolated behind a driver interface.

### Make assumptions explicit

```c
#include <stdint.h>

_Static_assert(sizeof(uint32_t) == 4, "unexpected uint32_t representation");
```

The exact assertion is a modern-language feature; the engineering principle is historical and universal: do not leave critical platform assumptions implicit.

## 9. Verification and debugging

When reviewing legacy embedded C, answer these questions before changing syntax:

1. What language standard does the build actually select?
2. Which compiler extensions are enabled?
3. Is the source intentionally portable to C90, or merely old?
4. Are any declarations relying on a later dialect?
5. Are `char`, `int`, `long`, or pointer widths being assumed?
6. Are ABI-sensitive structs or function interfaces crossing module boundaries?
7. Are volatile accesses being used for MMIO, or incorrectly for synchronization?

Useful evidence includes compiler standard macros, build flags, warning output, generated assembly, linker maps, ABI documentation, and representative builds on every supported compiler/target.

## 10. Staff-level takeaway

The practical value of C89/C90 knowledge is understanding why apparently simple source decisions can encode portability and ABI assumptions.

A Staff Engineer should be able to distinguish:

- language-standard guarantees;
- implementation-defined choices;
- ABI conventions;
- vendor extensions;
- project coding-policy restrictions.

The right question is rarely "Is this valid C?" It is:

> "Is this valid for our declared language baseline, our compiler set, our ABI, our target memory model, and the portability guarantees the product actually needs?"

## References

- ISO/IEC 9899:1990 — Programming languages — C.
- WG14 C standards archive: https://www.open-std.org/jtc1/sc22/wg14/www/standards
- cppreference C language reference: https://en.cppreference.com/w/c/language

## Related

[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
[[02_C99_additions]]
[[03_C11_concurrency_and_atomics]]
