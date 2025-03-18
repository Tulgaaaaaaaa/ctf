from pwn import *
from string import printable
from time import sleep

chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ{@!#$%&()*+,-./:;<=>?[\\]^_`|}~'

r = remote('13.124.117.173', 10301)
r.recv()

flag = 'CTFMN{'

while flag[-1] != '}':
    for i in chars:
        ind = 0
        if len(flag) % 2 == 0:
            ind = (len(flag)+2) * 16
            pay = 'A' + flag + i + 'A'
        else:
            ind = (len(flag)+1) * 16
            pay = flag + i
        
        r.sendline(pay.encode())

        cipher = r.recvline()
        k = cipher.replace(b'\r\n', b'').replace(b'ciphertext = ',b'').replace(b'plaintext = ', b'')

        last = k[ind:ind*2]
        first = k[:ind]

        if first == last:
            flag += i
            print('Found!')
            print(pay)
            break
    print(flag)
