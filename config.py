import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

# Load environment variables from .env file
load_dotenv()

def _int_env(name: str, default: int) -> int:
    raw = getenv(name)
    if raw is None or not str(raw).strip():
        return default
    try:
        return int(raw)
    except (TypeError, ValueError):
        raise RuntimeError(f"Environment variable {name} must be an integer.") from None


# ── DausaXmusic identity and core bot config ───────────────────────────────────
PROJECT_NAME = "DausaXmusic"
PROJECT_VERSION = "1.0.1"

API_ID = _int_env("API_ID", 0)
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN")

OWNER_NAME = getenv("OWNER_NAME", "𝐋𝐎𝐊𝐄𝐒𝐇 𝐃𝐀𝐔𝐒𝐀")
OWNER_ID = _int_env("OWNER_ID", 1236703127)
OWNER_USERNAME = getenv("OWNER_USERNAME", "lokesh_dausa").lstrip("@")
BOT_USERNAME = getenv("BOT_USERNAME", "DAUSA_MUSIC1_BOT").lstrip("@")
BOT_NAME = getenv("BOT_NAME", "⏤͟͞• ˹𝚀𝚄𝙴𝙴𝙽 ✘ ᴍᴜsɪᴄ˼🫧")
ASSUSERNAME = getenv("ASSUSERNAME", "")

# ── Database & logging ─────────────────────────────────────────────────────────
MONGO_DB_URI = getenv("MONGO_DB_URI")
LOGGER_ID = _int_env("LOGGER_ID", 0)

# ── Limits (durations in min/sec; sizes in bytes) ──────────────────────────────
DURATION_LIMIT_MIN = _int_env("DURATION_LIMIT", 300)
SONG_DOWNLOAD_DURATION = _int_env("SONG_DOWNLOAD_DURATION", 1200)
SONG_DOWNLOAD_DURATION_LIMIT = _int_env("SONG_DOWNLOAD_DURATION_LIMIT", 1800)
TG_AUDIO_FILESIZE_LIMIT = _int_env("TG_AUDIO_FILESIZE_LIMIT", 157286400)
TG_VIDEO_FILESIZE_LIMIT = _int_env("TG_VIDEO_FILESIZE_LIMIT", 1288490189999)
QUEUE_LIMIT = _int_env("QUEUE_LIMIT", 10)
PLAYLIST_FETCH_LIMIT = _int_env("PLAYLIST_FETCH_LIMIT", QUEUE_LIMIT)

# ── External APIs ──────────────────────────────────────────────────────────────
API_URL = getenv("API_URL")        # optional
API_KEY = getenv("API_KEY")        # optional
DEEP_API = getenv("DEEP_API")      # optional
REPLICATE_API_TOKEN = getenv("REPLICATE_API_TOKEN")  # optional
REPLICATE_API_TOKENS = getenv("REPLICATE_API_TOKENS", "")  # optional comma-separated pool
GENVID_USE_PUBLIC_FALLBACKS = getenv("GENVID_USE_PUBLIC_FALLBACKS", "0")
HF_TOKEN = getenv("HF_TOKEN")  # optional
HF_TOKENS = getenv("HF_TOKENS", "")  # optional comma-separated pool
OCR_SPACE_API_KEY = getenv("OCR_SPACE_API_KEY", "")  # optional shared free key
ELITE_LLM_API_BASE = getenv("ELITE_LLM_API_BASE", "")
ELITE_LLM_API_KEY = getenv("ELITE_LLM_API_KEY", "")
ESSE_API_URL = getenv("ESSE_API_URL", "")
ESSE_API_KEY = getenv("ESSE_API_KEY", "")
ESSE_TIMEOUT = getenv("ESSE_TIMEOUT", "20")
PHONE_LOOKUP_API_KEY = getenv("PHONE_LOOKUP_API_KEY", "")
IPINFO_TOKEN = getenv("IPINFO_TOKEN", "")
IPQUALITYSCORE_API_KEY = getenv("IPQUALITYSCORE_API_KEY", "")

# Optional operator-authorized YouTube cookie export (never bundled).
COOKIE_URL = getenv("COOKIE_URL", "")

# Vars For API End Pont.
YTPROXY_URL = getenv("YTPROXY_URL", "") ## Optional xBit fallback endpoint.
YT_API_KEY = getenv("YT_API_KEY" , None ) ## Optional xBit API key like: xbit_10000000xx0233

# ── Hosting / deployment ───────────────────────────────────────────────────────
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# ── Git / updates ──────────────────────────────────────────────────────────────
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "")
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN")  # needed if repo is private

# ── Official DausaXmusic links ────────────────────────────────────────────────
INSTAGRAM_URL = getenv("INSTAGRAM_URL", "https://instagram.com/lokesh_dausa1")
WELCOME_IMAGE_PATH = "DAUSAXMUSIC/assets/branding/welcome-banner.png"
PLAYER_BRANDING_REFERENCE = "DAUSAXMUSIC/assets/thumb/player/dausaxmusic-cyan-reference.png"
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/kalam_se")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/DAUSA_123")

# ── Assistant auto-leave ───────────────────────────────────────────────────────
ASSISTANT_JOIN_CHATS = getenv("ASSISTANT_JOIN_CHATS", "")
AUTO_LEAVING_ASSISTANT = True
AUTO_LEAVE_ASSISTANT_TIME = _int_env("ASSISTANT_LEAVE_TIME", 15000)

# ── Debug ──────────────────────────────────────────────────────────────────────
DEBUG_IGNORE_LOG = True

# ── Spotify (optional) ─────────────────────────────────────────────────────────
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "")

# ── Session strings (optional) ─────────────────────────────────────────────────
STRING1 = getenv("STRING_SESSION")
STRING2 = getenv("STRING_SESSION2")
STRING3 = getenv("STRING_SESSION3")
STRING4 = getenv("STRING_SESSION4")
STRING5 = getenv("STRING_SESSION5")

# ── Media assets ───────────────────────────────────────────────────────────────
START_VIDS = [
    "https://files.catbox.moe/1jcn1p.mp4",
    "https://files.catbox.moe/1jcn1p.mp4",
    "https://files.catbox.moe/1jcn1p.mp4",
]
STICKERS = [
    "CAACAgUAAx0Cd6nKUAACASBl_rnalOle6g7qS-ry-aZ1ZpVEnwACgg8AAizLEFfI5wfykoCR4h4E",
    "CAACAgUAAx0Cd6nKUAACATJl_rsEJOsaaPSYGhU7bo7iEwL8AAPMDgACu2PYV8Vb8aT4_HUPHgQ",
]
HELP_IMG_URL = "https://files.catbox.moe/22oahi.jpg"
PING_VID_URL = "https://files.catbox.moe/5z1qte.mp4"
PLAYLIST_IMG_URL = "https://files.catbox.moe/u79q4y.jpg"
STATS_VID_URL = "https://files.catbox.moe/uo4lc8.mp4"
TELEGRAM_AUDIO_URL = "https://files.catbox.moe/eis7ei.jpg"
TELEGRAM_VIDEO_URL = "https://files.catbox.moe/eis7ei.jpg"
STREAM_IMG_URL = "https://files.catbox.moe/eis7ei.jpg"
SOUNCLOUD_IMG_URL = "https://files.catbox.moe/eis7ei.jpg"
YOUTUBE_IMG_URL = "https://files.catbox.moe/eis7ei.jpg"
SPOTIFY_ARTIST_IMG_URL = SPOTIFY_ALBUM_IMG_URL = SPOTIFY_PLAYLIST_IMG_URL = YOUTUBE_IMG_URL

# ── Helpers ────────────────────────────────────────────────────────────────────
def time_to_seconds(time: str) -> int:
    return sum(int(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))

DURATION_LIMIT = time_to_seconds(f"{DURATION_LIMIT_MIN}:00")

# ───── Bot Introduction Messages ───── #
AYU = ["💞", "🦋", "🔍", "🧪", "⚡️", "🔥", "🎩", "🌈", "🍷", "🥂", "🥃", "🕊️", "🪄", "💌", "🧨"]
AYUV = [
    "🎵 **Welcome {0} to {1}!**\\n\\n"
    "A Telegram music and voice-chat bot with multi-platform playback, "
    "playlists, queue controls, lyrics and group tools.\\n\\n"
    "👑 **Owner:** 𝐋𝐎𝐊𝐄𝐒𝐇 𝐃𝐀𝐔𝐒𝐀\\n"
    "⏱ **Uptime:** {2}\\n"
    "💾 **Storage:** {3}\\n"
    "⚙️ **CPU:** {4}\\n"
    "🧠 **RAM:** {5}\\n"
    "👥 **Users:** {6} | **Groups:** {7}"
]

# ── Runtime structures ─────────────────────────────────────────────────────────
BANNED_USERS = filters.user()
adminlist, lyrical, votemode, autoclean, confirmer = {}, {}, {}, [], {}

# ── Minimal validation ─────────────────────────────────────────────────────────
if SUPPORT_CHANNEL and not re.match(r"^https?://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHANNEL URL. Must start with https://")

if SUPPORT_CHAT and not re.match(r"^https?://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - Invalid SUPPORT_CHAT URL. Must start with https://")



def validate_required_config() -> list[str]:
    """Return missing/invalid required settings without exposing secret values."""
    missing = []
    if API_ID <= 0:
        missing.append("API_ID")
    if not API_HASH:
        missing.append("API_HASH")
    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")
    if not BOT_USERNAME:
        missing.append("BOT_USERNAME (your BotFather username, without @)")
    if OWNER_ID <= 0:
        missing.append("OWNER_ID")
    if LOGGER_ID == 0:
        missing.append("LOGGER_ID")
    if not SUPPORT_CHAT:
        missing.append("SUPPORT_CHAT")
    if not SUPPORT_CHANNEL:
        missing.append("SUPPORT_CHANNEL")
    if not MONGO_DB_URI:
        missing.append("MONGO_DB_URI")
    if not any([STRING1, STRING2, STRING3, STRING4, STRING5]):
        missing.append("STRING_SESSION (at least one assistant session)")
    return missing
