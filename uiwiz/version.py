import importlib.metadata

__version__: str = importlib.metadata.version("uiwiz").replace("+", ".")
