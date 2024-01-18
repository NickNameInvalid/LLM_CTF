import subprocess

# Interact with the executable to trigger flag generation
subprocess.run(["./bin.out"])  # Assuming "bin.out" is in the current directory

# Access the global 'flag' variable from the executable's memory
flag = subprocess.check_output(["strings", "./bin.out"]).decode()

# Find the actual flag within the extracted strings
start_index = flag.find("CTF{")
end_index = flag.find("}")
flag = flag[start_index:end_index + 1]

print("The flag is:", flag)
