from collections import Counter

with open('./challenge/ENCRYPTED', 'r') as f:
    data = f.read().split()[0]

def freq_analysis(data):
    sorted_freq = sorted(Counter(data).items(), key=lambda x: x[1], reverse=True)
    for char, count in sorted_freq:
        print(f"'{char}': {count}")

def recover_some_letters(data):
    special_chars = {
        'one': {'E', 'Y', 'U'},
        'two': {'X', 'A'},
        'three': {'N', 'W', 'G'},
        'four': {'C', 'I', 'R', 'D'},
        'six': {'L', 'J', 'O', 'T', 'P', 'V'},
        'eight': {'H', 'F', 'K', 'Q', 'S', 'B', 'M', 'Z'}
    }

    result = []
    for i, char in enumerate(data):
        if char in special_chars['one']:
            result.append(char)
        elif i % 2 == 0 and char in special_chars['two']:
            result.append(char)
        elif i % 3 == 0 and char in special_chars['three']:
            result.append(char)
        elif i % 4 == 0 and char in special_chars['four']:
            result.append(char)
        elif i % 6 == 0 and char in special_chars['six']:
            result.append(char)
        elif i % 8 == 0 and char in special_chars['eight']:
            result.append(char)
        else:
            result.append('.')

    return result

freq_analysis(data)
recovered = recover_some_letters(data)

open('TEST','w').write(''.join(recovered))

for i in range(len(recovered)):
    window = recovered[i-5:i+5]
    if '.' not in window:
        print(recovered[i-9:i+5])

