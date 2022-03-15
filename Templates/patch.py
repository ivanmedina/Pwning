from pwn import *

elf=ELF('./bin')
# for key, address in elf.symbols.iteritems():
#     print(key, hex(address))
elf.asm( elf.symbols['alarm'], 'ret')
elf.save('./bin_patch')