from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
from base64 import b64encode, b64decode

blockSize = AES.block_size

def pad(plain_text):
    number_of_bytes_to_pad = blockSize - len(plain_text) % blockSize
    padding_str = chr(number_of_bytes_to_pad) * number_of_bytes_to_pad
    padded_txt = plain_text.encode() + padding_str.encode()
    return padded_txt

def unpad(plain_txt):
    lst_ch = plain_txt[-1:]
    return plain_txt[:-ord(lst_ch)]

def int_to_bytes(integer):
    return integer.to_bytes((integer.bit_length() + 7) // 8, byteorder='big')

def encrypt_f(plain_txt, shared_secret):
    key_bytes = int_to_bytes(shared_secret)
    secret = hashlib.sha256(key_bytes).digest()
    padded_txt = pad(plain_txt)
    iv = get_random_bytes(blockSize)
    cipher = AES.new(secret, AES.MODE_CBC, iv)
    cipher_text = cipher.encrypt(padded_txt)
    return b64encode(iv + cipher_text).decode("utf-8")

def decrypt_f(cipher_txt, shared_secret):
    key_bytes = int_to_bytes(shared_secret)
    secret = hashlib.sha256(key_bytes).digest()
    cipher_txt = b64decode(cipher_txt)
    iv = cipher_txt[:AES.block_size]
    cipher = AES.new(secret, AES.MODE_CBC, iv)
    plain_txt = cipher.decrypt(cipher_txt[AES.block_size:]).decode("utf-8")
    return unpad(plain_txt)
