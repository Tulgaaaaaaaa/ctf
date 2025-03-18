from pwn import *
from string import printable
from time import sleep

chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{@!#$%&()*+,-./:;<=>?[\\]^_`|}~'

r = remote('13.124.117.173', 10302)
r.recv()

block_size = 32

flag = 'CTFMN{'

while flag[-1] != '}':
    for i in chars:
        initial = 'a' * (32 - (len(flag) % block_size) - 1)

        pay = initial + flag + i + initial
        r.sendline(pay.encode())
        cipher = r.recvline()

        k = cipher.replace(b'\r\n', b'').replace(b'ciphertext = ',b'').replace(b'plaintext = ', b'')

        print(pay)

        last = k[128:256]
        first = k[:128]

        if first == last:
            flag += i
            print(pay)
            break

    print(flag)

