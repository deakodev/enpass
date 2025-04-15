import argparse
import getpass

from en_hash import password_hash
from en_key import key_generate, key_retrieve, key_store
from en_master import master_packet
from en_result import Result
from en_vault import vault_master_confirm, vault_master_retrieve, vault_master_store
from en_session import session_valid, session_start, session_end

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

def cli_args() -> argparse.Namespace: 
    parser = argparse.ArgumentParser(description="Enpass CLI")
    commands = list(command_map.keys())
    parser.add_argument("command",  choices=commands, help="Command to execute")
    
    parser.add_argument("-m", "--master", help="Master password for login")

    return parser.parse_args()

def cli_init(_args) -> Result:
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
    if session_valid():
        return Result.LOGIN_REDUNDANT

    if master_password is None:
        from getpass import getpass
        master_password = getpass("Enter master password: ")

    if vault_master_confirm(master_password):
        return session_start()
    return Result.LOGIN_FAILED


def cli_logout(_args) -> Result:
    return session_end()


def cli_reset(_args) -> Result:


    return Result.RESET_SUCCESS


def cli_list(_args) -> Result:
    
    
    return Result.SERVICE_LIST


def cli_add(_args) -> Result:


    return Result.SERVICE_ADDED


def cli_remove(_args) -> Result:


    return Result.SERVICE_REMOVED


def cli_update(_args) -> Result:


    return Result.SERVICE_UPDATED


command_map = {
    "init": cli_init,
    "login": cli_login,
    "logout": cli_logout,
    "reset": cli_reset,
    "list": cli_list,
    "add": cli_add,
    "remove": cli_remove,
    "update": cli_update,
}