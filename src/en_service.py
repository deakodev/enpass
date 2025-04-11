from datetime import datetime, timezone
from typing import TypedDict

class PublicFields(TypedDict):
     name: str
     type: str | None
     link: str | None

class PrivateFields(TypedDict):
    encrypted_username: str
    encrypted_password: str

class ServicePacket(TypedDict):
    public: PublicFields
    private: PrivateFields
    updated_at: str

public_service_data = { "name": None, "type": None, "link": None }

def service_packet(encrypted_username, encrypted_password, public_fields) -> ServicePacket:
    return {
        "public": public_fields,
        "private": {
            "encrypted_username": encrypted_username.decode(),
            "encrypted_password": encrypted_password.decode()
        },
        "updated_at": datetime.now(timezone.utc).isoformat()
    }


