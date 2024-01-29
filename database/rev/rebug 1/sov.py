import subprocess

input_str = "A" * 12
p = subprocess.Popen("./test.out", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate(input=input_str.encode())
print(out.decode())