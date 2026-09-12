# Source to translation unit

## What a translation unit is
A **translation unit** is the C source program after preprocessing. It is the unit on which the compiler performs parsing and semantic analysis before producing an object file or other compiler output.

A useful mental model is:

`source file → preprocessing → translation unit → compilation → object code → linking`

The terms are deliberately distinct. A `.c` file is a source-file convention; a translation unit is the language/compiler concept resulting from preprocessing that source together with the included header contents and active macro/directive effects.

## Why this model exists
C supports separate compilation. Large programs can be divided into source files that are compiled independently and later linked. This provides:

- faster incremental builds
- separate ownership of implementation units
- controlled interfaces through headers
- reuse through libraries
- different build configurations for different targets

The linker subsequently combines independently produced object files and libraries.

## How preprocessing changes the input
Preprocessing handles directives and macro expansion before the compiler parses ordinary C constructs. `#include` incorporates the included header's preprocessing tokens into the resulting translation unit; it is not a runtime operation and does not create a module boundary.

```c
/* config.h */
#define BUFFER_SIZE 128

/* driver.c */
#include "config.h"
static unsigned char buffer[BUFFER_SIZE];
```

Conditional compilation can make two builds of the same source file produce materially different translation units:

```c
#ifdef FEATURE_X
void feature_x(void) { /* ... */ }
#endif
```

Therefore, source text alone is insufficient when diagnosing configuration-dependent build behavior.

## Translation-unit boundaries and linkage
A translation unit can contain declarations and definitions with different linkage properties. For example:

```c
/* a.c */
int counter;

/* b.c */
extern int counter;
```

The two translation units communicate through the language's declaration/linkage rules and, ultimately, the implementation's ABI and linker.

By contrast:

```c
/* a.c */
static int counter;
```

has internal linkage, so another translation unit cannot refer to that object by an ordinary external declaration.

This explains an important build distinction: a source file can compile successfully while the final program still fails to link.

## What is specified vs implementation/toolchain behavior
The C language specifies the translation process and the semantics/constraints of the resulting program. It does **not** prescribe a particular object-file format, assembler syntax, linker implementation, optimization pipeline, debugger format, or ABI.

Common implementation/toolchain choices include:

- object format such as ELF or another vendor format
- compiler driver stages
- assembler invocation
- linker and linker-script behavior
- symbol naming conventions
- ABI and calling conventions
- optimization passes
- debug-information format
- startup/runtime support

A conforming implementation can therefore have a very different internal pipeline while preserving required C semantics.

## Headers are not independently compiled modules
A common misconception is that each header is compiled independently. In the traditional C compilation model, a header is textually incorporated into each translation unit that includes it. The same header can therefore behave differently in different translation units because macro definitions, include order, feature-test configuration, compiler options, and target configuration can differ.

This is why header design, include guards, declaration consistency, and controlled configuration are important in large firmware builds.

## Embedded-system consequences
Translation-unit boundaries affect real firmware in several ways:

- startup code may be compiled separately from application code
- interrupt handlers may be referenced through symbols or linker-defined mechanisms
- linker scripts combine sections from many object files into flash/RAM regions
- `static` objects affect generated sections and final image size even though they are not externally visible
- target CPU, ABI, optimization, and section-placement options affect generated code
- different preprocessor configurations can produce materially different firmware images

For memory-constrained systems, source-file size is not a reliable predictor of flash/RAM consumption. Inspect object files and the final linker map.

## Failure modes
### Configuration drift
Two translation units may be compiled with incompatible feature macros or ABI-affecting options. The source can appear correct while the final program violates an interface assumption.

### Missing definition
A declaration can compile successfully but produce an undefined-symbol failure during linking if no compatible definition is supplied.

### Multiple definitions
Incompatible definitions or declarations across translation units can produce diagnostics or linker failures, depending on the exact language rule and implementation.

### Header-dependent behavior
A header that depends on macro state or include order can expose different declarations or implementations to different translation units.

### Debug/release divergence
Optimization and conditional compilation can make generated code, symbols, layout, and observable timing differ between configurations.

## Debugging workflow
When behavior differs between builds:

1. Capture the exact compiler command line for the affected source.
2. Inspect preprocessed output when macro/include behavior is suspected.
3. Compare language-standard, target CPU, ABI, optimization, and feature macros.
4. Inspect generated assembly/object symbols when code generation is involved.
5. Inspect the linker map and symbol table for final resolution and placement.
6. Verify that shared declarations are consistent across all translation units.

Useful tools include compiler preprocessing modes, diagnostics, `nm`, `objdump`, `readelf` for ELF-based toolchains, linker map files, and a debugger.

## Staff-level reasoning
When a build problem crosses a `.c`/`.h` boundary, first identify **which phase owns the symptom**:

- preprocessing → macros/includes/configuration
- compilation → syntax, constraints, types, semantics
- code generation → compiler options/optimization/assembly
- linking → symbols, sections, ABI, libraries
- runtime → generated image and target behavior

This phase-based model prevents treating every build failure as a generic compiler problem.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
