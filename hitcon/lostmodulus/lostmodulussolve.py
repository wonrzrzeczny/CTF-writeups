from nclib import *
import base64

HOSTNAME = "13.112.92.9"
PORT = 21701

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
    string = saferecv()
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
    return int(string, 16)

nc = Netcat((HOSTNAME, PORT))
print(nc.recv_exactly(18))

flag = int(nc.recv_exactly(512).decode(), 16)
print(flag)
nc.recv_exactly(1)
XD = 0

N = 0
i = 1024
while i >= 0: #decrypting N
    print(i)
    print(N)
    poti = sendA(2**i)
    encN = sendA(N)
    for j in range(i, i + 4)[::-1]: #ugh
        print(j)
        N += 2**j
        kkk = j - i
        realmod = N % 256
        
        encN = encN * (poti ** (2**kkk))
        
        encrmod = sendB(encN)
        if realmod != encrmod:
            N -= 2**j
            encN = encN // (poti ** (2**kkk))
            XD = encrmod
            print (encrmod)
    i -= 4
    
N += 1
#yay, we found the modulo
print(N)
print(flag)

sflag = ""
vflag = 0

#decrypting flag
def flagsub(flag, k, n):
    return ((1 - n*k) * flag) % (n*n)
    
vflag = 100875957455868337925440735881740964923696086881408630419864201017940698935980156443839104427677325695508371154529740778088364312572340524480844371681868776114848753736744960 #it should be equal to 0 at the beginning, the value you see here is the value calculated after the first run of the program
for i in range(0, 148)[::-1]: #for should start from i = 600, the 148 here was also set for the second run
    print(i)
    print(vflag)
    vflag += 2**i
    realmod = (10 - vflag) % 256
    encrmod = sendB(flagsub(flag, vflag, N))
    if realmod != encrmod:
        vflag -= 2**i