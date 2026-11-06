# DausaXmusic complete project audit and Railway fix

> **Historical 2026-11-05 audit:** version counts and the then-unused `COOKIE_URL` statement below describe that earlier snapshot. The final migration, current runtime and active secure cookie support are documented in `COMPLETE_REBUILD_REPORT.md`.

**Audit date:** 2026-11-05  
**Original GitHub snapshot audited:** `7d9d5b01734446e429aef06fa410b66990e647a8`  
**Target runtime:** Python 3.12 (tested with CPython 3.12.16)  
**Project:** https://github.com/dausaloki/DausaXmusic

## Result and scope

The complete repository was inspected recursively, including 215 Python source files (including root `config.py`), deployment files, requirements, assets, tests, environment handling, and startup/plugin loading. Deployment-blocking import, dependency, configuration, asset-path, and test-fixture issues were corrected.

This is a corrected source package, **not a claim of a live Railway deployment**. Telegram credentials, a production MongoDB, real assistant accounts, Docker daemon access, GitHub write access, and Railway access were not available. Those live checks remain explicitly listed in `DEPLOYMENT_CHECKLIST.md`.

## Main findings and fixes

| Area | Finding | Correction |
|---|---|---|
| YouTube imports | Four modules used nonexistent `youtubesearchpython.future`. | Changed to supported async `youtubesearchpython.__future__` in inline bot, start, lyrics, and thumbnails. Existing correct imports in the platform modules were retained. |
| YouTube classes | `Recommendations` is not exported anywhere by `youtube-search-python==1.6.6`; the optional import was dead code. | Removed the nonexistent class import and retained the working title-based async `VideosSearch` autoplay fallback. Verified all other used search exports directly from the installed package. |
| YouTube/HTTPX runtime | `youtube-search-python==1.6.6` calls HTTPX with `proxies=`, which HTTPX 0.28 removed. Import-only testing did not reveal this; a real search did. | Pinned `httpx[http2]==0.27.2`. A real `VideosSearch.next()` request subsequently returned a valid result. |
| Translator compatibility | Latest `gpytranslate==2.1.0` requires HTTPX ≥0.28.1, conflicting with the YouTube library’s required API. | Pinned `gpytranslate==1.5.1`; verified the same `Translator.detect()` and `Translator(...)` signatures used by the project, `pip check`, and a real translation request. |
| Missing dependency | `heroku3==5.2.1` imports `six` but does not declare it, causing startup `ModuleNotFoundError`. | Added `six==1.17.0` explicitly. |
| Blank Mongo URI | With a blank `.env` URI, Motor raised during import and the handler called status-0 `exit()`, bypassing required-variable validation. | Defer Mongo network I/O, allow blank URI to reach normal validation, avoid credential-bearing error output, and raise a clear nonzero fatal error for invalid configuration. |
| Fatal startup exits | Bot log-chat, assistant, and session failures could use status-0 exits. | Replaced fatal `exit()`/`sys.exit()` paths with explicit `RuntimeError` failures so Railway detects failure correctly; retries remain bounded to 10. |
| Environment sample | `OWNER_NAME` and `OWNER_ID` were merged by a literal `\n`; `BOT_NAME` appeared twice; many real settings were undocumented. | Rebuilt and sanitized `sample.env`: 86 unique assignments, no duplicates, no literal newline damage, and no secrets. |
| Environment scrubbing | `IPINFO_TOKEN` was removed by security scrubbing before its plugin read it. Related utility credentials were read inconsistently. | Load phone/IP credentials through `config.py`, retain their values for plugins, and register them for secret scrubbing/redaction. Verified with safe test values. |
| Blank tuning values | Direct `int(os.getenv(...))` calls could fail on blank optional tuning values. | Added shared blank-safe integer parsing while preserving defaults, including CPU-based `MAX_CONCURRENT`. |
| Missing assets | Queue, cute-wish, and couples features referenced nonexistent `assets/dausa` files while the repository contains `assets/vivaan`. | Corrected all three paths. Queue behavior passed the navigation test; every referenced replacement asset was checked for existence and nonzero size. |
| Case-sensitive files | `README.md` and `Readme.md` collide on case-insensitive filesystems. | Removed the redundant one-line `Readme.md`; retained the complete `README.md`. Final case-collision scan passed. |
| Secrets/artifacts | A cookie path was tracked, and the repository contained `tatus`, one-byte accidental files, and an inactive duplicate CI file. | Removed the cookie path and non-source artifacts; expanded Git/Docker exclusions for env, cookie, session, and cache files. No feature module or media asset was removed. |
| CI | Tests depended on the runner’s preinstalled tools and lacked dependency/import guards. | Added explicit FFmpeg installation, recursive compilation, `pip check`, old-YouTube-import rejection, and tests to the real workflow. |
| Test fixtures | Several tests predated the required Instagram button, current asset directory, ESSE URL requirement, and HTTPX 0.27 JSON formatting. | Updated tests to assert current intended branding/assets and version-independent JSON semantics; did not remove features or weaken provider assertions. |
| Repository metadata | `app.json` and a command example used `YOUR_GITHUB_USERNAME`. | Updated both to `https://github.com/dausaloki/DausaXmusic`. |

## Requirements compatibility verified

| Component | Audited version/state | Result |
|---|---|---|
| Python | 3.12.16 | Compatible; also retains the `audioop` module used by Voice Play. Python 3.13 is not the configured target. |
| Kurigram / Pyrogram API | `kurigram==2.2.26` | Imports and native button/UI tests passed. |
| PyTgCalls | `py-tgcalls==2.3.3` | Compatible with the pinned NTgCalls range. |
| NTgCalls | `ntgcalls==2.2.5` | Satisfies PyTgCalls `>=2.2.4,<3.0.0`; native package installed and imported. |
| TgCrypto | `tgcrypto==1.2.5` | Built/installed and imported successfully. |
| yt-dlp | `yt-dlp==2026.7.4` | Installed/imported on Python 3.12; retained without an unnecessary upgrade. |
| youtube-search-python | `1.6.6` | Async exports verified; real search passed with HTTPX 0.27.2. `Recommendations` is absent by package design. |
| HTTPX | `0.27.2` with HTTP/2 extra | Supports the `proxies=` API required by youtube-search-python; project tests passed. |
| gpytranslate | `1.5.1` | Preserves the project’s translator API and works with HTTPX 0.27.2; real translation passed. |
| heroku3 / six | `heroku3==5.2.1`, `six==1.17.0` | Missing transitive import fixed. |
| Pillow | `pillow==12.3.0` | Image/media tests passed. |
| Motor / PyMongo | `motor==3.7.1`, resolved `pymongo==4.19.0` | Installed/imported; no live external MongoDB claimed. |
| FFmpeg / FFprobe | Installed during audit; Dockerfile installs both via `ffmpeg` | Media tests passed; Docker build itself was not run. |

A fresh Python 3.12 virtual environment was created from the final `requirements.txt`. Installation succeeded, and `pip check` reported all 110 installed packages (including pytest) compatible.

## Tests actually performed

| Check | Result |
|---|---|
| Recursive `compileall` over `DAUSAXMUSIC`, `strings`, `scripts`, `tests`, and `config.py` | Passed; 215 Python files, zero syntax errors. |
| Ruff critical checks (`E9`, `F63`, `F7`, `F82`) | Passed; no critical syntax/undefined-name findings. |
| Application module import sweep | 203 modules imported, 0 failures. |
| Top-level and deferred import assertions | 2,155 checked, 0 failures. |
| Offline pytest suite in the final clean environment | **149 passed; 3,088 subtests passed; 0 failed.** |
| Offline startup orchestration with Telegram/Mongo/PyTgCalls/idle mocked | Passed; all 115 plugin modules loaded and start/stop calls verified. This was not a live bot login. |
| Missing/blank required environment startup | Correctly exited 1 with the exact missing-variable list; no silent status-0 exit. |
| `sample.env` static and runtime parsing | 86 unique variables; defaults/branding verified; blank `MAX_CONCURRENT` retained its automatic default. |
| Utility credential loading/scrubbing | Safe test values reached phone/IP plugins and were removed from live subprocess environment as intended. |
| YouTube package exports | Required classes present; `Recommendations` confirmed absent; no unsupported import path remains in Python files. |
| Real YouTube search | Passed and returned a result with an ID and title. |
| Real translator request | Passed language detection and translation. |
| JSON/YAML/shell deployment parsing | Passed for Railway/app JSON, Heroku/Docker Compose/CI/dependabot/locale YAML, and `setup`/`start`. |
| Branding constants | All requested bot, owner, owner ID, support, updates, Instagram, and bot username values matched exactly. |
| Asset paths and case collisions | Replacement assets present/nonempty; no case-insensitive path collisions. |
| Secret scan | No Telegram token, credentialed remote Mongo URI, private key, `.env`, cookie, or session file found in the final working tree. |

One non-fatal upstream Kurigram event-loop deprecation warning was reported by pytest. Pydub can also emit its own invalid-escape `SyntaxWarning` messages on first import. These originate in installed third-party packages and did not prevent Python 3.12 imports, startup orchestration, media tests, or live search/translation checks.

## Not performed / remaining external checks

- No real Telegram bot or assistant login was performed.
- No production MongoDB connection, real voice chat, or audio/video call was tested.
- No Docker image was built or run; Docker configuration was statically inspected and the same Python/dependency/media checks were run directly.
- No GitHub commit/push or Railway deployment was performed.
- YouTube search and translation succeeded at audit time, but third-party availability can change. yt-dlp downloads, media playback, optional AI providers, and other external services still need live verification.
- Resso is already treated by the source as discontinued; this external limitation was not hidden or represented as fixed.
- `COOKIE_URL`, `DEEP_API`, and `ASSUSERNAME` remain as legacy declarations because they existed in the project, but no active consumer was found in this revision. They are optional and not needed for Railway startup. No cookies are bundled.
- Railway’s local cache/log filesystem is ephemeral; use MongoDB for persistence and size cache limits appropriately.

## Complete changed-file list

Status: **M** = modified, **A** = added, **D** = removed intentionally.

### Modified deployment/configuration/documentation files (10)

- **M** `.dockerignore`
- **M** `.github/workflows/ci.yml`
- **M** `.gitignore`
- **M** `DEPLOYMENT_CHECKLIST.md`
- **M** `PROJECT_STATUS.md`
- **M** `README.md`
- **M** `app.json`
- **M** `config.py`
- **M** `requirements.txt`
- **M** `sample.env`

### Modified application Python files (17)

- **M** `DAUSAXMUSIC/__main__.py`
- **M** `DAUSAXMUSIC/core/bot.py`
- **M** `DAUSAXMUSIC/core/mongo.py`
- **M** `DAUSAXMUSIC/core/userbot.py`
- **M** `DAUSAXMUSIC/platforms/Youtube.py`
- **M** `DAUSAXMUSIC/plugins/Kishu/ip.py`
- **M** `DAUSAXMUSIC/plugins/Kishu/wishcute.py`
- **M** `DAUSAXMUSIC/plugins/bot/inline.py`
- **M** `DAUSAXMUSIC/plugins/bot/start.py`
- **M** `DAUSAXMUSIC/plugins/misc/downloadrepo.py`
- **M** `DAUSAXMUSIC/plugins/tools/couples.py`
- **M** `DAUSAXMUSIC/plugins/tools/phone.py`
- **M** `DAUSAXMUSIC/plugins/tools/queue.py`
- **M** `DAUSAXMUSIC/security.py`
- **M** `DAUSAXMUSIC/utils/lyrics.py`
- **M** `DAUSAXMUSIC/utils/thumbnails.py`
- **M** `DAUSAXMUSIC/utils/tuning.py`

### Modified tests (3)

- **M** `tests/test_esse_autoplay.py`
- **M** `tests/test_public_providers.py`
- **M** `tests/test_rich_buttons.py`

### Added documentation (4)

- **A** `AUDIT_REPORT.md`
- **A** `ENVIRONMENT_VARIABLES.md`
- **A** `GITHUB_UPLOAD.md`
- **A** `RAILWAY_DEPLOYMENT_HI.md`

### Removed redundant/unsafe/artifact files (8)

- **D** `.github/.github` — one-byte accidental artifact.
- **D** `.github/ci.yml` — inactive duplicate of the real workflow.
- **D** `DAUSAXMUSIC/DAUSAXMUSI` — one-byte accidental artifact.
- **D** `DAUSAXMUSIC/cookies.txt` — cookie files are excluded from the deliverable.
- **D** `DAUSAXMUSIC/core/core` — one-byte accidental artifact.
- **D** `Readme.md` — redundant case-variant pointer; full `README.md` retained.
- **D** `tatus` — generated diff/status output, not source.
- **D** `tests/tests` — one-byte accidental artifact.

**Total paths changed: 42.** No music command, plugin, feature module, UI module, locale, required asset, or license file was removed.
