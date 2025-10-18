from cryptography.fernet import Fernet
import os

# Generate key sekali saja dan simpan dengan aman
def generate_key():
    """Generate encryption key - JALANKAN SEKALI SAJA"""
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)
    print("✅ Encryption key berhasil dibuat!")
    return key

def load_key():
    """Load encryption key dari file"""
    try:
        with open('secret.key', 'rb') as key_file:
            return key_file.read()
    except FileNotFoundError:
        print("⚠️ Key file tidak ditemukan, membuat key baru...")
        return generate_key()

# Inisialisasi Fernet cipher
cipher = Fernet(load_key())

def encrypt_data(data):
    """Enkripsi data string"""
    if data is None or data == "":
        return ""
    return cipher.encrypt(data.encode('utf-8'))

def decrypt_data(encrypted_data):
    """Dekripsi data"""
    if encrypted_data is None or encrypted_data == "" or encrypted_data == b"":
        return ""
    if isinstance(encrypted_data, str):
        encrypted_data = encrypted_data.encode('utf-8')
    return cipher.decrypt(encrypted_data).decode('utf-8')