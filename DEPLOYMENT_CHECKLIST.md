# DausaXmusic deployment checklist

## Before first boot
- [ ] Rotate any exposed upstream credentials; use your own Telegram API ID/hash and bot token.
- [ ] Configure `API_ID`, `API_HASH`, `BOT_TOKEN`, `OWNER_ID`, `LOGGER_ID`, `MONGO_DB_URI`, and at least one `STRING_SESSION`.
- [ ] Add the bot to the private log chat/channel and promote it with required permissions.
- [ ] Confirm the assistant account can access the target group voice chats.
- [ ] Configure `SUPPORT_CHAT` and `SUPPORT_CHANNEL` with valid URLs.
- [ ] Configure optional provider credentials only if required.
- [ ] Keep `.env`, session strings, and cookies out of Git.

## After deploy
- [ ] Confirm bot startup message appears in logs.
- [ ] Confirm `/start`, `/help`, and `/ping` work.
- [ ] Confirm `/play` and `/queue` in a test group with an active voice chat.
- [ ] Test pause, resume, skip, stop, autoplay, and channel play.
- [ ] Test `/favorite`, `/favorites`, and `/unfavorite` in private chat.
- [ ] Test playlist create/add/show/remove/delete.
- [ ] Test owner `/health` and user `/report`.
- [ ] Confirm MongoDB data persists after a restart.
- [ ] Check CPU/RAM/disk and Railway/VPS restart behavior under load.
