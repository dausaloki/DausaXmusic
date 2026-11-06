# DausaXmusic final deployment verification checklist

This is the live deployment checklist. For the tests actually performed during the source audit, see `AUDIT_REPORT.md`; do not treat unchecked live items below as already verified.

## Source and repository

- [ ] Repository root directly contains `Dockerfile`, `railway.json`, `requirements.txt`, `config.py`, `sample.env`, and `DAUSAXMUSIC/`.
- [ ] No extra nested project root was uploaded.
- [ ] Redundant `Readme.md` and non-source artifacts were removed; the real `README.md` remains.
- [ ] `.env`, cookies, Telegram sessions, API secrets, private tokens, and database credentials are absent from Git.
- [ ] GitHub Actions completed successfully, including FFmpeg, dependency, compilation, import-guard, and test steps.

## Before first Railway boot

- [ ] Rotate any credential that was ever exposed publicly.
- [ ] Set `API_ID`, `API_HASH`, `BOT_TOKEN`, `LOGGER_ID`, and `MONGO_DB_URI` in Railway Variables.
- [ ] Set at least one valid assistant session: `STRING_SESSION` or one of `STRING_SESSION2` through `STRING_SESSION5`.
- [ ] Confirm `OWNER_ID=1236703127` and the preserved bot/owner branding.
- [ ] Confirm `BOT_USERNAME=DAUSA_MUSIC1_BOT` without `@`.
- [ ] Confirm `SUPPORT_CHAT=https://t.me/DAUSA_123` and `SUPPORT_CHANNEL=https://t.me/kalam_se`.
- [ ] Add the bot to the private log chat/channel and promote it to administrator.
- [ ] Confirm the assistant account can access the target groups and voice chats.
- [ ] Confirm MongoDB credentials and network access from Railway.
- [ ] Configure optional provider credentials only for features actually being used.
- [ ] Leave `COOKIE_URL` blank for anonymous playback, or set only your own authorized Netscape export at a private HTTPS URL; never commit or publicly paste cookies.
- [ ] Leave Railway Root Directory empty or `/`; use the root Dockerfile and `python -m DAUSAXMUSIC`.
- [ ] Keep failure retries bounded; do not replace the configured policy with an unbounded crash loop.

## Build and startup logs

- [ ] Docker build completed with Python 3.12 and FFmpeg/FFprobe available.
- [ ] Build-time `deno --version`, `yt_dlp_ejs` import, and FFmpeg checks passed.
- [ ] Dependency installation completed without resolver conflicts.
- [ ] No `ModuleNotFoundError` occurred (including `six` or `youtubesearchpython.future`).
- [ ] No HTTPX `unexpected keyword argument 'proxies'` error occurred during YouTube search.
- [ ] Required-variable validation did not report a missing setting.
- [ ] `Modules loaded.` appeared.
- [ ] `DausaXmusic started successfully.` appeared.
- [ ] The bot posted its startup message to `LOGGER_ID`.

## Live Telegram and music checks

- [ ] `/start`, `/help`, and `/ping` work.
- [ ] The assistant joins a test group voice chat.
- [ ] `/play <song name>` produces audible audio and `/queue` shows the correct current track.
- [ ] `/play <public YouTube watch URL>` also produces audible audio for the same test track.
- [ ] Logs show `Direct yt-dlp format selected` and `YouTube source ok | source=direct_ytdlp` without requiring Worker/xBit credentials.
- [ ] If a source fails, inspect the first sanitized direct-extraction/preflight error rather than only the final generic message.
- [ ] If Railway returns HTTP 429/`Sign in to confirm you're not a bot`, record it as an external IP/session challenge—not MongoDB/FFmpeg—and test only an authorized cookie/provider path without assuming a code-only bypass.
- [ ] Pause, resume, skip, stop, seek, loop, shuffle, speed, and autoplay work as expected.
- [ ] `/vplay` and video playback work.
- [ ] Queue list/back buttons and the corrected queue welcome image work.
- [ ] `/lyrics`, song download, and thumbnail generation work.
- [ ] `/favorite`, `/favorites`, and `/unfavorite` work in private chat.
- [ ] Playlist create/add/show/remove/delete flows work.
- [ ] Couple and cute-wish commands use their existing `assets/vivaan` media correctly.
- [ ] Owner `/health` and user `/report` work.
- [ ] Optional Voice Play and AI/provider features are tested separately when configured.

## Persistence and operations

- [ ] MongoDB settings/data persist after a restart.
- [ ] No repeating crash/restart pattern appears in Railway logs.
- [ ] CPU, RAM, open files, and disk use remain within service limits during playback.
- [ ] Ephemeral cache/log growth is understood; persistent data is not stored only in the container filesystem.
- [ ] Third-party provider outages are distinguished from bot startup failures.
