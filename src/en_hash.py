import base64
import bcrypt


def password_hash(password: str) -> str:
    hashed_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    hashed_password = base64.b64encode(hashed_bytes).decode("utf-8")
    return hashed_password


def password_verify(password: str, hashed_password: str) -> bool:
    try:
        hashed_bytes = base64.b64decode(hashed_password)
        return bcrypt.checkpw(password.encode(), hashed_bytes)
    except Exception as error:
        print(f"Password verification failed: {error}")
        return False
