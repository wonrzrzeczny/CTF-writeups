from gmpy2 import invert, gcd
from sys import setrecursionlimit

import nclib

nc = nclib.Netcat(('hax.allesctf.net', 7331))

def recv_until(s):
	out = b''
	while not out.endswith(s):
		out += nc.recv_exactly(1)
	return out
	
def recv_infinite():
	while True:
		print(nc.recv_exactly(1).decode(), end='')

def mul(a, b, v, p):
	xa, ya = a[0], a[1]
	xb, yb = b[0], b[1]
	xr = (xa * xb + v * ya * yb) % p
	yr = (xa * yb + xb * ya) % p
	return (xr, yr)

def add(a, b, p):
	xa, ya = a[0], a[1]
	xb, yb = b[0], b[1]
	return ((xa + xb) % p, (ya + yb) % p)

#This boi likes to crush exponential hopes and dreams
setrecursionlimit(1000000)

def poww(a, e, v, p):
	if e == 0:
		return (1, 0)
	if e % 2 == 0:
		r = poww(a, e // 2, v, p)
		return mul(r, r, v, p)
	r = poww(a, e - 1, v, p)
	return mul(a, r, v, p)

def sqroot(s, p, k):
	#finding non-residue
	a = 1
	while pow(a * a - s, (p - 1) // 2, p) != p - 1:
		a += 1
	#the formula
	t = (p**k - 2 * p**(k-1) + 1) // 2
	q = p**(k - 1) * (p + 1) // 2
	pk = p ** k
	ld = a * a - s
	return (invert(2, pk) * pow(s, t, pk) * add(poww((a, 1), q, ld, pk), poww((a, -1), q, ld, pk), pk)[0]) % pk
	
from Crypto.Util.number import getPrime, getRandomRange

for i in range(42):
	p = getPrime(512)
	nc.send(str(p*p).encode() + b'\n')
	recv_until(b'of\n')
	s = int(recv_until(b'\n'))
	r = sqroot(s, p, 2)
	nc.send(str(r).encode() + b'\n')
	print(recv_until(b'p: '))
	nc.send(str(p).encode() + b'\n')
	recv_until(b'q: ')
	nc.send(str(p).encode() + b'\n')

recv_infinite()