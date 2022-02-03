## Fastbin with Use-After-Free
*****************************************
1.- Request two 0x50 size chunk
```
chunk_A = malloc(24, b"A"*24)
chunk_B = malloc(24, b"B"*24)
```
![imagen1.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/fastbin_dup/assets/Imagen1.png)

2.- Free chunk A
```
free(chunk_A)
```
![imagen2.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/fastbin_dup/assets/Imagen2.png)

3.- Free chunk B
```
free(chunk_B)
```
![imagen3.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/fastbin_dup/assets/Imagen3.png)

4.- Free chunk A
```
free(chunk_A)
```
![imagen4.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/fastbin_dup/assets/Imagen4.png)

5.- malloc(24,b'C'*24)
```
malloc(24,b'C'*24)
```
![imagen5.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/fastbin_dup/assets/Imagen5.png)

6.- There are the CCCCCCC… where before was the 7020 pointer :O, so where will do now the Ds malloc?
```
malloc(24,b'D'*24)
```
![imagen6.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/fastbin_dup/assets/Imagen6.png)

7.- Yes, in the next chunk linked in the 0x20 fastbin list...
So now we will send some EEEE's
```
malloc(24,b'E'*24)
```
![imagen7.png](https://raw.githubusercontent.com/ivanmedina/Pwning/master/HEAP/HeapLAB/fastbin_dup/assets/Imagen7.png)

And now we can note that we controll where the next 0x20 fastbin will be allocated.

## References

Max Kamper, Linux Heap Exploitation - Part 1, Udemy 3(9-11)