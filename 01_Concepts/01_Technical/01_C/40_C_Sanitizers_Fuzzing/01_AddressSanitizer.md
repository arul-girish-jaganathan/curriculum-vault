# AddressSanitizer

## Definition
**AddressSanitizer (ASan)** is a compiler/runtime instrumentation technology for detecting many memory-safety errors, including heap and stack buffer overflows, use-after-free, use-after-scope in supported configurations, and related invalid accesses. It is primarily a testing tool rather than a production-memory-safety mechanism.

## Scope and boundaries
ASan availability and exact options depend on compiler, target, operating system, and runtime. It can miss defects it cannot instrument or model, and its memory/time overhead makes it unsuitable for many constrained MCUs. A clean ASan run is evidence, not proof of memory safety.

## Mechanism and language rules
The compiler instruments memory accesses and allocation/deallocation paths. A shadow-memory model tracks whether application memory is addressable. When an instrumented access reaches poisoned/red-zone memory, the runtime reports the location and stack traces.

Conceptually:

```text
program -> compiler instrumentation -> ASan runtime -> shadow memory
```

## Embedded implications
The strongest workflow is often host-side testing of portable parsing, buffers, allocators, protocol logic, and drivers with hardware dependencies abstracted. The same C module can then be built for the MCU without ASan. This finds a large class of defects before target testing.

For target systems that support a sanitizer runtime, evaluate memory overhead, reserved address space, interrupt behavior, and real-time distortion before use.

## Edge cases and failure modes
- ASan changes memory layout and timing.
- Custom allocators are not modeled correctly unless integrated.
- DMA or hardware writes can bypass compiler instrumentation.
- Inline assembly can access memory outside the sanitizer model.
- Stack/heap overflows that do not hit instrumented red zones may evade detection.

## Verification / debugging
Build sanitizer-enabled tests with debug symbols and high-quality stack traces. Reproduce failures with the smallest input. Run unit, integration, and fuzz tests under ASan. Fix the first reported memory error because later failures may be cascading consequences.

## Performance, memory, timing and power
ASan commonly increases memory consumption substantially and adds runtime overhead. It is therefore excellent for host CI and fuzzing but usually inappropriate for a production MCU image. The overhead is a feature during testing because it makes hidden memory errors observable.

## Staff-level takeaway
Use ASan as a **high-signal dynamic memory-safety net**. Apply it to the largest practical portion of the codebase, especially parser and buffer logic, while explicitly testing the hardware-specific boundaries it cannot observe.