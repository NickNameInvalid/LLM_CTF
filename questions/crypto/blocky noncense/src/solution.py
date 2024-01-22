import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# A simple block cipher implementation
class SimpleBlockCipher:
    def __init__(self, key):
        self.key = key
        self.cipher = AES.new(self.key, AES.MODE_ECB)

    def encrypt(self, plaintext):
        # Pad the plaintext to a multiple of the block size
        padded_plaintext = pad(plaintext, AES.block_size)
        # Encrypt the plaintext
        ciphertext = self.cipher.encrypt(padded_plaintext)
        return ciphertext

    def decrypt(self, ciphertext):
        # Decrypt the ciphertext
        padded_plaintext = self.cipher.decrypt(ciphertext)
        # Unpad the plaintext
        plaintext = unpad(padded_plaintext, AES.block_size)
        return plaintext

# Example usage
if __name__ == "__main__":
    # Generate a random 256-bit key (32 bytes)
    key = get_random_bytes(32)
    
    # Create a block cipher instance
    cipher = SimpleBlockCipher(key)
    
    # Example plaintext
    plaintext = b"This is a secret message."
    
    # Encrypt the plaintext
    ciphertext = cipher.encrypt(plaintext)
    print(f"Ciphertext: {ciphertext}")
    
    # Decrypt the ciphertext
    decrypted_plaintext = cipher.decrypt(ciphertext)
    print(f"Decrypted plaintext: {decrypted_plaintext}")