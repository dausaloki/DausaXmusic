# Complete DausaXmusic audit and playback hardening

## Summary

Completes the three-source review against:

- `SkyBotsDeveloper/VivaanXmusic3.0` at `b59d44e`
- customized `dausaloki/DausaXmusic` main at `86bec22`
- PR #6 head `8e9efa6` (already merged; code-identical to main)

The branch preserves DausaXmusic branding, custom assets/UI and existing features. The final diff is **33 paths: 25 modified, 8 added, 0 removed**. It does not copy upstream's hardcoded Worker credential, branded README, cookie artifact or custom search fork. No Quiz Bot file is included.

## Comparison result

- Final raw inventory: 47 identical, 205 different, 29 custom-only, two upstream-only across 283 reviewed rows.
- Only upstream-only paths: branded `Readme.md` and `assets/cookies.txt`; neither is a missing feature.
- Baseline common text after package/brand normalization: 35 exact, 136 equivalent, 66 manually reviewed substantive differences.
- Latest upstream sticker-owner, thumbnail, public-provider, rich-button, MMF and Git-availability fixes were already present.
- Row-level decisions: `docs/upstream-comparison.csv`.
- Full review: `COMPLETE_REBUILD_REPORT.md`.

## Changes

- Adds secure optional support for existing `COOKIE_URL` using only the operator's authorized Netscape export.
  - Public HTTPS target and redirect validation
  - 1 MiB limit and Netscape-format validation
  - Private `0700` directory / `0600` file
  - No cookie URL/content logging; blank value preserves anonymous playback
- Updates `yt-dlp` to 2026.10.26 and Deno to the matching 2.9.8; retains yt-dlp-ejs 0.8.0.
- Restores normal TLS certificate verification in quote and song/YouTube download paths.
- Sanitizes additional media/provider diagnostic paths.
- Corrects `app.json` owner/session/branding/provider metadata without introducing required variables.
- Removes remaining original developer identity from AI responses and thumbnail fallback; replaces the unused upstream-branded reference image with approved DausaXmusic artwork while preserving its path.
- Adds exact archived-commit provenance through `FINAL_BUILD_INFO.md` and Git `export-subst`.
- Updates Railway, Android/Termux, security, playback and live-verification documentation.
- Adds cookie, branding and authorized-cookie extraction regression tests.

No feature module, command, locale, UI component or required asset is removed. MongoDB configuration, Docker/Railway startup and existing required Railway variables remain unchanged.

## Verification executed

- CPython 3.12.16 fresh dependency environment; 113 packages compatible.
- **165 tests + 3,088 subtests passed; 219 Python files compiled.**
- 201 application modules imported with zero failures.
- Offline mocked startup loaded all 115 plugins and verified start/stop orchestration.
- Recursive compilation, Ruff critical checks, `git diff --check`, JSON/YAML and shell syntax passed.
- Real anonymous public-video song-name and watch-URL paths passed direct HTTP + FFmpeg preflight.
- Real 11,829,048-byte local download passed ffprobe; AAC audio and H.264 video confirmed.
- Deno 2.9.8, yt-dlp 2026.10.26, yt-dlp-ejs 0.8.0 and FFmpeg 7.1.5 verified.

## Not performed / external limitation

No real Telegram login, production MongoDB connection, Telegram voice call, Docker daemon build, GitHub push or Railway deployment was performed by the audit environment.

The supplied Railway screenshot shows YouTube HTTP 429 and `Sign in to confirm you're not a bot` after successful startup. Sandbox success does not guarantee Railway playback because the IP/session reputation differs. This PR does not claim an anti-bot/authentication/DRM bypass. `COOKIE_URL` is optional for an authorized session and is not a guarantee; Worker/xBit remain optional authorized fallbacks.

## Railway variables

Keep existing values for:

```dotenv
API_ID=<existing>
API_HASH=<existing>
BOT_TOKEN=<existing>
MONGO_DB_URI=<existing>
LOGGER_ID=<existing>
STRING_SESSION=<existing authorized assistant>
```

At least one `STRING_SESSION`…`STRING_SESSION5` is required. Existing branding, MongoDB, UI, cache and provider variables remain unchanged. `COOKIE_URL` remains optional and blank by default. No new variable is required. See `RAILWAY_VARIABLES_FINAL.md` for the exact six required, one newly active optional and 79 unchanged names.

## Review checklist

- [ ] Review `COMPLETE_REBUILD_REPORT.md` and the complete CSV comparison.
- [ ] Confirm no secret file/value is staged.
- [ ] Confirm GitHub Actions passes.
- [ ] Deploy the review branch or merge deliberately; do not overwrite main directly.
- [ ] Run `/play <song name>` and `/play <public YouTube URL>` in a real voice chat.
- [ ] If Railway still returns 429/sign-in, record the external limitation and test only an authorized cookie/provider path.
- [ ] Complete `DEPLOYMENT_CHECKLIST.md` for Telegram, MongoDB, controls and persistence.
