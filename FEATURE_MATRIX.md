# DausaXmusic feature matrix

This inventory is derived from the imported source tree. Provider-specific commands may require credentials, provider uptime, Telegram permissions, and valid session strings.

| Feature group | Included capabilities | Main source locations |
|---|---|---|
| Music providers | YouTube, Spotify, Apple Music, SoundCloud, Resso, Telegram, Carbon | `DAUSAXMUSIC/platforms/` |
| Voice-chat playback | Audio/video play, live streams, channel play, play modes, queue and stream lifecycle | `plugins/play/`, `core/call.py`, `utils/stream/` |
| Player controls | Pause, resume, skip, stop, loop, seek, shuffle, speed, autoplay, auto-delete, VC notifications | `plugins/admins/`, `plugins/sudo/autoend.py` |
| Assistant accounts | Multiple Pyrogram assistant sessions, per-chat assistant selection, assistant lifecycle | `core/userbot.py`, `core/call.py`, `utils/database.py` |
| Inline player UI | Rich buttons, playback panels, queue navigation, settings, song cards | `utils/inline/`, `utils/rich_buttons.py`, `utils/thumbnail_renderer.py` |
| Song information | Lyrics, song lookup/download, metadata and thumbnails | `plugins/tools/lyrics.py`, `plugins/tools/song.py`, `utils/` |
| AI and media tools | GPT-style chat, image tools, video generation, background removal, upscale, MMF tools | `plugins/tools/`, `utils/free_ai.py` |
| Voice-play utilities | Voice request recognition, speech-to-text and text helpers | `utils/voiceplay*.py`, `plugins/admins/voiceplay.py` |
| Group management | Welcome, language, promote, purge, info, IDs, user/group tags, zombie cleanup | `plugins/Manager/` |
| Admin / owner controls | Authorization, maintenance, restart, block/ban, sudoers, logging, broadcast | `plugins/admins/`, `plugins/sudo/`, `plugins/misc/broadcast.py` |
| General utilities | Weather, QR, fonts, meme, IP tools, translation, TTS, movie lookup, news, social media helpers | `plugins/Kishu/`, `plugins/misc/`, `plugins/tools/` |
| Localization | English, Hindi, Arabic, Russian, Turkish | `strings/langs/` |
| Persistent data | MongoDB collections for users, chats, permissions, language and settings | `core/mongo.py`, `utils/database.py`, `mongo/` |
| DausaXmusic personal library | Private favorites and named playlists (create/list/add/show/remove/delete) | `plugins/personal/library.py` |
| DausaXmusic operations | Owner health diagnostics and private issue reports | `plugins/personal/owner_tools.py` |
| Deployment | Railway, Docker, Docker Compose, VPS shell setup, CI | `Dockerfile`, `docker-compose.yml`, `railway.json`, `.github/workflows/ci.yml`, `setup` |

## Explicit limitations

- Saved playlist entries are stored, but one-command sequential playlist playback is not implemented yet. Use `/play` for individual saved items.
- “24/7” behavior depends on a continuously running host and an active voice chat; Railway/VPS uptime cannot be guaranteed by bot code alone.
- Provider support is not a guarantee that each provider will remain accessible or permit a particular use.
- The imported implementation package remains named `DAUSAXMUSIC` internally to avoid breaking hundreds of cross-module imports. User-facing branding/configuration is DausaXmusic.
