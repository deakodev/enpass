import argparse
from argparse import Namespace
import getpass

from en_hash import password_hash
from en_key import key_generate, key_retrieve, key_store
from en_master import master_packet
from en_result import Result
from en_vault import vault_master_confirm, vault_master_retrieve, vault_master_store

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

def cli_args() -> Namespace: 
    parser = argparse.ArgumentParser(description="Enpass CLI")
    parser.add_argument("command", choices=["init", "login", "set", "get"], help="Command to execute")
    parser.add_argument("--master", help="Master password for login")
    return parser.parse_args()

def cli_init() -> Result:
    # determine if already initialized
    enpass_key = key_retrieve()
    master_hashed_password = vault_master_retrieve()
    if enpass_key and master_hashed_password:
        return Result.INIT_REDUNDANT

    print("Initializing Enpass...")
    enpass_key = key_generate() 
    key_store(enpass_key)

    master_provided_password = user_confirmed_input("Set master password: ")
    master_hashed_password = password_hash(master_provided_password)

    packet = master_packet(master_hashed_password)
    vault_master_store(packet)
    return Result.INIT_SUCCESS

def cli_login(master_password: str | None = None) -> Result:
    if master_password is None:
        master_password = user_input("Enter master password: ")
    if vault_master_confirm(master_password):
        print("cli_login") 
        return Result.LOGIN_SUCCESS
    return Result.LOGIN_FAILED
