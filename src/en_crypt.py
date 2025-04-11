from cryptography.fernet import Fernet

# [raw_str] is to be encrypted using [key_str]
def encrypt(raw: str, key: str) -> str:
    fernet = Fernet(key)
    encrypted_str = fernet.encrypt(raw.encode()).decode()
    return encrypted_str

# [encrypted_str] is to be decrypted using [key_str]
def decrypt(encryption: str, key: str) -> str:
    fernet = Fernet(key)
    raw_str = fernet.decrypt(encryption).decode()
    return raw_str 