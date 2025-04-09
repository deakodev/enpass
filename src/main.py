

import argparse
import os
from cryptography.fernet import Fernet

def key_generate(path):
    key = Fernet.generate_key()
    with open(path, "wb") as file:
        file.write(key)

def key_retrieve(path):
    return open(path, "rb").read()

ENPASS_KEY_PATH = "enpass.key"

def main():
    parser = argparse.ArgumentParser(description="Enpass CLI")
    parser.add_argument("command", choices=["login", "set", "get", "init"], help="Command to execute")
    parser.add_argument("--account", help="The name of the service / account")
    parser.add_argument("--pass", help="The pass to store")
    parser.add_argument("--master", help="Master pass for login")

    args = parser.parse_args()

    if (args.command == "init"):
        key_generate(ENPASS_KEY_PATH)
        print("Enpass initialized!")
        return

    if (os.path.exists("enpass.key")):
        enpass_key = key_retrieve(ENPASS_KEY_PATH)
    else:
        print(f"Error: Encryption key file {ENPASS_KEY_PATH} is missing.")
        return

    print("enpass_key:", enpass_key.decode());


if __name__ == "__main__":
    main()