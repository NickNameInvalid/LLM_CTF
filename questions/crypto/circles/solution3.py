from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# The special_function as provided in the server.py code
def special_function(n):
    if n < 1:
        return 1
    else:
        return 1 + (n * (n**3 - 6 * (n**2) + 23 * n - 18) // 24)

# The encrypted image file
with open('flag.enc', 'rb') as f:
    enc = f.read()

# The initialization vector used in the encryption
iv = b"r4nd0m_1v_ch053n"

# The constant used in the server.py code
constant = 0xcafed3adb3ef1e37

# Generate the key using the special_function with the constant
key = special_function(constant).to_bytes(32, "big")

# Create a new AES cipher object with the key and IV
cipher = AES.new(key, AES.MODE_CBC, iv)

# Decrypt the encrypted image
dec = unpad(cipher.decrypt(enc), AES.block_size)

# Save the decrypted image to a file
with open('flag.png', 'wb') as f:
    f.write(dec)

print("Image decrypted successfully and saved as 'flag.png'")