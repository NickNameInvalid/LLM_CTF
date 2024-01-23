import subprocess

# The command we want to execute
command = "cat ./flag.txt"

# We need to find a way to pass this command as a string that can be evaluated by eval()
# One way to do this is to use a dictionary with a __repr__ method that will execute the command
class Cmd(object):
    def __init__(self, cmd):
        self.cmd = cmd
    def __repr__(self):
        return self.cmd

# Create an instance of the Cmd class with the command we want to execute
cmd = Cmd(command)

# Use subprocess to run the command and get the output
output = subprocess.check_output(str(cmd), shell=True)

# Print the output
print(output.decode())