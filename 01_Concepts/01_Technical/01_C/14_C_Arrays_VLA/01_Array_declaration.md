# 01: Array Declaration

## Definition
An array declaration introduces an identifier whose type is an array of a specified element type and fixed extent (number of elements). In ISO C (C99 §6.7.5.2), an array type is constructed from a contiguous sequence of objects of a single complete object type.

## Scope and Boundaries
*   **Covers:** Fixed-extent array syntax, element type restrictions, constant expression dimension requirements, and storage allocation semantics.
*   **Does not cover:** Array initialization syntax (see [[02_Array_initialization]]), Variable Length Arrays (see [[09_Variable_length_arrays]]), Flexible Array Members (see [[08_Flexible_array_members]]), or pointer conversions (see [[03_Array_to_pointer_decay]]).

## Why Does It Exist
Arrays provide homogeneous contiguous indexing:
*   **Locality of Reference:** Placing identical data elements back-to-back in physical memory maximizes cache line utilization.
*   **Constant-Time Indexing:** Accessing any element via simple base-plus-offset calculation ($O(1)$).
*   **Hardware Mapping:** Direct representation of linear memory blocks, hardware buffers, and packet payloads.

## Mechanism and Language Rules
1.  **Syntax:** `type-specifier identifier[constant-expression(opt)];`.
2.  **Element Completeness:** The element type must be a complete object type. An array of `void`, an array of functions, or an array of incomplete structures is a constraint violation.
3.  **Dimension Constraints:** In file-scope (static) declarations, the size expression must be an integer constant expression greater than zero. Zero-length arrays (`int arr[0];`) violate ISO C constraints.
4.  **Contiguous Layout:** Elements are positioned contiguously in increasing memory addresses with zero padding between elements. The total size is guaranteed to be `N * sizeof(ElementType)`.
5.  **No Assignment:** Array types are non-modifiable lvalues; they cannot appear as the left operand of an assignment operator (`arr1 = arr2;` is illegal).

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>

#define BUFFER_CAPACITY 64U

/* Correct: File-scope fixed-size array declaration */
static uint32_t g_telemetry_buffer[BUFFER_CAPACITY];

/* Correct: Block-scope automatic array */
static void example_declaration(void)
{
    uint8_t scratchpad[16];
    scratchpad[0] = 0xAA;
    (void)scratchpad;
}

/* Incorrect: Constraint violation examples */
/* void invalid_void_arr[10]; */   /* Error: array of incomplete type 'void' */
/* int invalid_zero_len[0];   */   /* Error: zero size array in standard ISO C */
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Constraint Violation:** Declaring an array of functions, incomplete types, or negative/zero size (in standard ISO C).
*   **Compiler Extension:** GCC/Clang support zero-length arrays (`type arr[0];`) as a GNU extension for flexible structures. C99 standardized this as flexible array members (`type arr[];`).
*   **Implementation-Defined:** Maximum size limit for an array object (`PTRDIFF_MAX` or physical RAM limits).

## Edge Cases and Failure Modes
*   **Zero-Length Extension Portability:** Relying on `arr[0]` breaks across non-GNU compilers; use standard flexible array member syntax (`arr[]`).
*   **Massive Stack Allocations:** Declaring huge automatic arrays (`uint8_t buffer[65536];`) inside a function on a microcontroller immediately triggers a stack overflow.

## Embedded Implications
*   **Linker Section Mapping:** Arrays are placed in specific hardware memory sections (e.g., CCM RAM, DTCM, or external SDRAM) via compiler attributes:
    ```c
    __attribute__((section(".dtcm_ram"))) static uint32_t adc_dma_buffer[1024];
    ```
*   **ROM Placement:** Marking an array `const` places it into Flash/ROM (`.rodata`), saving RAM.

## Firmware Review Angle
1.  **Stack Size Audit:** Ensure local stack-allocated arrays do not exceed the thread's stack budget. Large buffers must be `static` or dynamic.
2.  **No Magic Numbers:** Verify that array extents are declared using explicit `#define` constants or enumerations, never bare numbers.
3.  **Banned Zero-Length Arrays:** Flag legacy `arr[0]` declarations and modernize to C99 flexible array members.

## Compiler, ABI, and Toolchain Implications
*   **Stack Alignment:** Compilers align local arrays to architecture word or cache-line boundaries (e.g., 4, 8, or 64 bytes).
*   **Stack Canaries:** When local arrays are declared, compilers with `-fstack-protector` insert canaries to detect boundary overruns.

## Performance, Memory, Timing, and Power
*   **Deterministic Fetch:** Direct contiguous arrays allow single-cycle register-indexed memory loads (`LDR r0, [r1, r2, LSL #2]`).
*   **Cache Locality:** Contiguous layout minimizes CPU cache misses and maximizes hardware prefetch efficiency.

## Verification / Debugging
*   **Compiler Diagnostics:** Use `-Wvla` to ensure no unintended variable-length arrays are generated.
*   **Map File Inspection:** Inspect linker `.map` files to verify physical location and footprint of declared arrays in RAM/Flash.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 18.7:* Flexible array members shall not be declared.
    *   *Rule 18.8:* Variable-length arrays shall not be used.
*   **Security Vulnerabilities:** Stack-based array overruns overwrite return addresses, enabling arbitrary code execution.

## Trade-offs and Alternatives
*   **Static Extent vs. Dynamic Allocation:** Fixed-size arrays guarantee deterministic allocation and zero heap fragmentation, at the cost of static memory reservation.

## Staff-Level Takeaway
Array declarations enforce contiguous physical layout. Staff engineers must ensure array dimensions are bounded, statically sized via symbolic constants, and that large buffers are allocated in static/global storage or dedicated linker sections rather than the thread stack frame.

## Related Concepts
*   [[02_Array_initialization]]
*   [[03_Array_to_pointer_decay]]
*   [[10_sizeof_arrays]]
*   [[Linker Scripts and Memory Sections]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
