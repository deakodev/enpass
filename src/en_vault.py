
from dataclasses import dataclass
import json
import os
from pathlib import Path
from en_config import ENPASS_VAULT_PATH 
from en_hash import password_verify
from en_master import MasterPacket
from en_service import ServicePacket

@dataclass
class Vault:
    master: MasterPacket
    services: list[ServicePacket]
  
def vault_open() -> Vault:
    filepath = Path(ENPASS_VAULT_PATH) 
    if not filepath.exists():
        filepath.parent.mkdir(parents=True, exist_ok=True)
        filepath.write_text(json.dumps(Vault(MasterPacket(), [])))

    try:
        with filepath.open("r") as file: 
            vault = json.load(file)
            return vault
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"[Error] Unable to read vault: {error}")
        return Vault(MasterPacket(), [])
    
def vault_master_retrieve() -> str | None:
    hashed_password = None
    vault = vault_open()
    if vault:
        hashed_password = vault.master.get("hashed_password") if isinstance(vault.master, dict) else None
    if hashed_password:
        return hashed_password
    return None

def vault_master_confirm(password: str) -> bool:
    hashed_password = vault_master_retrieve()
    if hashed_password:
        is_confirmed = password_verify(password, hashed_password)
        return is_confirmed
    print("No master password found in vault.")
    return False

def vault_service_store(packet: ServicePacket):
    pass
    # service_name = packet["public"]["name"]
    # with open(ENPASS_VAULT_PATH, "r") as file:
    #     vault_dict = json.load(file)
    # vault_dict[service_name] = packet
    # with open(ENPASS_VAULT_PATH, "w") as file:
    #     json.dump(vault_dict, file, indent=4) 


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

