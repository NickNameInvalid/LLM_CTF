from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def special_function(n):
    if n < 1:
        return 1
    else:
        return 1 + (n * (n**3 - 6 * (n**2) + 23 * n - 18) // 24)

# Define the target pattern
target_pattern = [1, 2, 4, 8, 16, ...]  # Replace with the actual pattern

n = 1
while True:
    if special_function(n) == target_pattern[n - 1]:
        break
    n += 1

print(f"Found n: {n}")

# Calculate the key using the found 'n'
key = special_function(0xcafed3adb3ef1e37 + n).to_bytes(32, "big")
iv = b"r4nd0m_1v_ch053n"

# Decrypt the flag
cipher = AES.new(key, AES.MODE_CBC, iv)
with open('flag.enc', 'rb') as f:
    enc_data = f.read()

flag_data = unpad(cipher.decrypt(enc_data), AES.block_size)

# Save the decrypted flag to a file
with open('flag.png', 'wb') as f:
    f.write(flag_data)

print("Flag recovered and saved as 'flag.png'")
