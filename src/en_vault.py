from dataclasses import asdict, dataclass
import json
from pathlib import Path

from en_config import ENPASS_VAULT_PATH 
from en_master import MasterPacket, master_confirm
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


def vault_save(vault: Vault):
    filepath = Path(ENPASS_VAULT_PATH)
    with filepath.open("w") as file:
        json.dump(asdict(vault), file, indent=4)


def vault_master_confirm(password: str) -> bool:
    vault = vault_open()
    return master_confirm(password, vault.master.hashed_password)
