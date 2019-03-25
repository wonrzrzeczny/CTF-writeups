import CompactFIPS202
from os import urandom

dict = {}

collision = False
counter = 0
msg1 = b''
msg2 = b''

cap = 48

while not collision:
	counter += 1
	if (counter % 1000 == 0):
		print(counter)
	msg = urandom((1600 - cap) // 8)
	hsh = CompactFIPS202.Keccak(1600 - cap, cap, msg, 0x06, 200)
	C = hsh[-(cap // 8):].hex()
	if C in dict:
		msg1 = msg
		msg2 = dict[C]
		collision = True
	else:
		dict[C] = msg

hsh1 = CompactFIPS202.Keccak(1600 - cap, cap, msg1, 0x06, 200)
hsh2 = CompactFIPS202.Keccak(1600 - cap, cap, msg2, 0x06, 200)
	
print(hsh1.hex())
print()
print(hsh2.hex())
print()

diff = b''
for i in range((1600 - cap) // 8):
	diff += (hsh1[i] ^ hsh2[i]).to_bytes(1, byteorder='big')
	
msg1 += ((1600 - cap) // 8)*b'\0'
msg2 += diff

print(msg1.hex())
print(msg2.hex())

print(CompactFIPS202.Keccak(1600 - cap, cap, msg1, 0x06, 32).hex())
print(CompactFIPS202.Keccak(1600 - cap, cap, msg2, 0x06, 32).hex())