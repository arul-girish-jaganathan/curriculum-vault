# LTO

## Definition
**Link-time optimization (LTO)** allows the compiler to perform optimization with visibility across translation-unit boundaries. Instead of treating every object file as an opaque unit until linking, the toolchain preserves optimization information so the linker/compiler pipeline can inline functions, propagate constants, eliminate unreachable code, devirtualize applicable calls, and reason about whole-program relationships.

## Scope and boundaries
LTO does not change the C language rules. It changes how much of the program the implementation can see at optimization time. It can expose bugs that were accidentally masked by separate compilation, particularly invalid aliasing, violated `const` assumptions, missing declarations, and incorrect assumptions about external visibility.

## Mechanism and language rules
With ordinary compilation, `a.c` and `b.c` are usually compiled separately. With LTO, optimization metadata or intermediate representation can survive into the link stage. Example:

```c
/* api.h */
int scale(int x);

/* api.c */
int scale(int x) { return x * 4; }
```

A non-LTO build may require a real call. LTO can discover that `scale` is small, inline it, propagate a constant argument, and eliminate the function symbol if no externally required reference remains.

### Linkage and visibility
Internal-linkage `static` functions are easy for the compiler to reason about. External symbols may remain visible to unknown consumers unless the build proves otherwise. Visibility attributes and whole-program assumptions can affect the optimizer, but they are toolchain/ABI contracts rather than ISO C rules.

## Embedded implications
LTO can substantially reduce firmware flash and improve hot-path performance by removing abstraction overhead. It is especially effective in layered HAL/driver code where many small wrappers otherwise cross translation units. It can also change symbol availability, debug experience, section retention, startup code, and timing.

A production build should test the exact LTO configuration used for release. Debugging a non-LTO binary and assuming identical code generation in the release image is unreliable.

## Edge cases and failure modes
- Missing prototypes or inconsistent declarations become more dangerous when optimization sees both sides.
- Symbols expected by bootloaders, debuggers, scripts, or external tools may disappear or be transformed.
- Inline/static definitions can interact with linkage and visibility mistakes.
- Weak/strong symbol override patterns may behave differently when whole-program optimization is enabled.
- LTO can expose undefined behavior that was previously hidden by call boundaries.

## Verification / debugging
Build with and without LTO and compare map files, symbol tables, disassembly, section sizes, and runtime measurements. Verify required externally consumed symbols with `nm`, `objdump`, or equivalent tools. Add CI builds for both representative development and production configurations.

## Performance, memory, timing and power
Benefits include interprocedural inlining, constant propagation, dead-code elimination, better register allocation, and reduced call overhead. Costs include longer builds, higher peak compiler memory use, and potentially less predictable debug symbols. Code-size reduction can improve flash pressure and instruction locality, but aggressive inlining can also increase code size.

## Staff-level takeaway
LTO should be treated as part of the product's compiler contract, not as an optional final switch. Document the exact toolchain, flags, linker behavior, symbol-retention rules, and verification evidence for the release image.