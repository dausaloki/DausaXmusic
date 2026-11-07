"""Optional, operator-authorized cookies for yt-dlp.

No cookie file is bundled. COOKIE_URL may point to the operator's own Netscape
cookie export over public HTTPS. Downloaded content is validated, stored outside
the repository with private permissions, and never written to logs.
"""

from __future__ import annotations

import atexit
import logging
import os
import shutil
import stat
import tempfile
import threading
import time
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import requests

import config
from DAUSAXMUSIC.security import validate_public_http_url


logger = logging.getLogger(__name__)
MAX_COOKIE_FILE_BYTES = 1024 * 1024
MAX_COOKIE_REDIRECTS = 3
COOKIE_DOWNLOAD_TIMEOUT = (5, 20)


class CookieProviderError(ValueError):
    """A safe, credential-free cookie configuration/download error."""


def _validate_cookie_url(url: str) -> str:
    if urlsplit(url).scheme.lower() != "https":
        raise CookieProviderError("COOKIE_URL must use HTTPS")
    try:
        # COOKIE_URL is itself secret-bearing configuration. The generic secret
        # containment check would therefore reject its own value, so only the
        # public-target validation is needed here.
        return validate_public_http_url(url, check_for_secrets=False)
    except Exception:
        raise CookieProviderError("COOKIE_URL must resolve to a public HTTPS host") from None


def _validate_netscape_cookie_content(content: bytes) -> None:
    if not content or len(content) > MAX_COOKIE_FILE_BYTES:
        raise CookieProviderError("cookie download is empty or too large")
    if b"\x00" in content:
        raise CookieProviderError("cookie download is not a text cookie file")
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise CookieProviderError("cookie download is not UTF-8 text") from None

    for raw_line in text.splitlines():
        line = raw_line.strip("\r\n")
        if not line.strip() or (line.startswith("#") and not line.startswith("#HttpOnly_")):
            continue
        fields = line.split("\t")
        if len(fields) != 7:
            continue
        domain, _include_subdomains, path, secure, expires, name, _value = fields
        if (
            domain
            and path.startswith("/")
            and secure.upper() in {"TRUE", "FALSE"}
            and expires.isdigit()
            and name
        ):
            return
    raise CookieProviderError("cookie download is not a valid Netscape cookie file")


def _write_private_cookie_file(content: bytes) -> tuple[str, str]:
    directory = tempfile.mkdtemp(prefix="dausaxmusic-cookies-")
    os.chmod(directory, stat.S_IRWXU)
    path = os.path.join(directory, "cookies.txt")
    try:
        descriptor = os.open(
            path,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            stat.S_IRUSR | stat.S_IWUSR,
        )
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
        return directory, path
    except Exception:
        shutil.rmtree(directory, ignore_errors=True)
        raise


def _download_cookie_file(url: str) -> tuple[str, str]:
    current_url = _validate_cookie_url(url)
    session = requests.Session()
    # Do not route a credentialed cookie export through ambient proxy settings.
    session.trust_env = False
    try:
        for redirect_count in range(MAX_COOKIE_REDIRECTS + 1):
            try:
                response = session.get(
                    current_url,
                    headers={
                        "Accept": "text/plain, application/octet-stream, */*;q=0.1",
                        "User-Agent": "DausaXmusic/authorized-cookie-loader/1.0",
                    },
                    allow_redirects=False,
                    stream=True,
                    timeout=COOKIE_DOWNLOAD_TIMEOUT,
                )
            except requests.RequestException:
                raise CookieProviderError("cookie download request failed") from None

            try:
                if response.status_code in {301, 302, 303, 307, 308}:
                    if redirect_count >= MAX_COOKIE_REDIRECTS:
                        raise CookieProviderError("too many cookie download redirects")
                    location = response.headers.get("Location")
                    if not location:
                        raise CookieProviderError("cookie download redirect has no destination")
                    current_url = _validate_cookie_url(urljoin(current_url, location))
                    continue

                if response.status_code != 200:
                    raise CookieProviderError(
                        f"cookie download returned HTTP {response.status_code}"
                    )
                content_length = response.headers.get("Content-Length")
                if content_length:
                    try:
                        declared_size = int(content_length)
                    except ValueError:
                        declared_size = 0
                    if declared_size > MAX_COOKIE_FILE_BYTES:
                        raise CookieProviderError("cookie download is too large")

                content = bytearray()
                for chunk in response.iter_content(chunk_size=16 * 1024):
                    if not chunk:
                        continue
                    content.extend(chunk)
                    if len(content) > MAX_COOKIE_FILE_BYTES:
                        raise CookieProviderError("cookie download is too large")
                _validate_netscape_cookie_content(bytes(content))
                return _write_private_cookie_file(bytes(content))
            finally:
                response.close()
    finally:
        session.close()

    raise CookieProviderError("cookie download failed")


class YouTubeCookieProvider:
    """Cache one operator-supplied cookie file and retry failures sparingly."""

    def __init__(self, failure_retry_seconds: int = 300):
        self.failure_retry_seconds = max(0, int(failure_retry_seconds))
        self._lock = threading.Lock()
        self._source_url = ""
        self._directory = None
        self._path = None
        self._retry_after = 0.0

    def _clear_locked(self) -> None:
        if self._directory:
            shutil.rmtree(self._directory, ignore_errors=True)
        self._directory = None
        self._path = None

    def get(self, url: str) -> str | None:
        source_url = (url or "").strip()
        if not source_url:
            return None

        with self._lock:
            if source_url == self._source_url:
                if self._path and Path(self._path).is_file():
                    return self._path
                if time.monotonic() < self._retry_after:
                    return None
            else:
                self._clear_locked()

            self._source_url = source_url
            try:
                self._directory, self._path = _download_cookie_file(source_url)
                self._retry_after = 0.0
                logger.info("Authorized YouTube cookie file loaded from COOKIE_URL.")
                return self._path
            except Exception as exc:
                self._clear_locked()
                self._retry_after = time.monotonic() + self.failure_retry_seconds
                reason = (
                    str(exc)
                    if isinstance(exc, CookieProviderError)
                    else type(exc).__name__
                )
                logger.warning(
                    "COOKIE_URL could not be loaded; continuing without cookies (%s).",
                    reason,
                )
                return None

    def cleanup(self) -> None:
        with self._lock:
            self._clear_locked()
            self._source_url = ""


_PROVIDER = YouTubeCookieProvider()
atexit.register(_PROVIDER.cleanup)


def get_youtube_cookie_file() -> str | None:
    """Return a private cookie file only when the operator configured COOKIE_URL."""

    return _PROVIDER.get(getattr(config, "COOKIE_URL", ""))
