from datetime import timedelta
from pathlib import Path

ENPASS_KEY_PATH = "bin/enpass.key"
ENPASS_VAULT_PATH = "bin/vault.json"
ENPASS_SESSION_PATH = Path.home() / ".session" 


ENPASS_SESSION_TIMEOUT = timedelta(minutes=10)