
import json
from en_config import ENPASS_VAULT_PATH
from en_hash import password_verify
from en_master import MasterPacket
from en_service import ServicePacket

def vault_service_store(packet: ServicePacket):
    service_name = packet["public"]["name"]
    with open(ENPASS_VAULT_PATH, "r") as file:
        vault_dict = json.load(file)
    vault_dict[service_name] = packet
    with open(ENPASS_VAULT_PATH, "w") as file:
        json.dump(vault_dict, file, indent=4) 


def vault_master_store(packet: MasterPacket):
    try:
        with open(ENPASS_VAULT_PATH, "r") as file:
            vault_dict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(e)
        vault_dict = {}
    
    vault_dict["master"] = packet

    with open(ENPASS_VAULT_PATH, "w") as file:
        json.dump(vault_dict, file, indent=4) 


def vault_master_confirm(password: str):
    try:
        with open(ENPASS_VAULT_PATH, "r") as file:
            vault_dict = json.load(file)

        password_hash_str = vault_dict.get("master", {}).get("password")

        if not password_hash_str:
            print("No master password found in vault.")
            return False

        return password_verify(password, password_hash_str)

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Vault read error: {e}")
        return False
