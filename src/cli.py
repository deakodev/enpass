import argparse
from argparse import Namespace
import getpass

from password import encrypt, password_hash
from key import key_generate, key_retrieve, key_store
from vault import vault_master_confirm, vault_master_packet, vault_master_store

def user_input(message):
    return getpass.getpass(message)

def user_confirmed_input(message):
    while True:
        value = user_input(message)
        value_confirm = user_input("Confirm: ")
        if value == value_confirm:
            return value
        else:
            print("Input does not match. Please try again.")

def cli_args() -> Namespace | None:
    parser = argparse.ArgumentParser(description="Enpass CLI")
    parser.add_argument("command", choices=["login", "set", "get", "init"], help="Command to execute")
    parser.add_argument("--master", help="Master pass for login")
    return parser.parse_args()

def cli_init() -> str | None:
    print("Initializing Enpass...")
    enpass_key = key_generate() 
    key_store(enpass_key)

    master_provided = user_confirmed_input("Set master password: ")
    master_hash_str = password_hash(master_provided)

    master_packet = vault_master_packet(master_hash_str)
    vault_master_store(master_packet)
    return f'Enpass initialized!'

def cli_login(master_arg: str | None = None) -> str | None:
    enpass_key = key_retrieve()
    if not enpass_key:
        print(f"[Error] Encryption key not found.")
        return None
    
    master_provided = user_input("Enter master password: ")
  
    if vault_master_confirm(master_provided):
        print("cli_login")
    return None
