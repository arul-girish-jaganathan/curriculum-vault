# 12: DMA Friendly Array Layouts

## Definition
A DMA-friendly array layout is a contiguous memory buffer engineered to satisfy hardware Direct Memory Access (DMA) engine constraints: strict address alignment, cache-line boundary synchronization, absence of compiler-injected padding, and dedicated memory bus section placement.

## Scope and Boundaries
*   **Covers:** Cache-line alignment, MPU attribute configuration for DMA buffers, hardware FIFO pitch/stride, non-cacheable RAM regions, and cache clean/invalidate operations.
*   **Does not cover:** General DMA controller programming, interrupt handling (see [[Interrupt Handling and ISRs]]), or general memory alignment (see [[Memory Alignment and Padding]]).

## Why Does It Exist
DMA controllers bypass the CPU core to read/write memory directly across internal system buses:
*   **Cache Coherency Hazards:** If an array shares a cache line with unrelated variables, CPU cache flushes will overwrite freshly written DMA data, or CPU cache dirty write-backs will corrupt DMA transfers.
*   **Hardware Alignment Demands:** High-speed DMA engines require 4-byte, 8-byte, or 32-byte (cache-line) aligned base addresses.
*   **Bus Master Accessibility:** DMA engines often cannot access tightly-coupled CPU memories (like ARM Cortex-M ITCM or DTCM); buffers must be allocated in general AXI/AHB SRAM.

## Mechanism and Language Rules
1.  **Cache Line Alignment:** DMA buffers must be aligned to the processor's L1 data cache line size (typically 32 bytes on Cortex-M7, 64 bytes on Cortex-A):
    ```c
    __attribute__((aligned(32))) static uint8_t dma_rx_buffer[256];
    ```
2.  **Cache Line Size Multiples:** The total byte size of a DMA buffer must be rounded up to an integer multiple of the cache line size to prevent false sharing within trailing cache lines.
3.  **Section Placement:** Placing arrays into DMA-accessible SRAM sections via linker attributes:
    ```c
    __attribute__((section(".dma_ram"), aligned(32))) static uint32_t adc_buffer[1024];
    ```
4.  **Cache Maintenance Synchronization:**
    *   *Transmit (Memory -> Peripheral):* CPU cleans/flushes data cache (`SCB_CleanDCache_by_Addr`) before DMA start, pushing CPU writes to physical RAM.
    *   *Receive (Peripheral -> Memory):* CPU invalidates data cache (`SCB_InvalidateDCache_by_Addr`) before reading DMA data, forcing reads from physical RAM.

## Examples

```c
/* Keep examples minimal: prove the rule before embedding it in a larger API. */
#include <stdint.h>
#include <stddef.h>

#define CACHE_LINE_SIZE 32U
#define BUFFER_SIZE     128U

/* Round up buffer size to multiple of cache line size */
#define DMA_BUFFER_ALLOC_SIZE     (((BUFFER_SIZE + CACHE_LINE_SIZE - 1U) / CACHE_LINE_SIZE) * CACHE_LINE_SIZE)

/* Correct: Aligned to cache line and placed in dedicated DMA section */
#if defined(__GNUC__)
__attribute__((aligned(CACHE_LINE_SIZE), section(".dma_buffers")))
#endif
static uint8_t g_dma_spi_rx[DMA_BUFFER_ALLOC_SIZE];

static void* get_dma_buffer_address(void)
{
    return (void *)g_dma_spi_rx;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
*   **Hardware Faults / Undefined Behavior:** Configuring a DMA transfer using a local stack-allocated array that goes out of scope before the transfer finishes. Dereferencing unaligned addresses on DMA engines lacking unaligned burst capabilities.
*   **Implementation-Defined:** Microcontroller memory bus interconnect matrix topology (which SRAM banks are mastered by which DMA streams).

## Edge Cases and Failure Modes
*   **False Sharing Cache Corruption (CRITICAL):** If `dma_rx_buffer[60]` occupies a 64-byte cache line, and the remaining 4 bytes of that line hold a regular variable `flags`: when the CPU writes to `flags`, it writes back the entire dirty 64-byte line, obliterating the newly arrived DMA data in `dma_rx_buffer`!
*   **Stack Allocation Trap:** Never place DMA buffers on the function stack. Stacks are not cache-line aligned and can be reclaimed by subsequent function calls while the DMA is actively transferring data.

## Embedded Implications
*   **Cortex-M7 Cache Maintenance:** Systems running ARM Cortex-M7 (e.g., STM32F7/H7) feature L1 D-Cache with write-back policy. Omitting cache clean/invalidate steps causes communication packets to read stale memory or transfer old data.
*   **MPU Non-Cacheable Regions:** To eliminate cache maintenance software overhead, robust architectures configure the MPU to mark the `.dma_buffers` RAM section as **Non-Cacheable** (Normal, Non-Cacheable, or Shared).

## Firmware Review Angle
1.  **Alignment Audit:** Ensure every DMA buffer is declared with explicit `aligned(N)` attributes matching the cache line size.
2.  **No Stack Buffers:** Verify that no pointer passed to a DMA controller points to automatic (stack) memory.
3.  **Allocation Size Rounding:** Check that buffer sizes are integer multiples of the cache line size to eliminate trailing-byte false sharing.
4.  **MPU / Cache Invalidation:** Verify that DMA receive channels invoke cache invalidation prior to parsing buffer payloads.

## Compiler, ABI, and Toolchain Implications
*   **Section Attributes:** The compiler flags arrays with section attributes, allowing linker scripts to place them into distinct physical memory blocks (e.g., SRAM1 vs. DTCM).
*   **Linker Script Alignment:** Linker scripts must align the start and end of DMA sections to cache-line boundaries:
    ```ld
    .dma_section (NOLOAD) : ALIGN(32) {
        *(.dma_buffers)
        . = ALIGN(32);
    } > RAM_D2
    ```

## Performance, Memory, Timing, and Power
*   **Zero CPU Load:** Once configured, DMA transfers run in parallel with the CPU, freeing 90%+ of CPU cycles for application processing.
*   **Bus Contention:** High-speed DMA bursts create bus contention on internal crossbar switches, adding occasional single-cycle arbitration latency to CPU SRAM fetches.

## Verification / Debugging
*   **JTAG Memory Inspection:** Inspect physical RAM directly via debugger memory windows to bypass the CPU cache and verify raw DMA writes.
*   **Hardware Watchpoints:** Place watchpoints on the memory region to detect CPU writes occurring during active DMA transfers.

## Safety, Security, and Reliability
*   **MISRA C:2012 Compliance:**
    *   *Rule 11.4:* Conversion between a pointer and an integer type (requires deviation for programming physical DMA register base addresses).
*   **Security Vulnerabilities:**
    *   DMA buffer overflows overwrite adjacent peripheral registers or kernel data, bypassing software memory protections.

## Trade-offs and Alternatives
*   **Cached RAM with Maintenance vs. Non-Cacheable RAM:**
    *   *Cached RAM:* High CPU read speed; requires manual cache invalidation/clean routines; prone to coherency bugs.
    *   *Non-Cacheable RAM (via MPU):* 100% immune to coherency bugs; zero maintenance cycle overhead; CPU reads/writes are slightly slower (uncached).
    *   *Staff Recommendation:* Use Non-Cacheable MPU regions for circular DMA ring buffers.

## Staff-Level Takeaway
DMA buffer engineering is a hardware-software boundary discipline. Staff engineers must mandate three non-negotiable rules for DMA arrays: declare buffers in dedicated non-cacheable MPU memory sections or align both size and base address to hardware cache-line boundaries, strictly forbid stack-allocated DMA buffers, and enforce buffer size rounding to prevent cache false sharing corruption.

## Related Concepts
*   [[01_Array_declaration]]
*   [[10_sizeof_arrays]]
*   [[11_Array_bounds_and_safety]]
*   [[Memory Alignment and Padding]]
*   [[Linker Scripts and Memory Sections]]

---
*Related: [[00_Chapter_Index]], [[../00_Complete_Topic_Map]]*
