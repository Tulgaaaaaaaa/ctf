n = 0x13
e = 0x10001

def scramble(b, a):
    print('a ->', a)
    print('b ->', b)
    k = []

    for i in range(n):
        k.append(a[b[i]])
    print(f'k -> {k}\n')
    return k

def super_scramble(a, e):
    b = list(range(n))
    while e:
        if e & 1:
            print('-' * 70)
            b = scramble(b, a)
        a = scramble(a, a)
        e >>= 1
    return b

message = [1, 4, 7, 15, 10, 9, 3, 6, 8, 17, 16, 5, 2, 13, 12, 14, 18, 0, 11]

scrambled_message = super_scramble(message, e)

print(scrambled_message)

# b = [0,1,2,3,4]
# a = [4,1,3,0,2]

# b = [4,1,3,0,2]