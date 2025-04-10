

import argparse
import os
import time
from cli import password_confirmed_from_user
from config import *
from crypto import password_encrypt, password_decrypt
from key import key_generate, key_store, key_retrieve
from vault import vault_store


def main():
    parser = argparse.ArgumentParser(description="Enpass CLI")
    parser.add_argument("command", choices=["login", "set", "get", "init"], help="Command to execute")
    parser.add_argument("--account", help="The name of the service / account")
    parser.add_argument("--pass", help="The pass to store")
    parser.add_argument("--master", help="Master pass for login")

    args = parser.parse_args()

    if (args.command == "init"):
        print("Preparing Enpass...")
        enpass_key = key_generate()
        key_store(enpass_key, ENPASS_KEY_PATH)
        master = password_confirmed_from_user("Set master password: ")
        encrypted_master = password_encrypt(master, enpass_key)
        master_packet = {
            "service_name": "master",
            "encrypted_password": encrypted_master.decode(),
            "timestamp": int(time.time()),
        }
        vault_store(master_packet, ENPASS_VAULT_PATH)
        print("Enpass initialized!")
        return

    if (os.path.exists(ENPASS_KEY_PATH)):
        enpass_key = key_retrieve(ENPASS_KEY_PATH)
    else:
        print(f"Error: Encryption key file <{ENPASS_KEY_PATH}> is missing.")
        return
    
    match args.command:
        case "login":
            pass

    if (args.command == "login" and os.path.exists(ENPASS_VAULT_PATH)):
        pass
    else:
        pass


    print("enpass_key:", enpass_key.decode());


if __name__ == "__main__":
    main()