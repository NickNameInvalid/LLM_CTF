def generate_flag(n1, n2):
    xor_result = n1 ^ n2
    flag = ""
    for i in range(8):  # 8 bytes in a 64-bit number
        byte_value = (xor_result >> (i * 8)) & 0xFF
        flag += format(byte_value, '08b')  # Convert byte to binary string
    return flag

local_28 = 0x6e37625970416742
local_20 = 0x44777343

flag = generate_flag(local_28, local_20)
print(flag)