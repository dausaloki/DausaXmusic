# DausaXmusic

**Bot display name:** ⏤͟͞• ˹𝚀𝚄𝙴𝙴𝙽 ✘ ᴍᴜsɪᴄ˼🫧  
**Owner:** 𝐋𝐎𝐊𝐄𝐒𝐇 𝐃𝐀𝐔𝐒𝐀  
**Telegram:** [@lokesh_dausa](https://t.me/lokesh_dausa)  
**Bot:** [@DAUSA_MUSIC1_BOT](https://t.me/DAUSA_MUSIC1_BOT)

DausaXmusic is a Telegram group music and voice-chat bot with multi-source playback, queue controls, playlists, lyrics, group administration, and optional AI/media utilities.

## Official community links

- Support group: https://t.me/DAUSA_123
- Updates channel: https://t.me/kalam_se
- Instagram: https://instagram.com/lokesh_dausa1

No YouTube, GitHub profile, or website social link is configured.

## Included capabilities

- Group voice-chat audio and video playback
- YouTube, Spotify, Apple Music, SoundCloud, Resso and Telegram media integrations (provider availability may change)
- Queue, pause, resume, skip, stop, seek, shuffle, loop, speed and autoplay controls
- Channel/live playback and assistant accounts
- Lyrics search and song utilities
- Dynamic music thumbnails and branded welcome banner
- Inline controls, rich buttons and help navigation
- Group welcome tools and moderation/admin commands
- Sudo tools, broadcast, statistics and logging
- Voice-play and speech-to-text utilities
- Optional AI and media utilities
- MongoDB persistence
- Private favorites and playlist manager
- Owner health diagnostics and user reports

Some integrations require credentials and/or may be affected by third-party service changes. A feature being present in the source does not guarantee that its external provider is currently available.

## Quick setup

1. Create a Telegram bot with [@BotFather](https://t.me/BotFather).
2. Obtain Telegram API credentials from https://my.telegram.org.
3. Copy `sample.env` to `.env`.
4. Fill in `API_ID`, `API_HASH`, `BOT_TOKEN`, `LOGGER_ID`, `MONGO_DB_URI`, and at least one authorized `STRING_SESSION`.
5. Confirm the prefilled owner ID, bot username, support group, updates channel and Instagram URL are yours.
6. Install Python 3.12, FFmpeg and requirements:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m DAUSAXMUSIC
```

## Railway

1. Upload the corrected project contents to your GitHub repository; keep `Dockerfile` and `railway.json` at the repository root. See `GITHUB_UPLOAD.md`.
2. Create a Railway project from that repository and leave Root Directory empty or `/`.
3. Add the required values from `sample.env` under Railway Variables. The complete 86-variable reference is in `ENVIRONMENT_VARIABLES.md`.
4. Use MongoDB Atlas or another reachable MongoDB service.
5. Follow the Hindi guide `RAILWAY_DEPLOYMENT_HI.md` and the live `DEPLOYMENT_CHECKLIST.md`.
6. Deploy and inspect logs. A successful image build alone does not prove that Telegram login, assistant sessions, database access or voice calls work.

YouTube voice-chat playback now tries direct yt-dlp first, with no Worker or xBit API required. Deno and the local EJS component are pinned in `requirements.txt`; existing optional API fallbacks remain available. See `PLAYBACK_FIX_REPORT.md` for the exact root cause and real song-name/URL extraction tests.

The original source-audit changes are documented in `AUDIT_REPORT.md`, and the latest playback repair and verification results are in `PLAYBACK_FIX_REPORT.md`.

## Docker / VPS

```bash
cp sample.env .env
# Edit .env and add your private credentials.
docker compose up -d --build
docker compose logs -f
```

For a VPS, install Python 3.12 and FFmpeg, configure `.env`, then run with Docker or a process supervisor such as systemd.

## Useful commands

| Command | Purpose |
|---|---|
| `/play`, `/vplay` | Play audio/video in a group voice chat |
| `/queue`, `/player` | Queue and player controls |
| `/pause`, `/resume`, `/skip`, `/stop` | Playback controls |
| `/lyrics` | Search lyrics |
| `/song` | Song utility |
| `/favorite`, `/favorites`, `/unfavorite` | Personal favorites |
| `/playlist` | Personal playlist manager |
| `/health` | Owner runtime diagnostics |
| `/report` | Send an issue report |

Use `/help` in Telegram for the active command catalogue.

## Security

- Never commit `.env`, Telegram session strings, cookies, API keys or database credentials.
- Rotate any credential that has ever been exposed publicly.
- Use only accounts and media sources you are authorized to access.
- Keep the repository private until you have reviewed all configuration and assets.
- Do not expose MongoDB publicly.

## License and third-party notices

This project contains modified components from an MIT-licensed upstream codebase. The original MIT license and its required copyright notice are retained in `LICENSE` as required by that license. Other third-party libraries and assets remain subject to their respective licenses.
