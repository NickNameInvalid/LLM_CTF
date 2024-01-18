# Convert the list of seemingly random numbers to a string of bits
data_string = ""
for number in [533258111, 274428993, 391005533, 391777629, 390435677, 273999169, 534074751, 99072, 528317354, 446173689, 485174588, 490627992, 105525542, 421383123, 132446300, 431853817, 534345998, 496243321, 365115424, 302404521, 289808374, 1437979, 534308692, 272742168, 391735804, 391385911, 391848254, 273838450, 534645340]:
    # Convert the number to binary representation
    binary_string = bin(number)[2:]
    # Pad the binary string with leading zeros to make it 8 bits long
    binary_string = binary_string.zfill(8)
    data_string += binary_string

# Extract the first 4 bytes (32 bits) as the version and error correction level
version_ec_level = data_string[:32]

# Extract the remaining data bits
data_bits = data_string[32:]

# Convert the data bits to a string of characters
data_string = ""
for i in range(0, len(data_bits), 8):
    byte_string = data_bits[i:i+8]
    character = chr(int(byte_string, 2))
    data_string += character

# Check if the extracted data starts with "csawctf{"
if data_string.startswith("csawctf{"):
    # Print the extracted flag
    print(data_string)
else:
    print("Error: Extracted data does not start with 'csawctf{'")