from tales import *
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

n = 0x1337
e = 0x10001

def scramble(a, b):
    return [b[a[i]] for i in range(n)]

def super_scramble(a, e):
    b = list(range(n))
    while e:
        if e & 1:
            b = scramble(b, a)
        a = scramble(a, a)
        e >>= 1
    return b

def inverse_permutation(p):
    inv = [0] * len(p)
    for i, pi in enumerate(p):
        inv[pi] = i
    return inv

def reverse_scramble(scrambled_msg, e):
    identity = list(range(n))
    P = super_scramble(identity, e)
    P_inv = inverse_permutation(P)
    original_msg = [scrambled_msg[P_inv[i]] for i in range(n)]
    return original_msg

message = reverse_scramble(scrambled_message,e)

key = sha256(str(message).encode()).digest()
dec_flag = AES.new(key, AES.MODE_ECB).decrypt(bytes.fromhex(enc_flag))

print(dec_flag)
print(unpad(dec_flag, 16).decode())