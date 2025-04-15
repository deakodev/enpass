from cryptography.fernet import Fernet

# [raw] is to be encrypted using [key]
def encrypt(raw: str, key: str) -> str:
    fernet = Fernet(key)
    encrypted_str = fernet.encrypt(raw.encode()).decode()
    return encrypted_str

# [encryption] is to be decrypted using [key]
def decrypt(encryption: str, key: str) -> str:
    fernet = Fernet(key)
    raw_str = fernet.decrypt(encryption).decode()
    return raw_str 