import base64
import requests

def get_flag():
    try:
        response = requests.get('http://android-dropper.csaw.io:3003')
        encoded_flag = response.text.strip()
        decoded_flag = base64.b64decode(encoded_flag)
        flag = obf(275, 306, 42, decoded_flag)
        return flag
    except Exception as e:
        print(e)
        return None

def obf(paramInt1, paramInt2, paramInt3, notTheFlag):
    i = paramInt2 - paramInt1
    arrayOfChar = [0] * i
    for paramInt2 in range(i):
        arrayOfChar[paramInt2] = chr(notTheFlag[paramInt1 + paramInt2] ^ paramInt3)
    return ''.join(arrayOfChar)

print(get_flag())