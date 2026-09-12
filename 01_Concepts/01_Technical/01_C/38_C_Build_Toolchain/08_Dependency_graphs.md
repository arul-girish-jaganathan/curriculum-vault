# Dependency graphs

## Definition
A **dependency graph** models which build artifacts depend on which inputs. Nodes can represent source files, headers, generated files, object files, libraries, linker scripts, tools, or configuration; edges describe relationships that determine rebuild order and correctness.

## Scope and boundaries
A correct build graph is different from a filesystem listing. If a generated header, linker script, compiler flag, or tool version affects an output, that relationship should be represented or controlled. Build-system syntax is tool-specific, but the engineering requirement is reproducible dependency closure.

## Mechanism and language rules
A simplified graph is:

```text
config.h -> a.c -> a.o --\
header.h -> b.c -> b.o ----> firmware.elf -> binary
linker.ld -----------------/
```

If `header.h` changes, affected translation units must rebuild. If a linker script changes, the link must rerun even when object files remain identical.

### Dependency closure
The final artifact should be reproducible from declared inputs: source, generated source, headers, compiler/tool versions, flags, linker script, libraries, and relevant environment. Hidden dependencies produce stale or non-reproducible binaries.

## Embedded implications
Generated register headers, protocol definitions, version metadata, device-tree-like configuration, linker scripts, and binary assets often participate in embedded builds. Board variants should have explicit dependency/configuration graphs rather than ad-hoc copied files.

## Edge cases and failure modes
- Header dependency tracking misses generated includes.
- A compiler flag changes but objects are not rebuilt.
- Environment variables silently select a different SDK.
- Linker script changes without triggering a full link.
- Generated files depend on tools whose versions are not pinned.
- Parallel CI exposes an undeclared ordering dependency.

## Verification / debugging
Use build-system dependency visualization or dry-run modes. Delete build outputs and perform clean builds to compare with incremental builds. Capture commands in a compilation database. Verify that changing each important input invalidates the expected outputs.

## Performance, memory, timing and power
Accurate dependency graphs make incremental builds fast because unaffected nodes are reused. Incorrect graphs trade build speed for correctness risk. In large firmware repositories, deterministic parallel builds reduce CI time while preserving exact ordering.

## Staff-level takeaway
A build graph is part of the software architecture. If a build cannot explain why an artifact changed, the system lacks a trustworthy dependency model.