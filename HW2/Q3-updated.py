
# coding: utf-8

# In[3]:


import os
import hashlib

def key_generation():
    # Generate a random byte followed by a fixed sequence of bytes, all in binary
    r = os.urandom(1)
    secret_key_binary = ''.join(format(byte, '08b') for byte in r) + '01100110' * 15  # 16 bytes total
    #print("secret key",secret_key_binary )
    #print("lengh", len(secret_key_binary))
    return secret_key_binary

def sha3_binary(input_binary):
    # Convert the binary string to bytes
    input_bytes = bytes(int(input_binary[i:i+8], 2) for i in range(0, len(input_binary), 8))
    # Compute SHA-3 hash
    sha3_hash = hashlib.sha3_256(input_bytes).digest()
    # Convert hash back to binary
    
    return ''.join(format(byte, '08b') for byte in sha3_hash)

def words_to_binary(words):
    # Convert words to a binary string, ensuring a space ('00100000') between words
    binary_result = ''.join(format(ord(char), '08b') for word in words for char in (word + ' '))
    # Trim the last space added above and ensure the string is exactly 512 bits
    binary_result = binary_result[:-8]  # Remove the last '00100000'
    binary_result = binary_result.ljust(512, '0')[:512]  # Ensure exactly 512 bits
    return binary_result

def binary_to_words(binary_string):
    # Convert binary string back to words, handling spaces correctly
    words = ''.join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))
    # Trim any trailing null characters that may have been added as padding
    words = words.rstrip('\x00')
    return words


def encrypt(message_binary, secret_key_binary):
    # Generate initial subkeys from the SHA-3 hash of the binary secret key
    sha3_result_binary = sha3_binary(secret_key_binary)
    #print("sha3output",sha3_result_binary )
    #print("length", len( sha3_result_binary))
    S1_binary, S2_binary = sha3_result_binary[:128], sha3_result_binary[128:]
    
    # Hash S1 and S2 again with SHA-3
    S1_hashed_binary = sha3_binary(S1_binary)
    S2_hashed_binary = sha3_binary(S2_binary)
    
    # XOR operation directly on binary strings
    subkey_binary = S1_hashed_binary + S2_hashed_binary  # Concatenate the two subkeys
    
    #print("r_star", len(subkey_binary))
    ciphertext_binary = ''.join(str(int(message_binary[i]) ^ int(subkey_binary[i % len(subkey_binary)])) for i in range(len(message_binary)))
    return ciphertext_binary

def decrypt(ciphertext_binary, secret_key_binary):
    # Decryption follows the same process as encryption due to XOR's symmetric nature
    sha3_result_binary = sha3_binary(secret_key_binary)
    #print("length", len( sha3_result_binary))
    S1_binary, S2_binary = sha3_result_binary[:128], sha3_result_binary[128:]
    
    # Hash S1 and S2 again with SHA-3
    S1_hashed_binary = sha3_binary(S1_binary)
    S2_hashed_binary = sha3_binary(S2_binary)
    
    # XOR operation directly on binary strings
    subkey_binary = S1_hashed_binary + S2_hashed_binary  # Concatenate the two subkeys
    message_output = ''.join(str(int( ciphertext_binary[i]) ^ int(subkey_binary[i % len(subkey_binary)])) for i in range(len(ciphertext_binary)))
    return message_output

# Example usage
# secret_key_binary = key_generation()
secret_key_binary = "11111111011001100110011001100110011001100110011001100110011001100110011001100110011001100110011001100110011001100110011001100110"
#print("secret key",secret_key_binary )
english_words = input("Enter English words for the message (e.g., 'hello world'): ").split()
message_binary = words_to_binary(english_words)

# Encrypt and decrypt the message
ciphertext_binary = encrypt(message_binary, secret_key_binary)
# ciphertext_binary = "00010011110111000111000011001101011101010110010011110011100010010000001101011101101101011100110101010001000111010100000001011111011110110110100101110011110110110110011110101001110000100000011010111010110010100011101011100011000100000000010101100011001000010001001010011110000010100101100000001011110001100001100111100110010000110101111000111011101111110011110000110101001100011100010111100011100001010001000110011101111011010001111100111100110100001100000001101011010111111011101110001001101100011010110101011100"
decrypted_message_binary = decrypt(ciphertext_binary, secret_key_binary)
decrypted_message = binary_to_words(decrypted_message_binary)

print("Decrypted Message:", decrypted_message)
print("Ciphertext (Binary):", ciphertext_binary)
print("cipherlengh", len(ciphertext_binary))

