from dataclasses import dataclass
from datetime import datetime, timezone
from en_hash import password_verify


@dataclass
class MasterPacket:
    hashed_password: str | None = None
    updated_at: str | None = None


def master_packet(hashed_master: str) -> MasterPacket: 
    return MasterPacket(
        hashed_password=hashed_master,
        updated_at=datetime.now(timezone.utc).isoformat(),
    )


def master_confirm(password: str, hashed_password: str | None) -> bool:
    if not hashed_password:
        print("No master password found in vault.")
        return False

    return password_verify(password, hashed_password)
