from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Define the special function based on Moser's Circles pattern
def special_function(n):
    if n < 1:
        return 1
    else:
        return 2**(n - 1)  # Modified to reflect Moser's Circles pattern

# Decrypt the flag using the inferred key and given IV
with open('flag.enc', 'rb') as f:
    enc = f.read()

key = special_function(0xcafed3adb3ef1e37).to_bytes(32, "big")
iv = b"r4nd0m_1v_ch053n"
cipher = AES.new(key, AES.MODE_CBC, iv)
data = unpad(cipher.decrypt(enc), AES.block_size)

with open('flag_decrypted.png', 'wb') as f:
    f.write(data)

print("Decrypted flag saved as flag_decrypted.png")
