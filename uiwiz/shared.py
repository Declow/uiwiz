from pathlib import Path

resources = {}


def register_resource(key: str, resource: Path):
    resources[key] = resource
