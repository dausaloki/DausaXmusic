from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
from ..logging import LOGGER

LOGGER(__name__).info("Initializing MongoDB client...")

try:
    # Motor treats None as its local default and defers network I/O. This lets
    # __main__.validate_required_config report a blank URI clearly instead of
    # exiting during import with a misleading success status.
    _mongo_async_ = AsyncIOMotorClient(
        MONGO_DB_URI or None,
        serverSelectionTimeoutMS=5000,
    )
    mongodb = _mongo_async_.DausaXmusic
except Exception as exc:
    # Do not print the URI or driver exception, which may contain credentials.
    LOGGER(__name__).error(
        "MongoDB client initialization failed (%s). Check MONGO_DB_URI format.",
        type(exc).__name__,
    )
    raise RuntimeError("Invalid MONGO_DB_URI configuration.") from None

LOGGER(__name__).info("MongoDB client initialized; connection is verified on first use.")
