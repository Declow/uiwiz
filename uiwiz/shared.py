import hashlib
import inspect
from functools import lru_cache
from pathlib import Path
from typing import Callable, Dict, Optional

resources: Dict[str, Path] = {}
page_map: Dict[Callable, str] = {}


@lru_cache(maxsize=None)
def hash_function_extended(func):
    """
    This was an interesting problem. I needed to hash the function
    to be able to store the route in a dictionary. Nothing special
    but the reason for using the source code has to do with
    uvicorn and multiple workers. The function object is not the
    same in different workers, so I had to use the source code
    to generate a hash that would be the same in all workers.
    """
    try:
        source = inspect.getsource(func) + func.__name__
    except (TypeError, OSError):
        # Fallback for built-in functions or functions without source code
        source = f"{func.__module__}.{func.__qualname__}"
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def register_resource(key: str, resource: Path):
    resources[key] = resource


def register_path(key: str, func: Callable):
    page_map[hash_function_extended(func)] = key


def fetch_route(func: Callable) -> Optional[str]:
    return page_map.get(hash_function_extended(func))


def reset_resources():
    resources.clear()
    page_map.clear()


def route_exists(path: str) -> bool:
    return path in list(page_map.values())
