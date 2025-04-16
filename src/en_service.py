from dataclasses import asdict, dataclass
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
    

def service_packet(service: PublicFields, encrypted_username, encrypted_password) -> ServicePacket:
    return ServicePacket(
        public=PublicFields(name=service.name, type=service.type, link=service.link),
        private=PrivateFields(encrypted_username=encrypted_username, encrypted_password=encrypted_password),
        updated_at=datetime.now(timezone.utc).isoformat()
    )


def service_public_unpack(service) -> dict:
    return service.public if isinstance(service.public, dict) else asdict(service.public)


def service_private_unpack(service) -> dict:
    return service.private if isinstance(service.private, dict) else asdict(service.private)

