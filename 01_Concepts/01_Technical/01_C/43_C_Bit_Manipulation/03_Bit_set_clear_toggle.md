# Bit set clear toggle

> Canonical C topic note — Chapter 43. Setting, clearing, and toggling individual bits are common low-level operations, but the safe implementation depends on type width and whether the storage is ordinary memory or a hardware register.

## Definition
For a value `x` and mask `m`: set uses `x | m`, clear uses `x & ~m`, and toggle uses `x ^ m`. Test uses `(x & m) != 0`.

## Mechanism and language rules
Use unsigned values for bit manipulation. Because `~` applies after integer promotion, a clear operation can accidentally affect bits outside a narrow intended field unless the value is explicitly converted/masked to the correct width.

### What to reason about
- Is the mask one bit or a field mask?
- What type does integer promotion produce?
- Is the operation performed on RAM, an atomic object, or MMIO?
- Can another execution context update the same word?
- Does the hardware provide atomic set/clear operations?

For ordinary shared memory, a read-modify-write sequence is not automatically atomic merely because each C expression looks small.

## Embedded implications
GPIO flags, status words, permission bits, and peripheral registers commonly use these operations. For MMIO, a generic `reg = reg | mask` may be wrong for write-one-to-clear, write-one-to-set, command, or read-sensitive registers.

### Firmware review angle
Provide semantic helpers such as `set_bits`, `clear_bits`, and `test_bits` only when their hardware meaning is known. Prefer peripheral-provided atomic aliases where available.

## Edge cases and failure modes
- `~mask` changes unintended high bits.
- Concurrent read-modify-write loses another writer's update.
- Toggle is not idempotent and repeated execution changes state again.
- Register access semantics make read-modify-write invalid.

## Example pattern
```c
uint32_t set_bit(uint32_t value, unsigned bit)
{
    return value | (UINT32_C(1) << bit);
}

uint32_t clear_bit(uint32_t value, unsigned bit)
{
    return value & ~(UINT32_C(1) << bit);
}
```
The caller must guarantee `bit < 32`.

## Verification / debugging
Test bit 0, the highest valid bit, adjacent bits, and invalid positions. For shared state, test interrupt/task races. For registers, verify access semantics against the reference manual and inspect bus transactions if necessary.

Staff-level questions: Is this operation atomic for every writer? Is toggle safe to retry? Does the mask encode only the owned field?

## Staff-level takeaway
Bit operations are safe when **width, ownership, atomicity, and hardware semantics** are explicit. Never assume a read-modify-write is universally safe at a hardware boundary.

## Related
[[00_Chapter_Index]]
[[../00_Complete_Topic_Map]]
