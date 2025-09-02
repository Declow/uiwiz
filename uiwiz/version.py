import importlib.metadata

__version__: str = "0.0.0"
try:
    # Could fail during development
    __version__ = importlib.metadata.version("uiwiz").replace("+", ".")
except importlib.metadata.PackageNotFoundError:
    pass
