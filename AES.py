# from 子滨 https://bingege.top/2020/11/28/jin-ri-xiao-yuan/
import math
import random
import base64
from Crypto.Cipher import AES

# 获取随机字符串
def getRandomString(length):
    chs = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    result = ''
    for i in range(0, length):
        result += chs[(math.floor(random.random() * len(chs)))]
    return result

# AES加密
def EncryptAES(s, key, iv='1' * 16, charset='utf-8'):
    key = key.encode(charset)
    iv = iv.encode(charset)
    BLOCK_SIZE = 16
    pad = lambda s: (s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE))
    raw = pad(s)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(bytes(raw, encoding=charset))
    return str(base64.b64encode(encrypted), charset)

# 金智的AES加密过程
def AESEncrypt(data, key):
    return EncryptAES(getRandomString(64) + data, key, getRandomString(16))

if __name__ == '__main__':
    print(EncryptAES('1234567890','1'*16))