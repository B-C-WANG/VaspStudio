import pickle
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

class Info():
    def __init__(self,info):
        self.info = info




def encrypt(key,text):
    cryptor = AES.new(key, AES.MODE_CBC, key)
    # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
    length = 16
    count = len(text)


    if (count % length != 0):
        add = length - (count % length)
    else:
        add = 0

    text = text + (b'\0' * add)
    ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
    return b2a_hex(ciphertext)

def decrypt(key, text):
        cryptor = AES.new(key, AES.MODE_CBC, key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip(b'\0')


def make_a_key_with_right_length(key):
    # key的长度为16 24 或32，需要零补如果不满足长度条件

    if len(key) < 16:
        key += int(16 - len(key)) * "0"
    elif len(key) < 24:
        key += int(24 - len(key)) * "0"
    elif len(key) < 32:
        key += int(24 - len(key)) * "0"
    return  key




def pickle_encrypt_to_file(file_path,key,object):

    key = make_a_key_with_right_length(key)
    data = pickle.dumps(object)
    data = encrypt(key, data)
    with open(file_path,"wb") as f:
        f.write(data)

def pickle_decrypt_from_file(file_path,key):
    key = make_a_key_with_right_length(key)
    with open(file_path,"rb") as f:
        data = f.read()
    data = decrypt(key,data)
    return pickle.loads(data)


if __name__ == '__main__':

    key = "wang" # 用户给出的key，只能由用户自己记忆，或服务器备份

    # pickle加密
    a = Info("password")

    pickle_encrypt_to_file("pw.vspp",key,a)

    a = pickle_decrypt_from_file("pw.vspp",key)
    print(a.info)







    