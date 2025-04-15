import argparse
from dataclasses import asdict
from getpass import getpass
import json

from en_crypt import encrypt
from en_hash import password_hash
from en_key import key_generate, key_retrieve, key_store
from en_master import master_packet
from en_result import Result
from en_service import PublicFields, ServicePacket, service_packet
from en_session import session_active, session_start, session_end
from en_vault import vault_master_confirm, vault_open, vault_save

def user_confirmed_input(message):
    while True:
        value = getpass(message)
        value_confirm = getpass("Confirm: ")
        if value == value_confirm:
            return value
        else:
            print("Input does not match. Please try again.")

def cli_args() -> argparse.Namespace: 
    parser = argparse.ArgumentParser(description="Enpass CLI")
    commands = list(COMMAND_MAP.keys())
    parser.add_argument("command", choices=commands, help="Command to execute")
    
    parser.add_argument("-m", "--master", help="Master password for login")

    return parser.parse_args()

def cli_init(_args) -> Result:
    vault = vault_open()

    if vault.master.hashed_password and key_retrieve():
        return Result.INIT_REDUNDANT

    print("Initializing Enpass...")
    key_store(key_generate())

    master_password = user_confirmed_input("Set master password: ")
    hashed_password = password_hash(master_password)

    vault.master = master_packet(hashed_password)
    vault_save(vault)

    return Result.INIT_SUCCESS


def cli_login(args) -> Result:
    if session_active():
        return Result.LOGIN_REDUNDANT

    master_password = args.master if args.master else getpass("Enter master password: ")

    if vault_master_confirm(master_password):
        return session_start()

    return Result.LOGIN_FAILED


def cli_logout(_args) -> Result:
    return session_end()


def cli_reset(_args) -> Result:


    return Result.RESET_SUCCESS


def cli_list(_args) -> Result:
    if not session_active():
        return Result.SERVICE_ADDED_FAILED | Result.SESSION_INACTIVE

    vault = vault_open()
    if vault.services:
        # Print header
        print(f"\n{'Name':<20}| {'Type':<15}| {'Link'}")
        print("-" * 60)

        # Print rows
        for service in vault.services:
            service_info = service.public if isinstance(service.public, dict) else asdict(service.public)
            name = service_info['name']
            type_ = service_info['type']
            link = service_info['link']
            print(f"{name:<20}| {type_:<15}| {link}")
        print("-" * 60, "\n")
        return Result.SERVICE_LIST

    return Result.SERVICE_LIST_FAILED



def cli_add(_args) -> Result:
    if not session_active():
        return Result.SERVICE_ADDED_FAILED | Result.SESSION_INACTIVE
    
    service_info = PublicFields(
        name=input("name*: "),
        type=input("type: ") or None,
        link=input("link: ") or None,
    )

    vault = vault_open()
    enpass_key = key_retrieve()
    if vault.master.hashed_password is None or enpass_key is None:
        return Result.SERVICE_ADDED_FAILED

    username = input("username: ")
    encrypted_username = encrypt(username, enpass_key)
    password = input("password: ")
    encrypted_password = encrypt(password, enpass_key)

    packet = service_packet(service_info, encrypted_username, encrypted_password)
    is_confirmed = "Y" == input("Submit? [Y/n]: ")

    if packet and is_confirmed:
        vault.services.append(packet)
        vault_save(vault)
        return Result.SERVICE_ADDED

    return Result.SERVICE_ADDED_FAILED
 

def cli_remove(_args) -> Result:


    return Result.SERVICE_REMOVED


def cli_update(_args) -> Result:


    return Result.SERVICE_UPDATED


COMMAND_MAP = {
    "init": cli_init,
    "login": cli_login,
    "logout": cli_logout,
    "reset": cli_reset,
    "list": cli_list,
    "add": cli_add,
    "remove": cli_remove,
    "update": cli_update,
}