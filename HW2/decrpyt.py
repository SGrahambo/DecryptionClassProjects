
import os
import hashlib
import csv
import time

def sha3_binary(input_binary):
    # Convert the binary string to bytes
    input_bytes = bytes(int(input_binary[i:i+8], 2) for i in range(0, len(input_binary), 8))
    # Compute SHA-3 hash
    sha3_hash = hashlib.sha3_256(input_bytes).digest()
    # Convert hash back to binary
    
    return ''.join(format(byte, '08b') for byte in sha3_hash)

def binary_to_words(binary_string):
    # Convert binary string back to words, handling spaces correctly
    words = ''.join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))
    # Trim any trailing null characters that may have been added as padding
    words = words.rstrip('\x00')
    return words

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

def increment_binary(binary_string):
    num = int(binary_string, 2)
    num += 1

    return format(num, '0' + str(len(binary_string)) + 'b')


file_name = "results.csv"

# first_secret = "00000000"
# second_secret = "011001100110011001100110011001100110011001100110011001100110011001100110011001100110011001100110011001100110011001100110"
first_secret = "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
second_secret = ""
first_secret_length = len(first_secret)

ciphertext_binary = "11101100000101110101001000101101101000111011101011001111001101101010101001000101000011010111011110011010011010001011001110011011110100010011001000100110000000000011100010101010001111001101010110010001101111000001000111000111100100101000001101110110100111001111101110001100000101100111011101010001001011111001110010110000101001110001100100111001100000101110111011011110111001000111000111101110001100111010110011000000110111001010110110000001001000000001110001001101100111100110100010110100011001111111000001100100"
# with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
#     csv_writer = csv.writer(csvfile)

#     if csvfile.tell() == 0:
#         csv_writer.writerow(['Secret Key', 'Decrypted Message'])

#     while first_secret_length >= len(first_secret):
#         # print("first secret:", first_secret)
#         secret_key_binary = first_secret + second_secret
#         decrypted_message_binary = decrypt(ciphertext_binary, secret_key_binary)
#         decrypted_message = binary_to_words(decrypted_message_binary)

#         csv_writer.writerow([secret_key_binary, decrypted_message])

#         # print("Decrypted Message:", decrypted_message)

#         first_secret = increment_binary(first_secret)

with open('C:/Users/sgrah/Documents/CS 327/HW2/' + file_name, 'a', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    count = 0
    
    # Write headers if the file is empty
    if csvfile.tell() == 0:
        csv_writer.writerow(['Secret Key', 'Decrypted Message'])

    t0 = time.time()
    
    while first_secret_length >= len(first_secret):
        secret_key_binary = first_secret + second_secret
        decrypted_message_binary = decrypt(ciphertext_binary, secret_key_binary)
        decrypted_message = binary_to_words(decrypted_message_binary)

        csv_writer.writerow([secret_key_binary, decrypted_message])

        first_secret = increment_binary(first_secret)
        count += 1
        if (count == 100000):
            print("keys processed: ", count)
            print("key: ", secret_key_binary)
            break

    t1 = time.time()

    totalTime = t1-t0
    print("time: ", totalTime)

        






        
# secret_key_binary = first_secret + second_secret
# decrypted_message_binary = decrypt(ciphertext_binary, secret_key_binary)
# decrypted_message = binary_to_words(decrypted_message_binary)

# Encrypt and decrypt the message

# print("Ciphertext (Binary):", ciphertext_binary)
# print("cipherlengh", len(ciphertext_binary))
# print("Decrypted Message:", decrypted_message)