from itertools import permutations

def decrypt_with_partial_key(ENCRYPTED, PARTIAL_KEY):
    INV_KEY = {}

    for i in range(len(PARTIAL_KEY)):
        if PARTIAL_KEY[i] != '.':
            original_letter = chr(i + ord('A'))
            encrypted_letter = PARTIAL_KEY[i]
            INV_KEY[encrypted_letter] = original_letter

    decrypted_message = []

    special_chars = {
        'one': {'E', 'Y', 'U'},
        'two': {'X', 'A'},
        'three': {'N', 'W', 'G'},
        'four': {'C', 'I', 'R', 'D'},
        'six': {'L', 'J', 'O', 'T', 'P', 'V'},
        'eight': {'H', 'F', 'K', 'Q', 'S', 'B', 'M', 'Z'}
    }

    for char in ENCRYPTED:
        if char in INV_KEY:
            decrypted_message.append(INV_KEY[char])
        else:
            if i % 4 == 0 and char in special_chars['four']:
                decrypted_message.append(char)
            elif i % 6 == 0 and char in special_chars['six']:
                decrypted_message.append(char)
            elif i % 8 == 0 and char in special_chars['eight']:
                decrypted_message.append(char)
            else:
                decrypted_message.append('?')

    return decrypted_message

word = 'NGW'
all_perm= [''.join(p) for p in permutations(word)]

for perm in all_perm:
    KEY_1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    N_ind = KEY_1.index('N')
    G_ind = KEY_1.index('G')
    W_ind = KEY_1.index('W')

    PARTIAL_KEY = ['X', '.', '.', '.', 'E', '.', 'G', '.', '.', '.', '.', '.', '.', 'N', '.', '.', '.', '.', '.', '.', 'U', '.', 'W', 'A', 'Y', '.']
    PARTIAL_KEY[N_ind] = perm[0]
    PARTIAL_KEY[G_ind] = perm[1]
    PARTIAL_KEY[W_ind] = perm[2]

    ENCRYPTED = open('ENCRYPTED','r').read()
    result = decrypt_with_partial_key(ENCRYPTED, PARTIAL_KEY)


    for i in range(len(result)):
        window = result[i-5:i+8]
        if '?' not in window and window:
            print(''.join(window))

    print('\n\n')

# for i in range(1000):
#     s = result[i]
#     if s == 'N':
#         print(data[i])
