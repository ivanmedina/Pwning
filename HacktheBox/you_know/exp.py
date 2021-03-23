#!/usr/bin/python3
from pwn import *
context.log_level='debug'
#context.terminal = ["terminator", "-e"]
#context.terminal = ["tmux", "splitw", "-h"]
#context.terminal = ['terminator', '--tew-tab', '-x']

import time
import struct
elf = context.binary = ELF("./vuln")
libc = elf.libc
# =============================================================================
gs = '''
continue
'''
# =============================================================================
def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)

exp=""

# =============================================================================
io = start()
g = cyclic_gen()
#io.sendafter(" \n", "A"*200)
io.interactive()
