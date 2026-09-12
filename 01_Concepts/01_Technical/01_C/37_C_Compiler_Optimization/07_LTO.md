# LTO

> Canonical C topic note — chapter 37.

## Definition
Link-time optimization (LTO) preserves compiler intermediate representation into the link stage so optimization can reason across translation-unit boundaries. It can expose calls, constants, aliases, and unused code that ordinary per-file compilation cannot see.

## Mechanism and language rules
Without LTO, `a.c` is generally compiled without seeing the implementation in `b.c`. With LTO, the optimizer can inline cross-TU functions, propagate constants, eliminate unreachable functions, devirtualize some indirect calls when provable, and perform whole-program analysis.

```c
/* api.c */
static int scale(int x) { return x * 4; }
```

The final machine code may differ substantially from non-LTO output even with identical source and optimization level. LTO is an implementation/toolchain feature, not an ISO C semantic requirement.

## Embedded implications
LTO often reduces flash and improves hot-path performance, but it can also increase build time, change debug information, expose latent UB, alter symbol visibility assumptions, and remove functions or objects that firmware expected to discover indirectly.

Startup tables, interrupt vectors, registration mechanisms, linker-retained symbols, weak hooks, and assembly references require explicit toolchain retention contracts. Attributes such as `used`, linker `KEEP`, or explicit references may be required, depending on the toolchain.

## Edge cases and failure modes
- Assembly referencing a symbol that the compiler cannot see.
- Constructor/registration tables removed as apparently unused.
- Weak-symbol selection changing after whole-program visibility changes.
- Debugger stepping becoming less intuitive.
- Latent UB becoming visible only with LTO.

## Verification / debugging
Build both LTO and non-LTO variants. Compare map files, symbol tables, section sizes, and disassembly. Test all registration/startup paths. Treat differences as expected until a contractual behavior is lost; then identify the missing compiler/linker visibility or retention rule.

## Staff-level takeaway
LTO turns the program from a collection of translation units into a larger optimization domain. Any mechanism that depends on invisible references must have an explicit retention and ABI contract.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
