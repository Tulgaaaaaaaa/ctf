from pwn import *
import time

# Target server address and port
target_ip = '139.162.5.230'
target_port = 10279

# Function to calculate the response time based on the guess
def get_response_time(guess):
    # Connect to the remote server using pwntools
    p = remote(target_ip, target_port)
    
    p.recvuntil("The password is: '")  # Receive password hint
    p.recvuntil("\n")  # Skip the new line
    p.recvuntil("Try to read flag.\n")  # Skip this message
    p.recvuntil("Send your password.\n")  # Skip the message prompting for password
    
    # Send the current guess and measure the response time
    p.sendline(guess.encode())
    start_time = time.time()
    p.recv(1024)  # Wait for the server's response
    end_time = time.time()
    
    p.close()
    return end_time - start_time

# Function to perform the attack and find the password
def timing_attack():
    # The password is most likely around the same length as the one in the example code.
    # We will start by trying to guess the password character by character.

    # Initialize the guess
    guess = ""
    password_length = len("SHA1 was the most common HMAC method in the old good days. Unfortunately now it is retired")
    
    for i in range(password_length):
        best_char = None
        best_time = -1
        
        # Try every possible character (from space to ~ for the exploit)
        for char in range(32, 127):
            guess_try = guess + chr(char)
            response_time = get_response_time(guess_try)
            
            # We're looking for the slowest response time to indicate a match
            if response_time > best_time:
                best_time = response_time
                best_char = chr(char)
        
        # Add the best character to the guess
        guess += best_char
        print(f"Current guess: {guess}")
    
    print(f"Final password guess: {guess}")
    return guess

# Perform the timing attack to guess the password
if __name__ == "__main__":
    final_password = timing_attack()
    print(f"Exploit completed! The guessed password is: {final_password}")

