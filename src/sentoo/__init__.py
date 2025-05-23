import importlib.metadata

from .client import Sentoo
from .async_client import AsyncSentoo

try:
    __version__ = importlib.metadata.version(__name__)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0"  # Fallback for development mode


__all__ = ["Sentoo", "AsyncSentoo"]
