from pwn import *
from string import printable
import concurrent.futures

# Character set for the brute force attack
chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+,-./:;<=>?@[\\]^_`{|}~'

# Connect to the remote service
r = remote('13.124.117.173', 10301)
r.recv()

# Starting flag
flag = 'CTFMN{'

# Function to check for matching ciphertext
def check_flag_suffix(i, j, flag):
    ind = (len(flag) + 2) * 16
    pay = flag + i + j
    r.sendline(pay.encode())
    k = r.recv().replace(b'\r\nplaintext = ', b'').replace(b'ciphertext = ', b'')
    last = k[ind:ind*2]
    first = k[:ind]
    
    if first == last:
        return i + printable[printable.index(j)-1]
    return None

# Main loop to find the flag
while flag[-1] != '}':
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Create a list of tasks for each combination of i and j
        tasks = [executor.submit(check_flag_suffix, i, j, flag) for i in chars for j in chars]
        
        # Wait for the results
        for future in concurrent.futures.as_completed(tasks):
            result = future.result()
            if result:
                flag += result
                print('Found!')
                print(flag)
                break  # Stop once we find the next character(s)
    
    print(f"Current flag: {flag}")

