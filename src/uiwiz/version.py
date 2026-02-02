import contextlib
import importlib.metadata

__version__: str = "0.0.0"

with contextlib.suppress(importlib.metadata.PackageNotFoundError):
    __version__ = importlib.metadata.version("uiwiz").replace("+", ".")
