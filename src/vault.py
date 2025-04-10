import json


def vault_store(packet, path):
    with open(path, "w") as file:
        json.dump(packet, file, indent=4)

