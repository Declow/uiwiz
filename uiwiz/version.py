import importlib.metadata

__version__: str = "0.0.0"  # Default version in case metadata is not available
try:
    # Attempt to get the version from the package metadata
    __version__ = importlib.metadata.version("uiwiz").replace("+", ".")
except importlib.metadata.PackageNotFoundError:
    # If the package is not found, keep the default version
    pass
# __version__: str = importlib.metadata.version("uiwiz").replace("+", ".")
