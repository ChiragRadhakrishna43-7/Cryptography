from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
from base64 import b64encode, b64decode

def custom_pad(data, block_size):
    pad_length = block_size - len(data) % block_size
    pad_chr = chr(pad_length)
    return data + pad_chr * pad_length

def custom_unpad(data):
    pad_length = data[-1]
    return data[:-pad_length]

def convert_int_to_bytes(number):
    return number.to_bytes((number.bit_length() + 7) // 8, 'big')

def encrypt_f(text, key):
    key_bytes = convert_int_to_bytes(key)
    secret_key = hashlib.sha256(key_bytes).digest()
    padded_text = custom_pad(text, AES.block_size).encode()
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(padded_text)
    return b64encode(iv + encrypted_data).decode("utf-8")

def decrypt_f(encrypted_data, key):
    key_bytes = convert_int_to_bytes(key)
    secret_key = hashlib.sha256(key_bytes).digest()
    decoded_data = b64decode(encrypted_data)
    iv = decoded_data[:AES.block_size]
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(decoded_data[AES.block_size:])
    unpadded_data = custom_unpad(decrypted_data)
    return unpadded_data.decode("utf-8")
