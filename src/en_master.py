from datetime import datetime, timezone
from typing import TypedDict

class MasterPacket(TypedDict):
    hashed_password: str
    updated_at: str

def master_packet(hashed_master: str) -> MasterPacket: 
    return  {
        "hashed_password": hashed_master,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }