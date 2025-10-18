import os
from cryptography.fernet import Fernet

def load_key():
    key = os.environ.get('SECRET_KEY')
    if not key:
        raise Exception("SECRET_KEY environment variable not set!")
    if isinstance(key, str):
        key = key.encode()
    return key

cipher = Fernet(load_key())

def encrypt_data(data):
    if data is None or data == "":
        return ""
    return cipher.encrypt(data.encode('utf-8')).decode('utf-8')

def decrypt_data(encrypted_data):
    if encrypted_data is None or encrypted_data == "" or encrypted_data == b"":
        return ""
    if isinstance(encrypted_data, str):
        encrypted_data = encrypted_data.encode('utf-8')
    return cipher.decrypt(encrypted_data).decode('utf-8')