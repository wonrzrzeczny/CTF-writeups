from nclib import *
import base64
from math import *


# Took from SO
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m


HOSTNAME = "18.179.251.168"
PORT = 21700

def saferecv():
    out = ''
    chr = ' '
    while chr != '\n':
        chr = nc.recv_exactly(1).decode()
        if chr != '\n':
            out += chr
    return out.encode()

def sendA(number):
    nc.recv_exactly(5)
    nc.send_line(b'A')
    nc.recv_exactly(7)
    string = hex(number)[2:]
    if len(string) % 2 == 1:
        string = '0' + string
    nc.send_line(string.encode())
    #print(string.encode())
    string = saferecv()
    #print(string)
    return int(string, 16)
    
def sendB(number):
    nc.recv_exactly(5)
    nc.send_line(b'B')
    nc.recv_exactly(7)
    string = hex(number)[2:]
    if len(string) % 2 == 1:
        string = '0' + string
    nc.send_line(string.encode())
    string = saferecv()
    #print(string)
    return int(string, 16)

nc = Netcat((HOSTNAME, PORT))
print(nc.recv_exactly(18))

flag = int(saferecv(), 16)

N = 0
for i in range(10):
    k = i*7 + 3
    a1 = sendA(k)
    a2 = sendA(k*k)
    N = gcd(N, a1*a1 - a2)
    
print(N)

sflag = ""
vflag = 0

for i in range(65):
    potinv = modinv(2**(8*i), N)
    enck = sendA(potinv)
    print(potinv)
    print((potinv * (2**(8*i))) % N)
    msg = sendB(enck * flag)
    msg = (msg - (potinv * vflag) % N) % 256
    print(msg)
    vflag += msg * 2**(8*i)
    sflag = chr(msg) + sflag
    print(sflag)