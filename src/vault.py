
import json
from datetime import datetime, timezone
from typing import TypedDict
from config import ENPASS_VAULT_PATH
from password import password_verify

class MasterPacket(TypedDict):
    password: str
    updated_at: str

class Service(TypedDict):
    name: str | None
    type: str | None
    link: str | None
    
service = { "name": None, "type": None, "link": None }


def vault_service_packet(encrypted_username, encrypted_password, service=service): 
    return  {
            "service": service,
            "encrypted_username": encrypted_username.decode(),
            "encrypted_password": encrypted_password.decode(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }


def vault_master_packet(hash_str: str) -> MasterPacket: 
    return  {
            "password": hash_str,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }


def vault_service_store(packet):
    service_name = packet["service"]["name"]
    with open(ENPASS_VAULT_PATH, "r") as file:
        vault_dict = json.load(file)
    vault_dict[service_name] = packet
    with open(ENPASS_VAULT_PATH, "w") as file:
        json.dump(vault_dict, file, indent=4) 


def vault_master_store(packet):
    try:
        with open(ENPASS_VAULT_PATH, "r") as file:
            vault_dict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(e)
        vault_dict = {}
    
    vault_dict["master"] = packet

    with open(ENPASS_VAULT_PATH, "w") as file:
        json.dump(vault_dict, file, indent=4) 


def vault_master_confirm(password_str):
    try:
        with open(ENPASS_VAULT_PATH, "r") as file:
            vault_dict = json.load(file)

        password_hash_str = vault_dict.get("master", {}).get("password")

        if not password_hash_str:
            print("No master password found in vault.")
            return False

        return password_verify(password_str, password_hash_str)

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Vault read error: {e}")
        return False
