# Searching and sorting

## Definition
The C standard library provides generic array algorithms `bsearch` and `qsort` in `<stdlib.h>`. Both operate on arbitrary objects through `void *` and element sizes, using a caller-supplied comparison function. `bsearch` searches an already sorted array and returns a pointer to a matching element or `NULL`; `qsort` rearranges an array into an order defined by the comparison function.

## Scope and Boundaries
* **Covers:** `qsort`, `bsearch`, comparator contracts, element size/count, ordering, stability, and embedded cost.
* **Does not cover:** implementation-specific sorting algorithms or tree/hash data structures.

## Why Does It Exist
C has no built-in generic container algorithm mechanism. `qsort` and `bsearch` provide reusable operations over arbitrary object arrays without requiring one library implementation for every element type.

## Mechanism and language rules
The array is described by a base pointer, element count, and element size. The comparator receives pointers to two elements and must return a negative, zero, or positive result according to their relative order. It must impose a consistent ordering compatible with the algorithm's requirements.

`qsort` does not guarantee stability: equal keys may change relative order. `bsearch` requires the searched array to be sorted according to the same comparison relationship; otherwise its result is not meaningful. The returned pointer from `bsearch`, when non-null, points into the original array and becomes invalid if that array's lifetime ends or it is moved/reallocated.

### What to reason about
- The comparator arguments point to elements, not necessarily to the application's semantic key type; cast them correctly.
- Never implement integer comparison as `return a - b;` when overflow is possible.
- Comparator consistency matters: contradictory results can break algorithm assumptions.
- `qsort` may invoke the comparator many times, so comparator cost can dominate runtime.
- `bsearch` is logarithmic in comparisons for typical implementations, but the standard specifies behavior rather than promising a particular complexity contract.
- Element size and count must describe the actual array; overflow in `count * size` can invalidate surrounding size assumptions.

## Embedded implications
Generic library sorting can consume code space and execute with nontrivial stack and comparator-call overhead. Function-pointer calls can inhibit inlining and increase worst-case timing. For small fixed arrays, insertion sort or a hand-specialized sort can be smaller, faster, and easier to bound.

### Firmware review angle
Ask whether sorting is allowed in a real-time path, whether the comparator is deterministic, and what maximum array size is possible. If data belongs to an ISR/shared buffer, establish synchronization before sorting because `qsort` mutates the array.

## Edge cases and failure modes
- `return *(const int *)a - *(const int *)b;` can overflow and violate the comparator contract.
- Sorting pointers by subtraction is not generally valid unless the pointers are elements of the same array and the intended ordering is appropriate; pointer ordering semantics are narrower than integer ordering.
- A comparator that changes global state or depends on mutable external state can return inconsistent results.
- `bsearch` on an array sorted with a different key or comparator can fail even when the target value appears present.
- Passing a wrong element size makes the library step through the array incorrectly, leading to invalid memory access.

## Example pattern
```c
#include <stdlib.h>

static int compare_u32(const void *lhs, const void *rhs)
{
    unsigned int a = *(const unsigned int *)lhs;
    unsigned int b = *(const unsigned int *)rhs;
    return (a > b) - (a < b);
}

static void sort_ids(unsigned int *ids, size_t count)
{
    qsort(ids, count, sizeof ids[0], compare_u32);
}
```

## Verification / debugging
Unit-test empty, one-element, duplicate, already sorted, reverse-sorted, maximum-value, and large-count cases. Verify comparator antisymmetry and transitivity with property-based tests. Benchmark comparator cost separately from algorithm overhead, and inspect stack usage on the target.

## Staff-level takeaway
Generic search/sort APIs trade type safety and specialization for reuse. A Staff engineer should verify the comparator as a mathematical ordering contract, bound the data size and execution time, and choose a specialized algorithm when deterministic firmware behavior matters more than genericity.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
[[13_C_Pointers/05_void_pointers]]
[[50_C_Performance/00_Chapter_Index]]
