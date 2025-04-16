from datetime import datetime
import json

from en_config import ENPASS_SESSION_PATH, ENPASS_SESSION_TIMEOUT


def session_start() -> bool:
    expires_at = (datetime.now() + ENPASS_SESSION_TIMEOUT).isoformat()
    try:
        with open(ENPASS_SESSION_PATH, "w") as f:
            json.dump({"expires_at": expires_at}, f)
        return True
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"[Error] Unable to read vault: {error}")
        return False


def session_active() -> bool:
    if not ENPASS_SESSION_PATH.exists():
        return False
    try: 
        with open(ENPASS_SESSION_PATH, "r") as f:
            data = json.load(f)
        expires_at = datetime.fromisoformat(data.get("expires_at", ""))
        return datetime.now() < expires_at
    except Exception:
        return False 


def session_end() -> bool:
    if ENPASS_SESSION_PATH.exists():
        ENPASS_SESSION_PATH.unlink()
        return True
    else: 
        return False
 