# Dead-code elimination

## Definition
**Dead-code elimination (DCE)** removes computations, branches, stores, and sometimes entire functions whose results cannot affect permitted observable behavior. It is one of the most important consequences of the C abstract-machine model: source statements are not sacred if their effects are provably irrelevant.

## Scope and boundaries
A statement is removable only when the compiler can prove that removing it preserves required behavior. A calculation whose value is unused is often removable; a `volatile` access, I/O operation, synchronization operation, or call with unknown side effects generally is not. Undefined behavior can also change what the compiler may assume.

## Mechanism and language rules
Example:

```c
int f(int x)
{
    int unused = x * 7;
    int result = x + 1;
    return result;
}
```

The multiplication and `unused` object may disappear entirely. DCE works locally and globally, often after constant propagation, inlining, control-flow analysis, and interprocedural analysis.

### Unreachable branches
If analysis proves a condition always false, the corresponding branch can be eliminated. If a configuration macro excludes a feature, the preprocessor removes it before compilation; if the compiler proves a runtime condition constant, DCE can remove it later.

### Stores and memory effects
A store to an ordinary local that is overwritten before being read can disappear. A store to a global may disappear only when no valid observer can see it. Volatile stores are observable and therefore have stronger preservation requirements.

## Embedded implications
DCE is valuable for product variants: feature-disabled code, unused protocol paths, debug instrumentation, and unused driver helpers can vanish from the final image. But firmware engineers sometimes accidentally rely on dead code as if it performed hardware initialization. For example, a non-volatile write to an object representing a peripheral register may be optimized away if the compiler has no valid reason to observe it.

DCE can also remove “keepalive” variables used only for debugging. If a diagnostic value must survive, use a real observable mechanism, a debugger-supported facility, or an appropriate volatile design where justified.

## Edge cases and failure modes
- “The source writes it, so the hardware sees it.” Not necessarily.
- Using an ordinary variable for MMIO.
- Keeping safety checks whose result is ignored.
- Assuming logging code exists in the production binary because it remains in the source.
- Expecting linker garbage collection and compiler DCE to behave identically; they operate at different stages.
- Debugger breakpoints becoming impossible because instructions were eliminated or merged.

## Verification / debugging
Inspect optimized assembly and linker map output. Enable section-level garbage collection where appropriate and examine why a symbol is retained or removed. Use compiler optimization remarks when available. For hardware behavior, probe the actual bus/peripheral or inspect target registers rather than relying only on source-level stepping.

## Performance, memory, timing and power
DCE directly reduces instruction count, flash usage, branch paths, and sometimes RAM. Removing unnecessary memory traffic can improve timing and power. It can also change timing enough to invalidate an accidental delay implemented through computation; deliberate delays should use timers or architecture-supported mechanisms.

## Staff-level takeaway
Ask of every apparently unnecessary statement: **what observable contract requires this effect?** If none exists, deletion is probably correct. If the effect matters to hardware, concurrency, diagnostics, or safety, encode that requirement explicitly rather than attempting to defeat optimization with folklore.