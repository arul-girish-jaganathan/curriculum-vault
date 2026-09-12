# Dead-code elimination

> Canonical C topic note — chapter 37.

## Definition
Dead-code elimination (DCE) removes computations whose results cannot affect required observable behavior. A statement that looks useful to a human is removable if its value is never used and its side effects are not observable under the C abstract machine.

## Mechanism and language rules
Compilers perform local and global DCE after building control-flow and data-flow information. Unreachable branches, unused temporaries, redundant stores, and whole functions may disappear. A call is removable only when the compiler can establish that its effects are irrelevant; ordinary function calls are not assumed pure without evidence.

```c
int f(int x)
{
    int unused = x * 42;
    return 7;
}
```

The calculation of `unused` can disappear. A volatile access, I/O operation, atomic operation, or call with required side effects generally cannot be treated as dead merely because its return value is unused.

Undefined behavior matters: once execution reaches UB, the optimizer is not required to preserve the apparent path that preceded it.

## Embedded implications
DCE is valuable for eliminating unused features and shrinking flash/RAM. It also explains why “dummy reads,” delay loops, debug variables, and defensive-looking calculations may vanish. Link-time garbage collection can extend dead-code removal to sections and unused functions across translation units.

For safety code, a requirement should be represented by a real observable action or verified invariant, not by code that merely “looks like it does something.”

## Edge cases and failure modes
- Busy-wait delay loops removed because the result is unused.
- Diagnostics removed because they only update an unobserved local.
- Expected initialization removed when no defined read follows.
- Assuming a debugger-visible variable must exist in optimized code.
- Marking objects volatile merely to defeat DCE rather than defining the hardware contract.

## Verification / debugging
Inspect optimized assembly and linker map files. Use compiler warnings for unused results and static analysis for unreachable paths. If code must remain for a real external effect, identify that effect explicitly and test it.

## Staff-level takeaway
Ask “what observable contract keeps this code alive?” If the answer is only source-code intent, the design is fragile. Make required effects explicit and let dead-code elimination expose unnecessary complexity.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
