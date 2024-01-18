import numpy as np
from PIL import Image

# Function to convert a number to a 32-bit binary string
def number_to_binary(num):
    return format(num, '032b')

# Read the numbers from the file
with open('qr_code.txt', 'r') as file:
    numbers = file.read().splitlines()

# Convert each number to a binary string and map '1' to black and '0' to white
qr_code_data = []
for num in numbers:
    binary_str = number_to_binary(int(num))
    row_data = [int(bit) * 255 for bit in binary_str]  # '1' for black, '0' for white
    qr_code_data.append(row_data)

# Convert the list of lists to a numpy array
qr_code_array = np.array(qr_code_data, dtype=np.uint8)

# Create an image from the numpy array and save it as a PNG file
img = Image.fromarray(qr_code_array, 'L')
img.save('qr_code.png')

print("QR code image saved as 'qr_code.png'. Scan it to get the flag.")