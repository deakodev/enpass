from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class MasterPacket:
    hashed_password: str | None = None
    updated_at: str | None = None

def master_packet(hashed_master: str) -> MasterPacket: 
    return MasterPacket(
        hashed_password=hashed_master,
        updated_at=datetime.now(timezone.utc).isoformat(),
    )