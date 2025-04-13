from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class PublicFields:
    name: str
    type: str | None
    link: str | None

@dataclass
class PrivateFields:
    encrypted_username: str
    encrypted_password: str

@dataclass 
class ServicePacket:
    public: PublicFields
    private: PrivateFields
    updated_at: str

def service_packet(encrypted_username, encrypted_password, service: PublicFields) -> ServicePacket:
    return ServicePacket(
        public=PublicFields(name=service.name, type=service.type, link=service.link),
        private=PrivateFields(encrypted_username=encrypted_username.decode(), encrypted_password=encrypted_password.decode()),
        updated_at=datetime.now(timezone.utc).isoformat()
    )


