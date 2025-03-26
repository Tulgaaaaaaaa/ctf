from pwn import *
import string


r = remote('94.237.48.147',52676)

initil = b'A' * 16
pw = b''

for i in range(16):
    for c in string.ascii_letters + string.digits:
        r.sendline(b'1')
            
        two = b'A' * (16 - (len(pw) + 1))
        three = two + pw + c.encode()
            
        pay = initil + three + two

        r.sendline(pay)
        r.recv()
        
        enc = bytes.fromhex(r.recvuntil(b'\n\n').split(b' ')[-1].replace(b'\n\n',b'').decode())
            
        second = enc[16:32]
        third = enc[32:48]

        if xor(second, initil) == xor(third, three):
            pw += c.encode()
            break
        else:
            print('Failed: ', c)
    
    print(pw)

for j in range(1,5):

    r.sendline(b'1')
    first = b'A' * (16 - (j))
    pay = initil + first
    r.sendline(pay)
    r.recv()
    enc = bytes.fromhex(r.recvuntil(b'\n\n').split(b' ')[-1].replace(b'\n\n',b'').decode())
    third = enc[32:48]

    for c in string.ascii_letters + string.digits:
        r.sendline(b'1')
        lol = pw[1:]
        pay = initil + first + pw[:j] + lol + c.encode()
        r.sendline(pay)
        r.recv()

        enc = bytes.fromhex(r.recvuntil(b'\n\n').split(b' ')[-1].replace(b'\n\n',b'').decode())

        second = enc[32:48]

        if second == third:
            pw += c.encode()
            break
        else:
            print('Failed: ', c)
    
    print(pw)

r.sendline(b'2')
r.sendline(bytes(pw))

print(r.recv())
print(r.recv())

r.interactive()





# [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]
# [ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ] --- [ ][ ][ ][ ]
