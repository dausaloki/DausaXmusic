import os
import asyncio

CPU = os.cpu_count() or 4


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or not str(raw).strip():
        return default
    try:
        return int(raw)
    except (TypeError, ValueError):
        raise RuntimeError(f"Environment variable {name} must be an integer.") from None


MAX_CONCURRENT = _env_int("MAX_CONCURRENT", min(64, CPU * 8))
CHUNK_SIZE = _env_int("CHUNK_SIZE", 64 * 1024)

YTDLP_TIMEOUT = _env_int("YTDLP_TIMEOUT", 45)
YOUTUBE_META_TTL = _env_int("YOUTUBE_META_TTL", 300)
YOUTUBE_META_MAX = _env_int("YOUTUBE_META_MAX", 2048)

SEM = asyncio.Semaphore(MAX_CONCURRENT)
