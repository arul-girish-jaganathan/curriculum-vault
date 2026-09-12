# 11: DMA Descriptors

## Definition
DMA descriptors are hardware-defined data structures residing in system memory that configure direct memory access (DMA) transfers, scatter-gather lists, and ring buffers. Because DMA controllers read these descriptors asynchronously via the system bus, their layout, alignment, and endianness must match hardware specifications exactly.

## Scope and Boundaries
- **Covers:** Hardware descriptor rings, scatter-gather DMA, ring buffer pointers, and cache synchronization for descriptors.
- **Does not cover:** General buffer alignment ([[../27_C_Alignment_Object_Representation/10_DMA_alignment]]) or socket serialization.

## Why Does It Exist
Advanced peripherals (Ethernet MACs, USB controllers, FPGA interfaces) manage high-throughput packet transfers using descriptor rings:
- **Scatter-Gather Operations:** Allowing DMA controllers to read or write non-contiguous memory blocks by chaining descriptor pointers.
- **Asynchronous Processing:** Hardware updates descriptor status fields (e.g., transfer complete, error flags) asynchronously, requiring volatile memory semantics and atomic synchronization.

## Mechanism and Language Rules
- **Exact Hardware Layout:** DMA descriptors are typically defined using packed structures or explicit byte offsets to match hardware register maps.
- **Volatile Qualifiers:** Pointers and status fields within descriptor structures must be marked `volatile` to prevent compilers from caching values in CPU registers across asynchronous hardware updates.

## Examples
```c
#include <stdint.h>
#include <stdalign.h>

#define DESCRIPTOR_ALIGNMENT 32

/* Hardware Ethernet / Peripheral DMA Descriptor */
typedef struct alignas(DESCRIPTOR_ALIGNMENT) {
    volatile uint32_t status_control;
    uint32_t          buffer_addr;
    uint32_t          buffer_size;
    uint32_t          next_descriptor_addr;
} dma_descriptor_t;

static dma_descriptor_t tx_ring_buffer[4];

void init_dma_ring(void) 
{
    for (int i = 0; i < 4; ++i) {
        tx_ring_buffer[i].status_control = 0;
        tx_ring_buffer[i].buffer_addr = 0;
        tx_ring_buffer[i].buffer_size = 512;
        tx_ring_buffer[i].next_descriptor_addr = (uint32_t)(uintptr_t)&tx_ring_buffer[(i + 1) % 4];
    }
}
```

## Undefined, Unspecified, and Implementation-Defined Behavior
- **Undefined Behavior:** Failing to use `volatile` on DMA descriptor fields updated asynchronously by hardware controllers leads to race conditions and compiler optimization bugs.

## Edge Cases and Failure Modes
- **Cache Coherency Mismatch:** CPU writes descriptor updates to cache, but DMA controller reads stale data directly from physical RAM because cache lines were not flushed.

## Embedded Implications
- **Bare-Metal Drivers:** Writing Ethernet MAC or USB driver rings requires meticulous attention to descriptor struct alignment (`alignas`), padding, and cache maintenance.

## Firmware Review Angle
- **Audit Volatile & Alignment:** Verify that all hardware DMA descriptor structures are strictly aligned and all status/control fields are marked `volatile`.

## Compiler, ABI, and Toolchain Implications
- **Memory Barriers:** Updating DMA descriptor chains requires explicit memory barrier instructions (`__DMB()` on ARM) to ensure store ordering is visible to hardware controllers.

## Performance, Memory, Timing, and Power
- **Zero-Copy Networking:** Scatter-gather DMA descriptors enable zero-copy packet forwarding across high-speed network interfaces.

## Verification / Debugging
- **Hardware Debugger Inspection:** Use JTAG to inspect DMA ring pointer linked lists and verify that hardware status registers update correctly.

## Safety, Security, and Reliability
- **Ring Corruption Prevention:** Strict boundary checking on descriptor ring pointers prevents buffer overflows and wild memory writes by misconfigured DMA engines.

## Trade-offs and Alternatives
- **Descriptor Rings vs. Single Buffers:** Descriptor rings enable continuous, zero-overhead streaming and scatter-gather multiplexing at the cost of increased driver complexity.

## Staff-Level Takeaway
DMA descriptors are physical hardware interfaces mapped into software data structures. Treat them with absolute rigor: enforce strict alignment (`alignas`), mark asynchronous status fields `volatile`, and manage cache coherency explicitly.

## Related Concepts
- [[00_Chapter_Index]]
- [[../27_C_Alignment_Object_Representation/10_DMA_alignment]]
- [[../27_C_Alignment_Object_Representation/12_ABI_and_packing]]
