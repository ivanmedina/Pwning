## Heap explotation guide
*****************************************
1.- House of Force ([link](https://github.com/ivanmedina/Pwning/tree/master/HEAP/HeapLAB/house_of_force)) 
- Overwrite top chunk to wrap until malloc_hook address with system function.

2.- Fastbin dup ([link](https://github.com/ivanmedina/Pwning/tree/master/HEAP/HeapLAB/fastbin_dup)) 
- Fastbin with use-after-free.
- Bypass fake chunk size.

3.-Fastbin dup challange ([link](https://github.com/ivanmedina/Pwning/tree/master/HEAP/HeapLAB/challenge-fastbin_dup)) 
- Crafting fake chunk with fastbins in main arena to exploit malloc_hook.
- Overwrite top chunk address in main arena so that when request it
we return to our fake chunk.
- Bypass check size of top chunk (GLibc 2.30).

4.- Unsafe unlink ([link](https://github.com/ivanmedina/Pwning/tree/master/HEAP/HeapLAB/unsafe_unlink)) 
- Request two chunks of same size.
- Overflow prev_inuse flag of chunk_B from chunk_A for indicating that previous chunk is candidate to consolidation.
- In this overflow we need also to set correctly the prev_size field of chunk A in chunk_B.
- The overflow must set valid values of FD and BK in chunk_A that indicate where we want to point. (shellcode)

5.- Safe unlink ([link](https://github.com/ivanmedina/Pwning/tree/master/HEAP/HeapLAB/safe_unlink)) 
- Request two chunks A and B, and leveraged an overflow bug to clear prev_inuse flag on the allocated chunk B.
- Prepare a fake chunk metadata in its previous chunk, chunk A, including a size field, forward pointer and backward pointer, and prev_size field.
- When we freed chunk B, its clear prev_inuse flag indicated to malloc that the previous chunk was free, therefore a candidate for consolidation.
- Malloc used our forged prev_size field to find the start of the previous chunk so it could unlink prior to consolidation.
- FD and BK checked that the BK at the destination pointed back to our fake chunk, and perform the same check to BK.
- Once our fake chunk passed the safe unlinking checks, malloc unlinked it. 
- It followed our FD and copied our BK over the BK at its destination. Then it followed our BK and copied our FD over the FD at its destination.

## References

Max Kamper, Linux Heap Exploitation - Part 1, Udemy