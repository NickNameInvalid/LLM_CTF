import subprocess

# Any string with 12 characters will work
input_string = "1234567890ab"  # Replace with your desired 12-character string

# Call the target_practice executable with the input
result = subprocess.run(["./test.out"], input=input_string, capture_output=True, text=True)

# Print the output (which should contain the flag)
print(result.stdout)
