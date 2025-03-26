import socket
from sympy import symbols


def elliptic_curve_order(a, b, p):
    curve_order = 0

    for i in range(1, p):
        x = pow(a, i, p)
        y = pow(b, i, p)
        
        curve_order += 1
        if (x * y) % p == 0:
            break
    return curve_order

def is_generator(g, p, factors):
    if pow(g, p-1, p) != 1:
        return False
    phi = p - 1
    for q in factors:
        if pow(g, phi // q, p) == 1:
            return False
    return True

p = 21214334341047589034959795830530169972304000967355896041112297190770972306665257150126981587914335537556050020788061
factors = [2, 3, 5, 635599, 2533393, 4122411947, 175521834973, 206740999513, 1994957217983, 215264178543783483824207, 10254137552818335844980930258636403]

HOST = '94.237.57.187'
PORT = 55762

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    def recv_until(prompt):
        data = b''
        while not data.endswith(prompt):
            data += s.recv(1)
        return data
    
    print(recv_until(b'How many bits is the prime p? > ').decode())
    s.sendall(b'384\n')
    
    print(recv_until(b'Enter the full factorization of the order of the multiplicative group in the finite field F_p in ascending order of factors (format: p0,e0_p1,e1_ ..., where pi are the distinct factors and ei the multiplicities of each factor) > ').decode())
    factorization = '2,2_5,1_635599,1_2533393,1_4122411947,1_175521834973,1_206740999513,1_1994957217983,1_215264178543783483824207,1_10254137552818335844980930258636403,1\n'
    s.sendall(factorization.encode())
    
    print(recv_until(b'\n').decode())
    for _ in range(17):
        g = int(s.recv(1024).strip().decode().replace('? >',''))
        response = b'1\n' if is_generator(g, p, factors) else b'0\n'
        s.sendall(response)
    
    x, y = symbols('x y')
        
    a = 408179155510362278173926919850986501979230710105776636663982077437889191180248733396157541580929479690947601351140
    b = 8133402404274856939573884604662224089841681915139687661374894548183248327840533912259514444213329514848143976390134

    # order = str(elliptic_curve_order(a, b, p)).encode()
    # print(order)
    # print(recv_until(b'What is the order of the curve defined over F_p? >').decode())
    print(recv_until(b'What is the order of the curve defined over F_p? >').decode())
    s.sendall(str(p).encode())

    print(s.recv(4096).decode())
