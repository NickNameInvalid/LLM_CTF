def printbinchar(char_val):
    """Convert a character to binary and perform XOR operation."""
    binary_representation = format(char_val, '08b')
    return xoring(binary_representation)

def xoring(binary_str):
    """Perform XOR operation on binary string."""
    xor_result = ""
    for i in range(0, 8, 2):
        if binary_str[i] == binary_str[i+1]:
            xor_result += "0"
        else:
            xor_result += "1"
    return xor_result

def main():
    # Initialize values equivalent to local_28 and local_20 in C code
    values = [0x6e, 0x37, 0x62, 0x59, 0x70, 0x41, 0x67, 0x42, 0x44, 0x77, 0x73, 0x43]

    # Flag to store the final result
    flag = ""

    # Iterate and process each value
    for i, val in enumerate(values):
        if i % 2 == 1:  # Only process if index is odd (since C code checks for even and non-zero)
            flag += printbinchar(val)

    return flag

# Run the main function to get the flag
flag = main()
flag
