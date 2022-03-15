#! /usr/bin/python3
from pwn import *

host = '<IP>'
puerto = 1234

binary_name = './BINARY'
context.binary = binary_name
context.log_level = "debug"
binary = context.binary

if(args['REMOTO']):
    p = remote(host, puerto)
else:
    p = process(["./ld-linux-x86-64.so.2", "./<BINARY>"], env={"LD_PRELOAD":"./libc.so.6"})

if(args['GDB']):
    base = p.libs()[binary.path]
    comandos_gdb = ""
    comandos_gdb += "br *" + hex(0x401757) + "\n"
    comandos_gdb += "continue\n"
    gdb.attach(p, comandos_gdb)