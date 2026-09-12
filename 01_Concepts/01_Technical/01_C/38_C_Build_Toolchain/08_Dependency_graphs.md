# Dependency graphs

> Canonical C topic note — chapter 38.

## Definition
A build dependency graph represents which generated artifacts depend on which sources, headers, libraries, generated files, and configuration inputs. Correct dependency modeling determines whether incremental builds are correct and efficient.

## Mechanism and language rules
A source file depends on directly included headers and relevant generated/configuration inputs. Objects depend on compiler options and source content. Final images depend on objects, libraries, linker scripts, startup files, and link flags.

## Embedded implications
Incorrect graphs create stale objects, non-reproducible binaries, or builds that accidentally use files from a previous configuration. Large embedded repositories benefit from explicit module boundaries and generated-file ownership.

## Edge cases and failure modes
- Header changes not triggering rebuilds.
- Generated configuration omitted from dependencies.
- Compiler flags changing without invalidating cached objects.
- Circular dependencies hiding architectural coupling.
- Parallel builds racing on generated outputs.

## Verification / debugging
Run clean and incremental builds and compare hashes. Inspect build-system dependency files. Change one input at a time and verify the expected artifacts rebuild. Generate dependency graphs for large modules.

## Staff-level takeaway
A build graph is a correctness model, not just a performance optimization. If an input can change the binary, it must be represented as a dependency.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
