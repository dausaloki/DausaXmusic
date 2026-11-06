# DausaXmusic YouTube playback — root cause and consolidated fix

**Audit/fix date:** 2026-11-06  
**GitHub baseline inspected:** `8cde05e13372e2c237afc3e5cdc4b3f1aee98e68` (`main`)  
**Repository:** https://github.com/dausaloki/DausaXmusic

## 1. Exact root cause

The reported generic message is `play_14` in `strings/langs/en.yml`. In the YouTube playback branch, `DAUSAXMUSIC/utils/stream/stream.py` raises it when `YouTube.download()` returns no `file_path`. Despite its wording, it does **not** prove that song-name search or metadata lookup failed.

The supplied Railway logs prove execution reached the media-source stage:

1. `Worker fallback API URL/key not set. Skipping worker fallback.`
2. `xBit fallback not configured for audio.`
3. `YouTube source failed.`

In the inspected `DAUSAXMUSIC/platforms/Youtube.py` baseline:

- `audio_dl()` tried only Worker and then xBit.
- `video_dl()` also tried only Worker and then xBit.
- Neither function passed the YouTube watch URL to `yt_dlp.extract_info()` for voice-chat playback.
- yt-dlp appeared elsewhere (`formats()`, song downloads, direct media downloads, and `video()`), but those are different code paths and did not make normal voice-chat `audio_dl()` direct-capable.

Therefore, with both optional APIs unset, normal voice-chat playback deterministically returned `(None, True)`. Song-name search and a YouTube watch URL both resolve to a video ID and then converge on this same broken source chain, explaining why both failed identically.

**Primary root cause: direct yt-dlp was not wired into the normal voice-chat audio/video source functions at all.** Missing Worker/xBit credentials only made that existing code defect visible; buying those APIs was not necessary.

### Secondary compatibility findings while implementing the fix

- Current yt-dlp warned that no supported JavaScript runtime was installed; only Deno is enabled by default. Some formats can be missing without it.
- A default-client `251/webm` URL could be extracted, but full media download/FFmpeg access returned HTTP 403 in the test environment. Extraction success alone was therefore not accepted as playback success.
- The standard yt-dlp Android client exposed a progressive `18/mp4` source for the public test video. Its full HTTP request returned 200, its range request returned 206, FFmpeg decoded its AAC audio successfully, and a real yt-dlp local download completed.
- iOS/mweb emitted PO Token requirements in this environment. They are not part of this fix. No cookies, PO Tokens, proxies, authentication bypass, DRM bypass, or paid access workaround is used.

## 2. Consolidated solution

Normal YouTube voice-chat source order is now:

```text
Direct yt-dlp → existing optional Worker → existing optional xBit
```

The direct implementation:

- runs extraction off the event loop with the existing `YTDLP_TIMEOUT` bound;
- uses yt-dlp's supported Android player client for a single-file FFmpeg-compatible source;
- prefers progressive format 18 for audio when available, then supported audio/combined fallbacks;
- requires a combined audio+video format for video instead of returning separate URLs PyTgCalls cannot consume as one input;
- validates returned URLs with the existing HTTP and FFmpeg preflight before returning a stream;
- retains local download fallback and background caching;
- preserves Worker and xBit for users who already configured them;
- applies the same compatible client/single-file selection to the `video()` URL extraction path;
- logs the selected source and sanitized extraction errors without signed media URLs;
- adds no new required environment variable.

Deno 2.8.3 and `yt-dlp-ejs==0.8.0` are pinned in `requirements.txt`. The Dockerfile verifies the EJS import, Deno executable, and FFmpeg during build. No `nixpacks.toml` is needed because `railway.json` explicitly selects the root Dockerfile.

## 3. Files changed in this playback repair

1. `DAUSAXMUSIC/platforms/Youtube.py` — direct source, compatible live URL extraction, preflight/local integration, source status, sanitized diagnostics.
2. `requirements.txt` — pinned Deno and local EJS component; retained yt-dlp 2026.7.4 and all existing dependencies.
3. `Dockerfile` — build-time Deno/EJS/FFmpeg validation; existing Python 3.12 and start command retained.
4. `tests/test_youtube_direct.py` — six direct audio/video/local/live/failure/security regression tests.
5. `sample.env` — clarified that Worker/xBit are not required for direct playback; no variable added or renamed.
6. `ENVIRONMENT_VARIABLES.md` — updated direct/Worker preflight descriptions.
7. `RAILWAY_DEPLOYMENT_HI.md` — direct playback requirements, logs, and Hindi deployment/verification guidance.
8. `DEPLOYMENT_CHECKLIST.md` — separate live song-name and YouTube URL checks.
9. `GITHUB_UPLOAD.md` — secure Android/Termux upload instructions and new ZIP name.
10. `PROJECT_STATUS.md` — current verified status and explicit unperformed live tests.
11. `README.md` — direct playback behavior and report link.
12. `PLAYBACK_FIX_REPORT.md` — this consolidated diagnosis and result.

No Quiz Bot file was touched. No music command, plugin, feature module, UI, locale, branding value, or existing fallback was removed. The actual project configuration remains root `config.py`; there is no separate `DAUSAXMUSIC/config.py` in this repository revision, and no config-code change was needed.

## 4. Railway variables

### Required values — keep the existing working values

```dotenv
API_ID=<existing Telegram API ID>
API_HASH=<existing Telegram API hash>
BOT_TOKEN=<existing BotFather token>
MONGO_DB_URI=<existing connected MongoDB URI>
LOGGER_ID=<existing numeric log chat ID>
STRING_SESSION=<existing authorized assistant session>
```

At least one of `STRING_SESSION` through `STRING_SESSION5` is required; the others are optional. Do not move real values into GitHub.

Keep the existing branding values unchanged, including `OWNER_ID=1236703127`, `BOT_USERNAME=DAUSA_MUSIC1_BOT`, the required bot/owner names, support/updates URLs, and Instagram URL.

### Playback settings — existing optional defaults, not new requirements

```dotenv
YTDLP_TIMEOUT=45
YOUTUBE_STREAM_HTTP_PROBE_TIMEOUT=15
YOUTUBE_STREAM_PREFLIGHT=1
YOUTUBE_STREAM_PREFLIGHT_TIMEOUT=15
```

If these are absent, the code already uses these defaults. They do not need to be added merely to deploy this fix.

`WORKER_FALLBACK_API_URL`, `WORKER_FALLBACK_API_KEY`, `YTPROXY_URL`, and `YT_API_KEY` remain optional. Leave them blank for direct-only playback, or keep existing authorized values as fallbacks. No new API URL/key is required. All unrelated Telegram, MongoDB, cache, UI, Voice Play, and optional provider variables should remain unchanged.

## 5. Deployment compatibility verified

| Requirement | Verified state |
|---|---|
| Python | CPython 3.12.16; Docker base remains `python:3.12-slim` |
| yt-dlp | 2026.7.4 |
| JavaScript runtime/component | Deno 2.8.3 and yt-dlp-ejs 0.8.0 installed and used successfully |
| FFmpeg/FFprobe | 7.1.5 available; direct AAC decode and local-file validation passed |
| Telegram/voice dependencies | Kurigram 2.2.26, PyTgCalls 2.3.3, NTgCalls 2.2.5, TgCrypto 1.2.5 installed/imported |
| Dependency consistency | 112 packages including pytest checked; zero conflicts |
| Railway builder/start | Dockerfile builder and `python -m DAUSAXMUSIC`; unchanged |
| Restart behavior | `ON_FAILURE`, maximum 10 retries; unchanged |
| `nixpacks.toml` | Absent and unnecessary with the explicit Dockerfile builder |
| MongoDB configuration | Unchanged; no live production database test performed here |

## 6. Tests actually performed

| Test | Result |
|---|---|
| Real song-name and watch-URL search | Both resolved the expected public video and metadata |
| Real integrated `YouTube.track()` + `YouTube.download(stream=True)` | **Both song name and YouTube URL passed**, returned `direct yt-dlp ok (audio)` |
| Existing HTTP + FFmpeg preflight on both integrated paths | Passed |
| Real direct FFmpeg audio decode | Exit 0; AAC audio decoded |
| Real integrated direct local download (`stream=False`) | 11,829,048-byte file; ffprobe confirmed AAC audio |
| New direct playback regression tests | 6 passed |
| Complete offline test suite | **155 passed, 3,088 subtests passed, 0 failed** |
| Recursive compilation | 216 Python files passed |
| Application imports | 203 modules, zero failures |
| Offline mocked startup | All 115 plugins loaded; start/stop orchestration passed |
| Dependency install and `pip check` | Passed; zero conflicts |
| Ruff critical checks and `git diff --check` | Passed |
| Railway/app JSON, deployment YAML, and shell syntax | Passed |
| Docker Python import commands and Deno/FFmpeg executables | Passed directly; Docker image build not available |

The sandbox initially reproduced extraction/download behavior on one public video. YouTube can change clients/formats at any time, so each target deployment and the actual media types used still need live verification.

## 7. Tests not performed

- No real Telegram bot/assistant login was performed.
- No actual Telegram voice chat was joined; audible PyTgCalls playback on Railway remains a live checklist item.
- No production MongoDB connection was made by this audit; the user's reported working MongoDB configuration was left unchanged.
- No Docker daemon was available, so the Dockerfile was validated statically and its dependency/runtime checks were run directly rather than building the image.
- No GitHub push or Railway deployment was performed.
- Private, age-restricted, DRM-protected, or otherwise unavailable videos were not bypassed or promised as supported.

## 8. Final live verification

After upload/redeploy, use a public non-DRM test song in a group with an active voice chat:

1. Run `/play <song name>` and confirm audible audio and the correct queue entry.
2. Run `/play <public YouTube watch URL>` for the same song and confirm audible audio again.
3. Confirm Railway logs contain `Direct yt-dlp format selected` and `YouTube source ok | source=direct_ytdlp`.
4. Confirm playback does not depend on Worker/xBit variables.
5. Test pause, resume, skip, stop, and one queued track.
6. Test `/vplay` with a public video if video playback is used.
7. If a failure occurs, inspect the first sanitized direct-extraction or preflight error, not only the final generic message.

Detailed Android upload steps are in `GITHUB_UPLOAD.md`; Hindi Railway steps are in `RAILWAY_DEPLOYMENT_HI.md`; the complete live checklist is in `DEPLOYMENT_CHECKLIST.md`.
