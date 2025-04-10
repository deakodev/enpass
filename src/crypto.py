from cryptography.fernet import Fernet

def password_encrypt(password, key):
    fernet = Fernet(key)
    return fernet.encrypt(password.encode())

def password_decrypt(password, key):
    fernet = Fernet(key)
    return fernet.decrypt(password).decode()