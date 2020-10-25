#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("callme")
libc = elf.libc

gs = '''
continue
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)


# =============================================================================

io = start()

# =============================================================================


# =============================================================================

io.interactive()
