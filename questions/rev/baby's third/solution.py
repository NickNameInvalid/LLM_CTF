import subprocess

def get_flag():
    # The hardcoded string in the C code
    flag = "csawctf{st1ng_th30ry_a1nt_so_h4rd}"

    # Call the executable with the flag as input
    result = subprocess.run(["./babysthird"], input=flag.encode(), stdout=subprocess.PIPE)

    # Print the output
    print(result.stdout.decode())

get_flag()