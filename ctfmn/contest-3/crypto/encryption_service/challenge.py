import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

flag = os.environ.get('flag', 'CTFMN{fake_flag_for_testing}')
key = os.urandom(16)

def encode(text):
    result = ''
    for char in text:
        result += f'{ord(char):08b}'
    return result


def encrypt(pt):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(pt.encode(), 16))
    return ciphertext.hex()


while True:
    pt = input('plaintext = ')
    pt = encode(pt) + encode(flag)
    print('ciphertext =', encrypt(pt))
