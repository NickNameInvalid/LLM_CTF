import subprocess

flag = "csawctf{st1ng_th30ry_a1nt_so_h4rd}"

result = subprocess.run(["./babysthird"], input=flag.encode(), stdout=subprocess.PIPE)

if result.stdout.decode().strip() == "Correct!":
    print("The flag is:", flag)
else:
    print("Incorrect password")