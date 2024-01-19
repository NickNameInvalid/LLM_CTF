from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Reverse engineer the special_function to find the original key
def reverse_special_function(n):
    # Since the special_function is a polynomial of degree 4, we can use
    # the quadratic formula to find the roots and then check which one is valid.
    # The roots of the polynomial are the values of n for which the function returns 1.
    # We can find these roots by setting the derivative of the polynomial to zero.
    # The roots are approximately 1.585 and 4.415, so we'll check these values.
    for root in [1, 2, 3, 4, 5]:
        if special_function(root) == 1:
            return root
    return None

def special_function(n):
    if n < 1:
        return 1
    else:
        return 1 + (n*(n**3 - 6*(n**2) + 23*n - 18)//24)

# Find the original key
original_key = reverse_special_function(0xcafed3adb3ef1e37)
key = original_key.to_bytes(32, "big")

# Decrypt the encrypted image
with open('flag.enc', 'rb') as f:
    enc = f.read()

iv = b"r4nd0m_1v_ch053n"
cipher = AES.new(key, AES.MODE_CBC, iv)
dec = unpad(cipher.decrypt(enc), AES.block_size)

# Save the decrypted image to a file
with open('flag.png', 'wb') as f:
    f.write(dec)

print("Flag saved to flag.png")