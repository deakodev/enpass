from en_config import ENPASS_SESSION_PATH, ENPASS_SESSION_TIMEOUT
from datetime import datetime
import json

def login():
    expires_at = (datetime.now() + ENPASS_SESSION_TIMEOUT).isoformat()
    with open(ENPASS_SESSION_PATH, "w") as f:
        json.dump({"expires_at": expires_at}, f)


def is_logged_in() -> bool:
    if not ENPASS_SESSION_PATH.exists():
        return False

    try: 
        with open(ENPASS_SESSION_PATH, "r") as f:
            data = json.load(f)
        expires_at = datetime.fromisoformat(data.get("expires_at", ""))
        return datetime.now() < expires_at
    except Exception:
        return False 


def logout():
    if ENPASS_SESSION_PATH.exists():
        ENPASS_SESSION_PATH.unlink()
 