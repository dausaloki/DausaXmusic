# DausaXmusic environment variables

This inventory was generated from the audited `sample.env`, `config.py`, and direct project environment reads. It contains no secret values.

**Session rule:** at least one of `STRING_SESSION`, `STRING_SESSION2`, `STRING_SESSION3`, `STRING_SESSION4`, or `STRING_SESSION5` is required. `STRING_SESSION` is the normal primary choice; the others are optional alternatives/additional assistants.

**Railway minimum:** set the six ordinary required values (`API_ID`, `API_HASH`, `BOT_TOKEN`, `MONGO_DB_URI`, `LOGGER_ID`) plus at least one assistant session. Branding variables already have safe project defaults.

| Exact variable | Required or optional | Purpose | Where to obtain the value | Sample/default |
|---|---|---|---|---|
| `API_ID` | Required | Telegram MTProto application ID used by the bot and assistant. | https://my.telegram.org → API development tools. | `Blank` |
| `API_HASH` | Required | Telegram MTProto application hash paired with API_ID. | Same Telegram application page as API_ID; keep private. | `Blank` |
| `BOT_TOKEN` | Required | Authenticates the Telegram bot client. | @BotFather → select/create the bot → API Token; keep private. | `Blank` |
| `MONGO_DB_URI` | Required | MongoDB connection URI for queues, settings, users, and other persistent data. | MongoDB Atlas or your MongoDB server; create a least-privilege database user. | `Blank` |
| `LOGGER_ID` | Required | Numeric Telegram group/channel ID used for startup and error logs. | Your private log group/channel; add the bot as admin and obtain its numeric chat ID (usually negative). | `Blank` |
| `STRING_SESSION` | Required* | Primary Kurigram/Pyrogram user-session string for the voice-chat assistant. | Generate locally with Kurigram/Pyrogram using the assistant account; never paste it into Git or an untrusted website. | `Blank` |
| `STRING_SESSION2` | Optional* | Second assistant account session for multi-assistant deployments. | Generate locally for a second authorized Telegram account. | `Blank` |
| `STRING_SESSION3` | Optional* | Third assistant account session. | Generate locally for a third authorized Telegram account. | `Blank` |
| `STRING_SESSION4` | Optional* | Fourth assistant account session. | Generate locally for a fourth authorized Telegram account. | `Blank` |
| `STRING_SESSION5` | Optional* | Fifth assistant account session. | Generate locally for a fifth authorized Telegram account. | `Blank` |
| `OWNER_NAME` | Optional | Owner display name shown by the bot; branding default is preserved. | Already supplied; change only if intentionally changing branding. | `𝐋𝐎𝐊𝐄𝐒𝐇 𝐃𝐀𝐔𝐒𝐀` |
| `OWNER_ID` | Optional | Numeric Telegram user ID with owner/sudo privileges. | Already set to 1236703127; use your Telegram numeric ID only for a different owner. | `1236703127` |
| `OWNER_USERNAME` | Optional | Owner Telegram username without @. | Already supplied from the existing project branding. | `lokesh_dausa` |
| `BOT_NAME` | Optional | Bot display name used in messages and generated media. | Already set to the required QUEEN ✘ MUSIC branding. | `⏤͟͞• ˹𝚀𝚄𝙴𝙴𝙽 ✘ ᴍᴜsɪᴄ˼🫧` |
| `BOT_USERNAME` | Optional | Bot username without @, used for deep links. | Already set to DAUSA_MUSIC1_BOT; it must match the BotFather username. | `DAUSA_MUSIC1_BOT` |
| `INSTAGRAM_URL` | Optional | Instagram button destination. | Already set to the required project Instagram URL. | `https://instagram.com/lokesh_dausa1` |
| `SUPPORT_CHANNEL` | Optional | Telegram updates-channel URL used by buttons. | Already set to https://t.me/kalam_se. | `https://t.me/kalam_se` |
| `SUPPORT_CHAT` | Optional | Telegram support-group URL used by buttons. | Already set to https://t.me/DAUSA_123. | `https://t.me/DAUSA_123` |
| `ASSUSERNAME` | Optional | Assistant username declared by the original configuration; no active consumer was found in this revision. | Telegram assistant username without @, or leave blank. | `Blank` |
| `ASSISTANT_JOIN_CHATS` | Optional | Comma-separated chat usernames/IDs that assistants should try to join at startup. | Your Telegram group/channel usernames or IDs; leave blank to disable automatic joins. | `Blank` |
| `ASSISTANT_LEAVE_TIME` | Optional | Seconds between automatic assistant-leave checks. | Set a positive integer; sample default is 15000 seconds. | `15000` |
| `DURATION_LIMIT` | Optional | Maximum playable track duration in minutes. | Set a positive integer; sample default is 300. | `300` |
| `SONG_DOWNLOAD_DURATION` | Optional | Song-download duration value used by download limit messaging. | Set an integer in seconds; sample default is 1200. | `1200` |
| `SONG_DOWNLOAD_DURATION_LIMIT` | Optional | Maximum duration accepted by song download flows, in seconds. | Set a positive integer; sample default is 1800. | `1800` |
| `QUEUE_LIMIT` | Optional | Maximum tracks held in a chat queue. | Set a positive integer; sample default is 10. | `10` |
| `PLAYLIST_FETCH_LIMIT` | Optional | Maximum tracks imported from a playlist request. | Set a positive integer; sample default is 10. | `10` |
| `TG_AUDIO_FILESIZE_LIMIT` | Optional | Maximum Telegram audio file size accepted, in bytes. | Set an integer byte limit; keep the sample default unless needed. | `157286400` |
| `TG_VIDEO_FILESIZE_LIMIT` | Optional | Maximum Telegram video file size accepted, in bytes. | Set an integer byte limit; keep the sample default unless needed. | `1288490189999` |
| `COOKIE_URL` | Optional | Loads your own authorized Netscape YouTube cookie export for supported yt-dlp paths. Public HTTPS only, 1 MiB maximum, private runtime file; no cookie is bundled. | Leave blank for anonymous playback. If needed, use a private HTTPS location you control; never a public paste, another person's cookies, or Git. | `Blank` |
| `SPOTIFY_CLIENT_ID` | Optional | Spotify application client ID for Spotify metadata integration. | Spotify Developer Dashboard → your app. | `Blank` |
| `SPOTIFY_CLIENT_SECRET` | Optional | Spotify application client secret. | Spotify Developer Dashboard → your app; keep private. | `Blank` |
| `YTPROXY_URL` | Optional | Base URL for the authorized xBit-compatible YouTube fallback endpoint. | Your authorized media API provider; leave blank for normal yt-dlp paths. | `Blank` |
| `YT_API_KEY` | Optional | API key paired with YTPROXY_URL. | Your authorized provider dashboard; keep private. | `Blank` |
| `WORKER_FALLBACK_API_URL` | Optional | Base URL for the authorized Worker media fallback. | Your deployed/authorized Worker endpoint. | `Blank` |
| `WORKER_FALLBACK_API_KEY` | Optional | Credential paired with WORKER_FALLBACK_API_URL. | Your authorized Worker provider; keep private. | `Blank` |
| `ESSE_API_URL` | Optional | Base URL for ESSE autoplay recommendations. | Your authorized ESSE service endpoint; both URL and key are needed. | `Blank` |
| `ESSE_API_KEY` | Optional | Bearer credential for ESSE autoplay recommendations. | Your authorized ESSE provider; keep private. | `Blank` |
| `ESSE_TIMEOUT` | Optional | ESSE request timeout in seconds. | Set a positive number; sample default is 20. | `20` |
| `API_URL` | Optional | Base URL for the custom song-download API fallback. | Your authorized compatible song API provider; use together with API_KEY. | `Blank` |
| `API_KEY` | Optional | Credential for the custom API_URL song-download fallback. | Your authorized song API provider; keep private. | `Blank` |
| `DEEP_API` | Optional | DeepAI credential declared by the original config; no active consumer was found in this revision. | DeepAI dashboard if needed by a future integration; otherwise leave blank. | `Blank` |
| `REPLICATE_API_TOKEN` | Optional | Single Replicate credential for configured AI generation providers. | Replicate account → API tokens; keep private. | `Blank` |
| `REPLICATE_API_TOKENS` | Optional | Comma-separated Replicate token pool for authorized failover. | Your Replicate account; keep every token private. | `Blank` |
| `HF_TOKEN` | Optional | Single Hugging Face credential for provider-backed AI requests. | Hugging Face settings → Access Tokens; keep private. | `Blank` |
| `HF_TOKENS` | Optional | Comma-separated Hugging Face token pool. | Your Hugging Face account; keep every token private. | `Blank` |
| `OCR_SPACE_API_KEY` | Optional | Credential for OCR.Space image text recognition. | https://ocr.space/ocrapi → API key; keep private. | `Blank` |
| `ELITE_LLM_API_BASE` | Optional | Base URL for the configured OpenAI-compatible chat-completions provider. | Your authorized LLM provider or self-hosted endpoint. | `Blank` |
| `ELITE_LLM_API_KEY` | Optional | Bearer credential for ELITE_LLM_API_BASE. | Your authorized LLM provider; keep private. | `Blank` |
| `GENVID_USE_PUBLIC_FALLBACKS` | Optional | Controls whether public no-key video fallbacks are also tried when Replicate tokens exist. | Set 1 to enable or 0 to disable; no credential required. | `0` |
| `VOICEPLAY_GROQ_API_KEY` | Optional | Primary Groq credential for Voice Play speech-to-text. | GroqCloud console → API Keys; keep private. | `Blank` |
| `VOICEPLAY_GROQ_API_KEY2` | Optional | Backup Groq credential for Voice Play failover. | A second authorized key from GroqCloud; keep private. | `Blank` |
| `VOICEPLAY_GROQ_API_KEYS` | Optional | Comma-separated additional Groq key pool. | Your authorized GroqCloud keys; keep private. | `Blank` |
| `GROQ_API_KEY` | Optional | Alias/fallback Groq credential recognized by Voice Play. | GroqCloud console → API Keys; keep private. | `Blank` |
| `VOICEPLAY_STT_MODEL` | Optional | Groq speech-to-text model name. | Groq model documentation; sample uses whisper-large-v3-turbo. | `whisper-large-v3-turbo` |
| `VOICEPLAY_HINDI_VOICE` | Optional | Edge TTS voice used for Hindi Voice Play prompts. | Microsoft Edge TTS voice list; sample uses hi-IN-SwaraNeural. | `hi-IN-SwaraNeural` |
| `VOICEPLAY_ENGLISH_VOICE` | Optional | Edge TTS voice used for English Voice Play prompts. | Microsoft Edge TTS voice list; sample uses en-IN-NeerjaNeural. | `en-IN-NeerjaNeural` |
| `VOICEPLAY_LISTEN_SECONDS` | Optional | Maximum Voice Play listening window in seconds. | Set a number; sample default is 8. | `8` |
| `VOICEPLAY_SILENCE_SECONDS` | Optional | Silence duration that ends a Voice Play utterance. | Set a number; sample default is 1.2. | `1.2` |
| `VOICEPLAY_MIN_VOICE_SECONDS` | Optional | Minimum voiced audio accepted for transcription. | Set a number; sample default is 0.45. | `0.45` |
| `VOICEPLAY_VAD_THRESHOLD` | Optional | Voice-activity detection audio threshold. | Tune only if needed; sample default is 160. | `160` |
| `VOICEPLAY_MAX_TRANSCRIPTIONS` | Optional | Maximum transcription attempts per Voice Play request cycle. | Set a positive integer; sample default is 4. | `4` |
| `VOICEPLAY_STT_TIMEOUT` | Optional | Speech-to-text request timeout in seconds. | Set a positive integer; sample default is 15. | `15` |
| `PHONE_LOOKUP_API_KEY` | Optional | APILayer-compatible phone number validation credential. | Your APILayer/phone-validation provider dashboard; keep private. | `Blank` |
| `IPINFO_TOKEN` | Optional | Token for IPInfo lookup enrichment. | https://ipinfo.io → account/token; keep private. | `Blank` |
| `IPQUALITYSCORE_API_KEY` | Optional | Credential for IPQualityScore IP risk lookup. | https://www.ipqualityscore.com → account API key; keep private. | `Blank` |
| `LOG_LEVEL` | Optional | Python logging threshold. | Use INFO, WARNING, ERROR, or DEBUG; sample uses INFO. | `INFO` |
| `LOG_FILE` | Optional | Local rotating log file path. | Set a writable container/VPS path; sample uses log.txt (ephemeral on Railway). | `log.txt` |
| `HEROKU_APP_NAME` | Optional | Heroku app name for Heroku-specific update/management features; not needed on Railway. | Your Heroku dashboard, only if using Heroku integration. | `Blank` |
| `HEROKU_API_KEY` | Optional | Heroku account credential; not needed on Railway. | Heroku account settings; keep private. | `Blank` |
| `UPSTREAM_REPO` | Optional | HTTPS Git repository URL used by update functionality. | Your GitHub repository URL; leave blank to disable upstream update handling. | `Blank` |
| `UPSTREAM_BRANCH` | Optional | Branch used with UPSTREAM_REPO. | Your Git branch name; sample uses main. | `main` |
| `GIT_TOKEN` | Optional | Git credential for authorized private-repository update access. | GitHub fine-grained PAT with minimal read access, only if required; keep private. | `Blank` |
| `MAX_CONCURRENT` | Optional | Maximum concurrent operations guarded by the shared download semaphore. | Leave blank for the automatic CPU-based default, or set a positive integer. | `Blank` |
| `CHUNK_SIZE` | Optional | I/O chunk size in bytes. | Set a positive integer; sample default is 65536. | `65536` |
| `YTDLP_TIMEOUT` | Optional | yt-dlp operation timeout in seconds. | Set a positive integer; sample default is 45. | `45` |
| `YOUTUBE_META_TTL` | Optional | YouTube metadata cache lifetime in seconds. | Set a non-negative integer; sample default is 300. | `300` |
| `YOUTUBE_META_MAX` | Optional | Maximum YouTube metadata cache entries. | Set a positive integer; sample default is 2048. | `2048` |
| `YOUTUBE_STREAM_HTTP_PROBE_TIMEOUT` | Optional | Seconds to wait for the first byte of a direct yt-dlp or Worker media stream. | Set a number; sample default is 15. | `15` |
| `YOUTUBE_STREAM_PREFLIGHT` | Optional | Enables/disables FFmpeg preflight validation for direct yt-dlp and Worker streams. | Set 1/true or 0/false; sample enables it. Keep enabled for normal Railway playback. | `1` |
| `YOUTUBE_STREAM_PREFLIGHT_TIMEOUT` | Optional | Maximum seconds allowed for direct/Worker stream preflight validation. | Set a number; sample default is 15. | `15` |
| `DOWNLOAD_CACHE_MAX_MB` | Optional | Maximum local download-cache size in MiB. | Set based on available disk; sample default is 2048. Railway filesystem is ephemeral. | `2048` |
| `DOWNLOAD_CACHE_MIN_FREE_MB` | Optional | Minimum free disk space preserved during caching, in MiB. | Set based on available disk; sample default is 512. | `512` |
| `WORKER_FALLBACK_API_ATTEMPTS` | Optional | Attempts for transient Worker 429/5xx failures (code caps this at 1–3). | Set an integer; sample default is 3. | `3` |
| `WORKER_FALLBACK_API_RETRY_DELAY_MS` | Optional | Base delay between transient Worker retries, in milliseconds. | Set a non-negative integer; sample default is 1000. | `1000` |
| `EMPTY_VC_GRACE_SECONDS` | Optional | Grace period before an empty voice chat is closed; code enforces at least 60. | Set a number of seconds; sample default is 300. | `300` |
| `EMPTY_VC_CHECK_INTERVAL` | Optional | Interval between empty-voice-chat checks; code enforces at least 15. | Set a number of seconds; sample default is 30. | `30` |

Blank optional API credentials disable only their related provider-backed integration; core startup still requires the mandatory Telegram/MongoDB/session values above.
