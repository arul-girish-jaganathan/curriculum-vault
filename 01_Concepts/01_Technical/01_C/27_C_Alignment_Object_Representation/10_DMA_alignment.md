# 10: DMA Alignment

## Definition
DMA (Direct Memory Access) alignment refers to the strict hardware memory address and size constraints imposed by DMA controllers on source and destination buffers. Because DMA controllers transfer data directly across the system bus without CPU intervention, buffers must meet exact hardware alignment requirements (typically 4-byte, 32-byte, or cache-line boundaries) to prevent transfer corruption or bus faults.

## Scope and Boundaries
- **Covers:** Peripheral DMA constraints, buffer alignment, cache coherence interaction, and scatter-gather lists.
- **Does not cover:** General CPU alignment ([[01_Alignment_requirements]]), dynamic memory allocation, or cache line optimizations ([[11_Cache_line_alignment]]).

## Why Does It Exist
DMA hardware operates independently of CPU memory management units:
- **Bus Width Requirements:** High-speed DMA engines (Ethernet MAC, USB PHY, SDMMC) require memory addresses to align with bus transfer widths (e.g., 32-bit or 64-bit words). Unaligned DMA addresses trigger hardware error interrupts or corrupted data transfers.
- **Cache Coherency Interaction:** If a DMA buffer resides in a cached memory region, CPU cache lines and physical RAM can fall out of sync, requiring explicit cache cleaning/invalidating around DMA transfers.

## Mechanism and Language Rules
- **Static Alignment:** Buffers destined for DMA must be declared using `alignas()` matching the peripheral controller requirement.
- **Heap Alignment:** Dynamic buffers for DMA must be allocated using aligned allocators (`aligned_alloc`), never standard `malloc` if standard `malloc` does not guarantee required peripheral alignment.

## Examples
```c
#include <stdio.h>
#include <stdalign.h>
#include <stdint.h>
#include <string.h>

#define DMA_BUFFER_SIZE 512
#define DMA_ALIGNMENT   32

/* Statically allocate a DMA-safe buffer aligned to 32 bytes */
alignas(32) static uint8_t dma_tx_buffer[DMA_BUFFER_SIZE];
alignas(32) static uint8_t dma_rx_buffer[DMA_BUFFER_SIZE];

void configure_dma_transfer(const uint8_t *src, size_t len) 
{
    if ((uintptr_t)src % DMA_ALIGNMENT != 0) {
        printf("Error: Source buffer is not DMA aligned!\n");
        return;
    }
    
    if (len > DMA_BUFFER_SIZE) {
        printf("Error: Transfer size exceeds buffer capacity.\n");
        return;
    }

    memcpy(dma_tx_buffer, src, len);
    printf("DMA buffers verified and prepared for transfer.\n");
}

int main(void) 
{
    alignas(32) uint8_t sample_data[64] = "Hello DMA Hardware!";
    configure_dma_transfer(sample_data, sizeof(sample_data));
    return 0;
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Hardware Bus Fault:** Passing an unaligned buffer pointer to a DMA controller register causes hardware bus faults, silent data corruption, or peripheral lockup.

## Edge Cases and Failure Modes
- **Stack-Allocated DMA Buffers:** Passing automatic stack variables to DMA controllers is extremely dangerous because stack frames can be misaligned or overwritten by concurrent function calls during active DMA transfers.
- **Cache Coherency Mismatch:** CPU modifies a cached variable, but DMA reads stale data directly from RAM because the cache line was not flushed.

## Embedded Implications
- **Cortex-M / RISC-V DMA:** On ARM Cortex-M microcontrollers, DMA buffers must often reside in non-cached SRAM regions (e.g., SRAM1/SRAM2) or require explicit CMSIS cache maintenance functions (`SCB_CleanDCache_by_Addr`, `SCB_InvalidateDCache_by_Addr`).

## Firmware Review Angle
- **Audit DMA Buffer Declarations:** Verify that all buffers passed to DMA peripherals are statically over-aligned using `alignas()` or allocated via aligned heap allocators.
- **Check Cache Maintenance:** Ensure proper cache cleaning/invalidating operations surround all active DMA operations in cached architectures (Cortex-A/R).

## Compiler, ABI, and Toolchain Implications
- **Linker Sections:** DMA buffers are often placed in specialized linker sections (`.dma_buffer`) mapped to specific physical memory banks.

## Performance, Memory, Timing, and Power
- **Zero CPU Load:** Properly aligned DMA transfers offload data movement entirely from the CPU to dedicated hardware DMA channels, maximizing power efficiency and throughput.

## Verification / Debugging
- **Debugger Memory Inspector:** Verify buffer addresses in GDB before initiating DMA transactions to ensure lower bits are zero (`addr % alignment == 0`).

## Safety, Security, and Reliability
- **Reliability:** DMA alignment errors are among the most pernicious intermittent bugs in embedded firmware, causing silent data corruption under heavy network/storage loads.

## Trade-offs and Alternatives
- **CPU Polled I/O vs. DMA:** CPU polled I/O requires zero alignment constraints but consumes 100% CPU cycles and stalls execution; DMA requires strict alignment and cache management but delivers maximum throughput.

## Staff-Level Takeaway
DMA alignment is an absolute hardware mandate. Never assume standard `malloc` or stack arrays meet peripheral DMA alignment rules. Always enforce static over-alignment (`alignas`) or use dedicated aligned allocation pools for all DMA transactions.

## Related Concepts
- [[00_Chapter_Index]]
- [[01_Alignment_requirements]]
- [[03_Alignas]]
- [[11_Cache_line_alignment]]
