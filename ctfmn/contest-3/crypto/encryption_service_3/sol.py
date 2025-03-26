from pwn import *
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Assuming the server is running locally on port 12345
conn = remote('localhost', 12345)

def get_ciphertext(input_text):
    conn.sendlineafter('plaintext = ', input_text)
    ciphertext = conn.recvline().decode().strip().split(' = ')[1]
    return ciphertext

def extract_flag():
    flag = ''
    block_size = 16
    known_flag = ''

    while True:
        # Determine the length of the flag
        input_length = block_size - (len(known_flag) % block_size) - 1
        input_text = 'A' * input_length

        # Get the ciphertext for the input
        ciphertext = get_ciphertext(input_text)
        target_block = len(ciphertext) // (2 * block_size) - 1

        # Brute force each byte
        for i in range(256):
            test_input = input_text + known_flag + chr(i)
            test_ciphertext = get_ciphertext(test_input)
            if test_ciphertext[target_block * block_size * 2:(target_block + 1) * block_size * 2] == ciphertext[target_block * block_size * 2:(target_block + 1) * block_size * 2]:
                known_flag += chr(i)
                print(f"Found byte: {chr(i)}")
                break

        # Check if we have found the entire flag
        if known_flag.endswith('}'):
            break

    return known_flag

flag = extract_flag()
print(f"Extracted flag: {flag}")
conn.close()

