# Task 4: AES-256 File Encryption/Decryption
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

def pad(data):
    return data + b" " * (16 - len(data) % 16)

def encrypt_file(filename, key):
    cipher = AES.new(key, AES.MODE_ECB)
    with open(filename, 'rb') as f:
        data = f.read()
    encrypted = cipher.encrypt(pad(data))
    with open(filename + ".enc", 'wb') as f:
        f.write(encrypted)
    print("File encrypted:", filename + ".enc")

def decrypt_file(filename, key):
    cipher = AES.new(key, AES.MODE_ECB)
    with open(filename, 'rb') as f:
        encrypted = f.read()
    decrypted = cipher.decrypt(encrypted).rstrip(b" ")
    with open(filename.replace(".enc", ".dec"), 'wb') as f:
        f.write(decrypted)
    print("File decrypted:", filename.replace(".enc", ".dec"))

# Example:
# key = get_random_bytes(32)  # Save this key securely!
# encrypt_file("secret.txt", key)
# decrypt_file("secret.txt.enc", key)
