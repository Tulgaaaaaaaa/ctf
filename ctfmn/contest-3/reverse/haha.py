import hashlib

def fnv1a_hash(data: bytes) -> int:
    hash_value = 0x811c9dc5
    for byte in data:
        hash_value = (hash_value ^ byte) * 0x1000193
    return hash_value & 0xFFFFFFFF

def shuffle_key(key: bytes, key_length: int) -> bytearray:
    state = bytearray(range(256))
    j = 0
    
    for i in range(256):
        j = (j + state[i] + key[i % key_length]) % 256
        state[i], state[j] = state[j], state[i]
    
    return state

def xor_encrypt(state: bytearray, data: bytearray) -> bytearray:
    i = 0
    j = 0
    encrypted_data = bytearray(len(data))
    
    for index in range(len(data)):
        i = (i + 1) % 256
        j = (j + state[i]) % 256
        state[i], state[j] = state[j], state[i]
        encrypted_data[index] = data[index] ^ state[(state[i] + state[j]) % 256]
    
    return encrypted_data

def encrypt_file(file_path: str, key: bytes):
    try:
        with open(file_path, "rb") as file:
            plaintext = file.read()
    except FileNotFoundError:
        print("Error: File not found")
        return
    
    key_state = shuffle_key(key, len(key))
    ciphertext = xor_encrypt(key_state, bytearray(plaintext))
    
    print("Ciphertext (hex):", " ".join(f"{byte:02X}" for byte in ciphertext))

def main():
    key = b"chall"
    key_hash = fnv1a_hash(key)
    print(f"Key hash: {key_hash:08X}")
    
    file_path = input("Enter plaintext file path: ").strip()
    encrypt_file(file_path, key)

if __name__ == "__main__":
    main()

