# Source Backbone

The knowledge base is a structured, paraphrased study framework. It is not a verbatim reproduction of any single source.

## Primary technical references
- GDB documentation: https://sourceware.org/gdb/documentation/
- GNU Debugger manual: https://sourceware.org/gdb/current/onlinedocs/gdb/
- LLVM LLDB documentation: https://lldb.llvm.org/
- DWARF standard resources: https://dwarfstd.org/
- Valgrind documentation: https://valgrind.org/docs/manual/
- AddressSanitizer documentation: https://clang.llvm.org/docs/AddressSanitizer.html
- UndefinedBehaviorSanitizer documentation: https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html
- ThreadSanitizer documentation: https://clang.llvm.org/docs/ThreadSanitizer.html
- MemorySanitizer documentation: https://clang.llvm.org/docs/MemorySanitizer.html
- Linux kernel debugging documentation: https://docs.kernel.org/dev-tools/
- Linux tracing documentation: https://docs.kernel.org/trace/index.html
- perf documentation: https://perf.wiki.kernel.org/
- ftrace documentation: https://docs.kernel.org/trace/ftrace.html
- bpftrace documentation: https://bpftrace.org/
- OpenOCD documentation: https://openocd.org/doc-release/html/
- Arm Cortex-M debugging resources: https://developer.arm.com/documentation
- Arm CoreSight documentation: https://developer.arm.com/architectures/system-architectures/CoreSight
- FreeRTOS kernel documentation: https://www.freertos.org/
- Zephyr documentation: https://docs.zephyrproject.org/

## Coverage philosophy
Use official tool documentation for commands and semantics, kernel/architecture documentation for platform-specific behavior, and practical experiments to validate assumptions on the target.
