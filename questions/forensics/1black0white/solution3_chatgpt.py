import qrcode
import numpy as np
from PIL import Image

# Given numbers
numbers = [
    533258111, 274428993, 391005533, 391777629, 390435677, 273999169, 534074751, 99072, 
    528317354, 446173689, 485174588, 490627992, 105525542, 421383123, 132446300, 431853817, 
    534345998, 496243321, 365115424, 302404521, 289808374, 1437979, 534308692, 272742168, 
    391735804, 391385911, 391848254, 273838450, 534645340
]

# Convert each number to binary and pad them to have the same length
binaries = [format(num, 'b').zfill(32) for num in numbers]  # Using 32-bit for each number

# Combine all binary strings
combined_binaries = ''.join(binaries)

# Determine the size of the QR code matrix
size = int(np.sqrt(len(combined_binaries)))
if size * size != len(combined_binaries):
    raise ValueError("The total number of binary digits does not form a perfect square.")

# Create the matrix
matrix = np.array([int(bit) for bit in combined_binaries]).reshape(size, size)

# Convert the binary matrix to an image (QR Code)
# Here, 1 represents black (0 in QR is usually white and 1 is black)
qr_image = Image.fromarray(np.uint8(matrix * 255), 'L')

# Display the QR code image
qr_image.show()
