import base64
import bcrypt
from cryptography.fernet import Fernet

def password_hash(password_str: str) -> str:
    hashed_bytes = bcrypt.hashpw(password_str.encode(), bcrypt.gensalt())
    hashed_str = base64.b64encode(hashed_bytes).decode("utf-8")
    return hashed_str

def password_verify(password_str: str, hashed_str: str) -> bool:
    try:
        hashed_bytes = base64.b64decode(hashed_str)
        return bcrypt.checkpw(password_str.encode(), hashed_bytes)
    except Exception as e:
        print(f"Password verification failed: {e}")
        return False

# [raw_str] is to be encrypted using [key_str]
def encrypt(raw_str: str, key_str: str) -> str:
    fernet = Fernet(key_str)
    encrypted_str = fernet.encrypt(raw_str.encode()).decode()
    return encrypted_str

# [encrypted_str] is to be decrypted using [key_str]
def decrypt(encrypted_str: str, key_str: str) -> str:
    fernet = Fernet(key_str)
    raw_str = fernet.decrypt(encrypted_str).decode()
    return raw_str 