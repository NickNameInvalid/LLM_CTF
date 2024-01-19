import yaml
import base64
import ansible_vault
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# Circular Bit Shifter decryption function
def circular_bit_shifter_decrypt(data, shift):
    return bytes([(b >> shift | b << (8 - shift)) & 0xFF for b in data])

# Ansible Vault password
vault_password = 'your_vault_password'

# Path to the encrypted vault file
vault_file_path = 'path_to_encrypted_vault_file'

# Decrypt the vault file
decrypted_data = ansible_vault.Vault(vault_password).load(open(vault_file_path).read())

# Extract the secret from the decrypted data
secret = yaml.safe_load(decrypted_data)['sus1337']

# Reverse the Circular Bit Shifter for all 3 variables
for shift in range(8):
    decrypted_secret = circular_bit_shifter_decrypt(base64.b64decode(secret), shift)
    try:
        flag = base64.b64decode(decrypted_secret).decode('utf-8')
        print(f"Flag: {flag}")
        break
    except:
        continue