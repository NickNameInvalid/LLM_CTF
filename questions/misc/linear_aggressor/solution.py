import numpy as np

# Given weights
w = np.array([99, 115, 97, 119, 99, 116, 102, 123, 109, 48, 100, 51, 49, 95, 53, 116, 51, 52, 49, 105, 110, 103, 95, 105, 53, 95, 98, 52, 100, 125])

# The flag format is flag{...}, so we know the first and last characters are 'f' and '}'
# We also know that the flag is 30 characters long, so we need to find 28 more characters
# The remaining characters are the ASCII values of the flag minus the weights and 125

# We can find the remaining characters by subtracting the weights and 125 from the ASCII values of the flag
# The ASCII values of the flag are from 97 ('a') to 122 ('z'), and from 48 ('0') to 57 ('9'), and '_' (95)

# We will brute force the remaining characters

# Possible characters
possible_chars = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(48, 58)] + ['_']

# Flag prefix and suffix
flag_prefix = 'flag{'
flag_suffix = '}'

# Find the remaining characters
remaining_chars = []
for i in range(28):
    found = False
    for char in possible_chars:
        if w.dot(np.array([ord(char)])) + 125 == w[i]:
            remaining_chars.append(char)
            found = True
            break
    if not found:
        print("No solution found.")
        exit()

# Construct the flag
flag = flag_prefix + ''.join(remaining_chars) + flag_suffix

print("The flag is:", flag)