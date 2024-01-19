import subprocess

# The input string can be anything of length 12
input_string = "A" * 12

# Call the executable file "test.out" with the input string
result = subprocess.run(["./test.out"], input=input_string.encode(), stdout=subprocess.PIPE)

# Print the output
print(result.stdout.decode())