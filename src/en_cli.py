import argparse
from getpass import getpass

from en_crypt import decrypt, encrypt
from en_hash import password_hash
from en_key import key_generate, key_retrieve, key_store
from en_master import master_packet
from en_result import Result
from en_service import PublicFields, service_packet, service_private_unpack, service_public_unpack
from en_session import session_active, session_start, session_end
from en_vault import vault_and_key, vault_master_confirm, vault_open, vault_save


# Prompt the user to confirm an action
def confirm(prompt: str = "Confirm? [Y/n]: ") -> bool:
    return input(prompt).strip().upper() == "Y"


# Parse command-line arguments
def cli_args() -> argparse.Namespace: 
    parser = argparse.ArgumentParser(description="Enpass CLI")
    commands = list(COMMAND_MAP.keys())

    parser.add_argument("command", choices=commands, help="Command to execute")
    parser.add_argument("-m", "--master", help="Master password for login")
    parser.add_argument("-n", "--name", help="Name of the service")

    return parser.parse_args()


# Setup vault master password and enpass key
def cli_init(_args) -> Result:
    vault = vault_open()

    # Check if already initialized
    if vault.master.hashed_password and key_retrieve():
        return Result.INIT_REDUNDANT

    print("🔐 Initializing Enpass...")

    # Generate and save new encryption key
    key_store(key_generate())

    # Prompt user to set master password
    while True:
        master_password = getpass("Set master password: ")
        master_password_confirm = getpass("Confirm password: ")
        if master_password == master_password_confirm:
            break
        print("❗ Passwords do not match. Please try again.")

    # Save hashed password to vault
    hashed_password = password_hash(master_password)
    vault.master = master_packet(hashed_password)
    is_saved = vault_save(vault)

    # Confirm setup completed successfully
    if is_saved and vault_open().master.hashed_password and key_retrieve():
        return Result.INIT_SUCCESS

    return Result.INIT_FAILED 


# Attempt login using master password, optional arg -m -master
def cli_login(args) -> Result:
    if session_active():
        return Result.LOGIN_REDUNDANT

    master_password = args.master or getpass("Enter master password: ")
    if vault_master_confirm(master_password) and session_start():
        return Result.LOGIN_SUCCESS

    return Result.LOGIN_FAILED


# End session 
def cli_logout(_args) -> Result:
    if session_end():
        return Result.LOGOUT_SUCCESS
    return Result.LOGOUT_REDUNDANT


# Add new service entry to the vault
def cli_add(_args) -> Result:
    if not session_active():
        return Result.SERVICE_ADDED_FAILED | Result.SESSION_INACTIVE

    vault_key = vault_and_key()
    if not vault_key:
        return Result.SERVICE_ADDED_FAILED

    vault, key = vault_key

    # Collect service metadata
    service_info = PublicFields(
        name=input("name*: "),
        type=input("type: ") or None,
        link=input("link: ") or None
    )

    username = input("username: ")
    password = input("password: ")

    # Encrypt credentials and package the service
    packet = service_packet(
        service_info,
        encrypted_username=encrypt(username, key),
        encrypted_password=encrypt(password, key)
    )

    # Confirm and save to vault
    if packet and confirm("Submit? [Y/n]: "):
        vault.services.append(packet)
        vault_save(vault)
        return Result.SERVICE_ADDED

    return Result.SERVICE_ADDED_FAILED


# Remove a service by name
def cli_remove(args) -> Result:
    if not session_active():
        return Result.SERVICE_REMOVED_FAILED | Result.SESSION_INACTIVE

    vault = vault_open() 

    if args.name and vault.services:
        # Filter out the service to remove
        vault.services = [
            s for s in vault.services if service_public_unpack(s).get("name") != args.name
        ]

        if confirm(f"Delete {args.name} data? [Y/n]: "):
            vault_save(vault)
            return Result.SERVICE_REMOVED

    return Result.SERVICE_REMOVED_FAILED


# List all saved services
def cli_list(_args) -> Result:
    if not session_active():
        return Result.SERVICE_LIST_FAILED | Result.SESSION_INACTIVE

    vault = vault_open()

    if vault.services:
        print(f"\n{'Name':<20}| {'Type':<15}| {'Link'}")
        print("-" * 60)
        for service in vault.services:
            info = service_public_unpack(service)
            name = info.get("name", "")
            type_ = info.get("type") or "None"
            link = info.get("link") or "None"
            print(f"{name:<20}| {type_:<15}| {link}")
        print("-" * 60, "\n")
        return Result.SERVICE_LIST

    return Result.SERVICE_LIST_FAILED


# View credentials for a service, requires -n --name <"service">
def cli_view(args) -> Result:
    if not session_active():
        return Result.SERVICE_VIEW_FAILED | Result.SESSION_INACTIVE

    vault_key = vault_and_key()

    if not vault_key or not args.name:
        return Result.SERVICE_VIEW_FAILED

    vault, key = vault_key

    for service in vault.services:
        info = service_public_unpack(service)
        if info.get("name") == args.name:
            private = service_private_unpack(service)
            print(f"username: {decrypt(private['encrypted_username'], key)}")
            print(f"password: {decrypt(private['encrypted_password'], key)}")
            return Result.SERVICE_VIEW

    print(f"No service found with name '{args.name}'")
    return Result.SERVICE_VIEW_FAILED


COMMAND_MAP = {
    "init": cli_init,
    "login": cli_login,
    "logout": cli_logout,
    "add": cli_add,
    "remove": cli_remove,
    "list": cli_list,
    "view": cli_view,
}
