# Static linkage

> Canonical C topic note — chapter 36.

## Definition
`static` at file scope gives an object or function **internal linkage**. The identifier is still visible according to its lexical scope, but the entity cannot be referred to by that identifier from another translation unit. This is a C language property; the exact local-symbol representation is an object-format/toolchain detail.

`static` also has a different meaning for block-scope objects: it gives static storage duration, not internal linkage. These meanings must be kept separate.

## Mechanism and language rules
```c
/* module.c */
static unsigned retry_count;
static void recover(void) { /* private implementation */ }
```

Another translation unit may contain an unrelated `static unsigned retry_count;`; the two objects are distinct even though their identifiers have the same spelling.

At file scope:

- `static` object/function declaration → internal linkage.
- no `static` on an ordinary file-scope function → external linkage by default.
- file-scope `const` has special C linkage rules and should be reviewed separately rather than importing C++ intuition.

At block scope:

```c
void sample(void)
{
    static unsigned calls;
    ++calls;
}
```

`calls` retains its value for the lifetime of the program (more precisely, static storage duration) but its name is only usable within the block. Its initialization occurs once before program startup is complete for the abstract C execution model; the exact startup mechanism is implementation-specific.

Internal linkage does not mean “optimized away,” “read-only,” or “thread-safe.” A static object can be mutable, can occupy RAM, and can participate in races if accessed concurrently without synchronization.

## Embedded implications
Internal linkage is one of the simplest architectural controls in embedded C. It limits accidental coupling between drivers and applications, makes ownership obvious, and can enable whole-program optimization.

Benefits include:

- reduced symbol namespace pollution;
- stronger module boundaries;
- fewer accidental cross-module dependencies;
- easier dead-code elimination and optimization;
- clearer ownership of state and helper functions.

But `static` does not itself eliminate RAM usage. A file-scope `static` buffer is still allocated unless optimization/linker garbage collection can remove it. A block-scope static buffer may also create persistent RAM pressure.

### Firmware review angle
Prefer private state and helpers to be `static` unless an intentional public interface requires external linkage. Inspect the map file to see whether private data is placed in the expected RAM section. Be careful with `static` state in reusable drivers: if the design requires multiple device instances, hidden singleton state may prevent reentrancy and instance scaling.

## Edge cases and failure modes
A common mistake is believing that putting `static` in a header creates one shared object. It does not. Every translation unit that includes a header containing a file-scope `static` definition gets its own entity. This can silently create duplicated state.

Likewise:

```c
/* bad public header for shared state */
static int debug_enabled;
```

Each source file sees a separate `debug_enabled`.

Use `static` declarations in headers mainly for carefully designed internal inline definitions or constants where duplication is intentional and appropriate, not as a substitute for `extern` when shared state is required.

A static function can have its address taken and passed as a callback; internal linkage remains a linker/module property and does not make function pointers inherently unsafe.

## Example pattern
```c
/* driver.c */
static uint8_t rx_buffer[128];
static size_t rx_used;

void driver_reset(void)
{
    rx_used = 0;
}
```

Only the intended API crosses the translation-unit boundary.

## Verification / debugging
Use compiler warnings such as unused-function/unused-variable diagnostics, inspect the object symbol table, and inspect the linker map. A useful architectural test is to search for every non-static file-scope function/object and justify its external visibility.

Staff-level questions:
- Is external linkage actually required?
- Is this state intentionally singleton?
- Would an opaque context object be better than hidden static state?
- Does a header accidentally instantiate private state in every translation unit?
- Does the binary show unexpected duplicated buffers or code?

## Staff-level takeaway
Use file-scope `static` as a **module-boundary primitive**. It encodes ownership directly in the language, reduces coupling, and makes interfaces auditable. Do not confuse linkage with storage duration, concurrency, or optimization.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
