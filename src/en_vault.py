from dataclasses import asdict, dataclass
import json
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
        empty_vault = asdict(Vault(MasterPacket(), []))
        filepath.write_text(json.dumps(empty_vault))

    try:
        with filepath.open("r") as file:
            data = json.load(file)
            return Vault(
                master=MasterPacket(**data.get("master", {})),
                services=[ServicePacket(**s) for s in data.get("services", [])]
            )
    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"[Error] Unable to read vault: {error}")
        return Vault(MasterPacket(), [])


def vault_master_retrieve() -> str | None:
    return vault_open().master.hashed_password or None


def vault_master_store(packet: MasterPacket):
    filepath = Path(ENPASS_VAULT_PATH)
    
    try:
        with filepath.open("r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data["master"] = asdict(packet)

    with filepath.open("w") as file:
        json.dump(data, file, indent=4)


def vault_master_confirm(password: str) -> bool:
    hashed_password = vault_master_retrieve()
    
    if not hashed_password:
        print("No master password found in vault.")
        return False

    return password_verify(password, hashed_password)
