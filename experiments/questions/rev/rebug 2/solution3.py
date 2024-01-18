import subprocess

def main():
    process = subprocess.Popen(["./bin.out"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, _ = process.communicate()

    flag_chars = []
    for char_str in output.split()[2::2]:  # Extract even-indexed characters
        char_code = int(char_str)
        binary_str = bin(char_code)[2:].zfill(8)
        left_half = binary_str[:4]
        right_half = binary_str[4:]
        xored_value = int(left_half, 2) ^ int(right_half, 2)
        flag_chars.append(chr(xored_value))

    flag = "".join(flag_chars)
    print("Flag:", flag)

if __name__ == "__main__":
    main()
