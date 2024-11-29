from pathlib import Path
from typing import Callable, Dict

resources: Dict[str, Path] = {}
page_map: Dict[Callable, str] = {}


def register_resource(key: str, resource: Path):
    resources[key] = resource


def register_path(key: str, func: Callable):
    page_map[func] = key


def route_exists(path: str) -> bool:
    return path in list(page_map.values())
