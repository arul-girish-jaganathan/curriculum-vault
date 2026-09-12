# 12: Sanitizer Backed Review

## Definition
Sanitizer-Backed Review is an engineering verification workflow that integrates compiler instrumentation tools—specifically AddressSanitizer (ASan) and UndefinedBehaviorSanitizer (UBSan)—into code reviews, continuous integration (CI) pipelines, and testing suites to catch lifetime and aliasing bugs automatically.

## Scope and Boundaries
- **Covers:** ASan, UBSan, compiler flags (`-fsanitize=address,undefined`), runtime memory error detection, and test instrumentation.
- **Does not cover:** Static code analysis tools or manual code inspection techniques.

## Why Does It Exist
Human code reviews and static analysis cannot catch every subtle use-after-free, out-of-bounds access, or strict aliasing violation. Sanitizer-backed review leverages compiler-injected runtime checks to intercept memory errors instantly upon test execution.

## Mechanism and Language Rules
- **AddressSanitizer (ASan):** Detects use-after-free, double free, heap/stack buffer overflows, and stack-use-after-return by "poisoning" shadow memory zones around allocations.
- **UndefinedBehaviorSanitizer (UBSan):** Detects signed integer overflow, null pointer dereferences, unaligned memory accesses, and strict aliasing/type violations at runtime.
- **Compiler Flags:**
  - GCC/Clang: `-fsanitize=address,undefined -fno-sanitize-recover=address`

## Examples
```bash
# Compilation command with sanitizers enabled
gcc -O2 -g -fsanitize=address,undefined -fno-sanitize-recover=address main.c -o main

# Execution will immediately abort with a detailed stack trace upon memory corruption
./main
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Sanitizer Interception:** Sanitizers intercept standard library calls (`malloc`, `free`, `memcpy`) to track object lifetimes and boundaries in shadow memory.

## Edge Cases and Failure Modes
- **Performance Penalty:** Sanitizers increase binary size and slow execution speed by 2x to 3x, making them unsuitable for production deployment on resource-constrained embedded targets.
- **Platform Limitations:** Requires OS support (Linux, macOS, Windows) and virtual memory management, restricting direct bare-metal sanitizer use.

## Embedded Implications
- **Host-Based Unit Testing:** Run embedded unit tests and hardware abstraction layer (HAL) stubs on a hosted x86 development machine with ASan/UBSan enabled to catch memory bugs before flashing to target microcontrollers.

## Firmware Review Angle
- **Mandatory CI Gate:** Require all unit tests and integration test suites to pass cleanly under `-fsanitize=address,undefined` before code is merged.
- **Review Sanitizer Reports:** Treat any sanitizer warning or crash report as a blocker bug.

## Compiler, ABI, and Toolchain Implications
- **Shadow Memory Mapping:** ASan reserves a large region of virtual memory for shadow tracking, modifying instrumentation hooks during code generation.

## Performance, Memory, Timing, and Power
- **Development-Only Tool:** Never ship firmware binaries compiled with ASan enabled due to memory and CPU overhead.

## Verification / Debugging
- **Detailed Tracebacks:** Sanitizers output exact source file names, line numbers, and memory offset diagrams when a violation occurs.

## Safety, Security, and Reliability
- **Defensive Engineering:** Automated sanitizer validation catches zero-day memory corruption flaws before deployment in safety-critical systems.

## Trade-offs and Alternatives
- **Sanitizers vs. Valgrind:** ASan is significantly faster and catches stack/global overflows that Valgrind misses, whereas Valgrind requires no recompilation.

## Staff-Level Takeaway
Never rely solely on static inspection for memory safety. Establish sanitizer-backed testing as a non-negotiable engineering gate. Run your test suites under ASan and UBSan religiously to eliminate lifetime and aliasing bugs prior to production release.

## Related Concepts
- [[00_Chapter_Index]]
- [[03_Dangling_pointers]]
- [[04_Use_after_free]]
- [[06_Strict_aliasing]]
