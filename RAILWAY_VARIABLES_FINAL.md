# Final Railway variable decisions

This list matches the rebuilt `sample.env`: **86 unique variables**. No variable was renamed and no new variable is required. Keep real values in Railway, not GitHub.

## Required — preserve the existing working values

```dotenv
API_ID=<existing Telegram API ID>
API_HASH=<existing Telegram API hash>
BOT_TOKEN=<existing BotFather token>
MONGO_DB_URI=<existing reachable MongoDB URI; do not replace it>
LOGGER_ID=<existing numeric log chat ID>
STRING_SESSION=<existing authorized primary assistant session>
```

At least one of `STRING_SESSION`, `STRING_SESSION2`, `STRING_SESSION3`, `STRING_SESSION4`, or `STRING_SESSION5` is required. `STRING_SESSION` is the normal primary choice; the other four remain optional unchanged variables.

The bot must be administrator in `LOGGER_ID`, and the assistant must be authorized for the target Telegram groups. These are account/chat requirements, not additional environment variables.

## Existing optional variable with newly active support

```dotenv
COOKIE_URL=
```

Leave it blank to preserve anonymous direct yt-dlp behavior. If Railway receives YouTube's HTTP 429/sign-in challenge, you may set it to a private HTTPS URL for **your own authorized Netscape `cookies.txt` export**. Do not use another person's cookies, a public paste, an upstream cookie file, or a hardcoded Worker key. This is optional and not a playback guarantee.

## Unchanged — do not edit these merely to deploy the rebuild

These **79 variables** keep their existing values/defaults. Blank optional credentials remain blank unless you intentionally use that provider.

```text
STRING_SESSION2  STRING_SESSION3  STRING_SESSION4  STRING_SESSION5
OWNER_NAME  OWNER_ID  OWNER_USERNAME  BOT_NAME
BOT_USERNAME  INSTAGRAM_URL  SUPPORT_CHANNEL  SUPPORT_CHAT
ASSUSERNAME  ASSISTANT_JOIN_CHATS  ASSISTANT_LEAVE_TIME  DURATION_LIMIT
SONG_DOWNLOAD_DURATION  SONG_DOWNLOAD_DURATION_LIMIT  QUEUE_LIMIT  PLAYLIST_FETCH_LIMIT
TG_AUDIO_FILESIZE_LIMIT  TG_VIDEO_FILESIZE_LIMIT  SPOTIFY_CLIENT_ID  SPOTIFY_CLIENT_SECRET
YTPROXY_URL  YT_API_KEY  WORKER_FALLBACK_API_URL  WORKER_FALLBACK_API_KEY
ESSE_API_URL  ESSE_API_KEY  ESSE_TIMEOUT  API_URL
API_KEY  DEEP_API  REPLICATE_API_TOKEN  REPLICATE_API_TOKENS
HF_TOKEN  HF_TOKENS  OCR_SPACE_API_KEY  ELITE_LLM_API_BASE
ELITE_LLM_API_KEY  GENVID_USE_PUBLIC_FALLBACKS  VOICEPLAY_GROQ_API_KEY  VOICEPLAY_GROQ_API_KEY2
VOICEPLAY_GROQ_API_KEYS  GROQ_API_KEY  VOICEPLAY_STT_MODEL  VOICEPLAY_HINDI_VOICE
VOICEPLAY_ENGLISH_VOICE  VOICEPLAY_LISTEN_SECONDS  VOICEPLAY_SILENCE_SECONDS  VOICEPLAY_MIN_VOICE_SECONDS
VOICEPLAY_VAD_THRESHOLD  VOICEPLAY_MAX_TRANSCRIPTIONS  VOICEPLAY_STT_TIMEOUT  PHONE_LOOKUP_API_KEY
IPINFO_TOKEN  IPQUALITYSCORE_API_KEY  LOG_LEVEL  LOG_FILE
HEROKU_APP_NAME  HEROKU_API_KEY  UPSTREAM_REPO  UPSTREAM_BRANCH
GIT_TOKEN  MAX_CONCURRENT  CHUNK_SIZE  YTDLP_TIMEOUT
YOUTUBE_META_TTL  YOUTUBE_META_MAX  YOUTUBE_STREAM_HTTP_PROBE_TIMEOUT  YOUTUBE_STREAM_PREFLIGHT
YOUTUBE_STREAM_PREFLIGHT_TIMEOUT  DOWNLOAD_CACHE_MAX_MB  DOWNLOAD_CACHE_MIN_FREE_MB  WORKER_FALLBACK_API_ATTEMPTS
WORKER_FALLBACK_API_RETRY_DELAY_MS  EMPTY_VC_GRACE_SECONDS  EMPTY_VC_CHECK_INTERVAL
```

In particular:

- Do not change `MONGO_DB_URI` or MongoDB feature configuration to address YouTube 429 errors.
- Do not add `PORT`; this is a background worker, not a web service.
- `YOUTUBE_STREAM_PREFLIGHT=1` remains the default and need not be added if absent.
- `WORKER_FALLBACK_API_URL`, `WORKER_FALLBACK_API_KEY`, `YTPROXY_URL`, and `YT_API_KEY` remain optional authorized fallbacks. No upstream value is supplied.
- No PO Token, proxy, DRM, anti-bot, or authentication-bypass variable exists or is required.

## Branding defaults to preserve

```dotenv
OWNER_NAME=𝐋𝐎𝐊𝐄𝐒𝐇 𝐃𝐀𝐔𝐒𝐀
OWNER_ID=1236703127
OWNER_USERNAME=lokesh_dausa
BOT_NAME=⏤͟͞• ˹𝚀𝚄𝙴𝙴𝙽 ✘ ᴍᴜsɪᴄ˼🫧
BOT_USERNAME=DAUSA_MUSIC1_BOT
INSTAGRAM_URL=https://instagram.com/lokesh_dausa1
SUPPORT_CHANNEL=https://t.me/kalam_se
SUPPORT_CHAT=https://t.me/DAUSA_123
```

For purpose, source and default of every variable, use the full table in `ENVIRONMENT_VARIABLES.md`.
