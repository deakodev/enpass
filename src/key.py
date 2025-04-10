from cryptography.fernet import Fernet

def key_generate():
    return Fernet.generate_key()

def key_store(key, path):
    with open(path, "wb") as file:
        file.write(key)

def key_retrieve(path):
    return open(path, "rb").read()