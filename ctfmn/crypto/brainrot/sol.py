import base64

def decrypt_message(encrypted_str, secret):
    decoded_str = base64.b64decode(encrypted_str).decode('utf-8')

    decrypted_str = ''.join(
        chr(ord(c) ^ ord(secret[i % len(secret)])) for i, c in enumerate(decoded_str)
    )
    return decrypted_str

if __name__ == "__main__":
    encrypted_str = "TwMdLyVaRRsOCCZ3WA0aHwUndzccEBkMNmk2FhwGVW09DQ0fDld+ZgwcEg9XfisLHQpVIRh7VEtHED0qehccOAINMXkKDUMYBi8sUREaBQ4/dUsbHA8QfHVLEQcGBXw="
    import itertools

    word = "Skibidi"

    combinations = []
    for combo in itertools.product(*[(char.lower(), char.upper()) for char in word]):
        combinations.append(''.join(combo))

    for combination in combinations:

        decrypted_message = decrypt_message(encrypted_str, combination)
        print(combination + "->  Decrypted message:", decrypted_message)

