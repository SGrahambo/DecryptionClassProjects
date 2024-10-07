def increment_binary(binary_string):
    # Convert binary string to integer
    decimal_num = int(binary_string, 2)
    
    # Increment the integer by one
    decimal_num += 1
    
    # Convert the incremented integer back to binary and return
    return format(decimal_num, '0' + str(len(binary_string)) + 'b')


# Example usage
binary_number = '0000'
binary_length = len(binary_number)
while binary_length >= len(binary_number):
    print("Incremented binary:", binary_number)
    binary_number = increment_binary(binary_number)
    

# new_number = increment_binary(binary_number)
# print("Incremented binary:", new_number)