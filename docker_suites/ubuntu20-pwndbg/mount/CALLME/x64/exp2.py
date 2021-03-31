from pwn import *
binf = ELF("callme")
libc = "libcallme.so"
#p = remote("chall.ctf.bamboofox.tw", 10102)
p=process('callme')
context.terminal = ["tmux", "splitw", "-h"]
gs = '''
break *0x400882
'''

def start():
    if args.GDB:
        return gdb.debug(binf.path, gdbscript=gs)
    else:
        return process(binf.path)


context.log_level = "DEBUG"

print(binf.plt)

p=start()
#pause()

p.sendafter("> ", 'A'*1000)


p.interactive()
