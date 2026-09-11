# Object Code Generation

Object-code generation maps the compiler's internal representation to target instructions and data representations while preserving the semantics required by the selected C implementation and target environment.

## What is generated
Typical output includes machine instructions, constant data, relocation records, symbol information and sections that later participate in linking. The exact object format and instruction selection are toolchain and target dependent.

## Optimization
Register allocation, instruction selection, constant propagation, inlining, dead-code elimination and other transformations can substantially change the binary while preserving required behavior. Optimization is allowed to exploit the assumptions made by the language contract; undefined behavior can therefore produce surprising transformations.

## Embedded concerns
Code generation affects flash size, RAM use, execution time, interrupt latency, stack usage and power. A source-level micro-optimization is meaningless until its generated code and system-level effect are measured.

## Volatile and hardware
Accesses to volatile-qualified objects have language-level requirements concerning observable accesses, but volatile is not a universal cache, synchronization or memory-barrier mechanism. MMIO correctness depends on the compiler, CPU memory system and peripheral specification together.

## Verification
Use compiler-generated assembly, object dumps and map files to answer “what actually shipped?” Keep source semantics as the primary correctness argument; assembly inspection is evidence about a particular compiler/target configuration.

## Staff-level view
Treat generated code as a measurable artifact with budgets: text size, data size, cycles, stack and latency. Make those budgets part of regression testing when performance or resource margins are product requirements.

## Related
- [[07_Assembly_inspection]]
- [[08_Compiler_driver_stages]]
- [[11_LTO_and_whole_program_optimization]]
- [[37_C_Compiler_Optimization]]
