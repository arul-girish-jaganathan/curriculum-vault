# C99 Additions

C99 changed everyday C programming substantially while retaining the core C model. For embedded engineers, the important question is not simply “what syntax was added?” but which features improve correctness, analyzability, expressiveness, and numerical code without introducing an unacceptable toolchain or certification burden.

## Major additions
C99 introduced mixed declarations and code, `//` comments, variable-length arrays (VLAs), designated initializers, compound literals, `inline`, `restrict`, `_Bool` and `<stdbool.h>`, `long long`, hexadecimal floating constants, and a substantially expanded library and preprocessing model. It also strengthened the language's support for integer types and floating-point programming.

### Designated initializers
Designators let initialization name an array element or structure member explicitly:

```c
struct Config c = {
    .timeout_ms = 100,
    .enabled = 1,
};
```

This reduces positional coupling when structures evolve. In embedded configuration tables, that can improve reviewability and reduce accidental field shifts. The trade-off is toolchain/coding-standard compatibility in older environments.

### `restrict`
`restrict` is a promise about how an object is accessed through pointer expressions during an execution. It can enable optimization because the implementation may assume the required non-aliasing relationship. It is not a general “make pointer faster” keyword. A false promise can create undefined behavior and optimization-dependent failures.

### VLAs
A VLA has a runtime-determined bound and automatic storage duration. It can be useful for bounded algorithms, but embedded systems must account for worst-case stack consumption. Some projects prohibit VLAs because stack depth is harder to prove and because compiler support or safety rules may restrict them.

## Embedded engineering implications
C99 features should be evaluated against four boundaries: language semantics, compiler support, ABI/object representation, and project policy. Designated initialization is usually a low-risk readability improvement; VLAs and `restrict` demand stronger architectural reasoning.

C99 also made it easier to write numerical and portable code, but the language still does not make a particular MCU's integer width, alignment, endianness, floating-point hardware, or ABI universal.

## Common mistakes
- Treating `restrict` as an optimization directive rather than a semantic contract.
- Assuming every C99 feature is supported equally by every embedded compiler.
- Using VLAs without a defensible stack bound.
- Assuming designated initialization implies a particular binary layout.

## Verification
Compile with the project's actual language mode and warnings enabled. For ABI-sensitive code, inspect object layout and generated assembly. For stack-sensitive code, measure and bound worst-case depth rather than relying on nominal tests.

## Staff-level view
Modernization should be evidence-driven. Select features because they reduce defect probability or improve maintainability, then verify compiler, static-analysis, certification and binary-impact consequences. A language feature is an engineering tool, not a maturity badge.

## Related
- [[01_C89_C90_heritage]]
- [[05_C23_modernization]]
- [[08_Implementation_defined_behavior]]
- [[37_C_Compiler_Optimization]]
