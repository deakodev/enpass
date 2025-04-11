import os
from config import ENPASS_KEY_PATH
from cryptography.fernet import Fernet

def key_generate():
    return Fernet.generate_key()

def key_store(key):
    with open(ENPASS_KEY_PATH, "wb") as file:
        file.write(key)

def key_retrieve():
    if (os.path.exists(ENPASS_KEY_PATH)):
        return open(ENPASS_KEY_PATH, "rb").read()
    else:
        print(f"Error: Encryption key file {ENPASS_KEY_PATH} is missing.")
        return