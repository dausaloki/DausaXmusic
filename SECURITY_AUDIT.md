# Security Audit

Date: 2026-11-06
Scope: final three-source rebuild and authorized playback hardening.

- Upstream's hardcoded Worker credential and `assets/cookies.txt` were excluded; no authenticated probe or credential migration was performed.
- `COOKIE_URL` is loaded through `config.py` before environment scrubbing, redacted as sensitive configuration, and consumed only as an optional operator-authorized Netscape cookie export.
- Cookie downloads require public HTTPS targets, revalidate up to three redirects, disable ambient proxy use, cap content at 1 MiB, validate Netscape rows, and use a private temporary directory (`0700`) and file (`0600`). Cookie URLs/content are not logged.
- Blank `COOKIE_URL` preserves anonymous playback. Invalid/unavailable cookie downloads disable only that optional cookie path and retry at most once per five minutes rather than on every track.
- Removed `verify=False` from the quote HTTP client and `nocheckcertificate=True` from YouTube/song yt-dlp options; normal TLS certificate verification is restored.
- Sanitized direct-download, background-cache, Worker and xBit diagnostic paths to avoid signed media URLs in logs.
- Regression coverage includes anonymous and configured extraction, HTTPS/redirect validation, malformed/oversized responses, private permissions, cached failures, secret-check defaults and URL log redaction.

Date: 2026-03-09
Scope: secret exposure hardening for subprocesses, logs, and user-controlled URL commands.

## Additional Hardening

6) Sensitive env isolation after startup
Files: `DAUSAXMUSIC/__init__.py`, `DAUSAXMUSIC/utils/security.py`
Patch: Sensitive env vars are stripped from the live process environment after config load so later child processes do not inherit bot secrets by default.

7) Clean subprocess environments
Files: `DAUSAXMUSIC/core/call.py`, `DAUSAXMUSIC/core/git.py`, `DAUSAXMUSIC/platforms/Youtube.py`, `DAUSAXMUSIC/plugins/sudo/restart.py`, `DAUSAXMUSIC/plugins/tools/kang.py`, `DAUSAXMUSIC/plugins/tools/tiny.py`, `DAUSAXMUSIC/plugins/tools/videoedit.py`, `DAUSAXMUSIC/utils/formatters.py`
Patch: Child processes now run with a reduced allowlisted environment instead of inheriting all loaded secrets.

8) Secret redaction in logs and error reports
Files: `DAUSAXMUSIC/logging.py`, `DAUSAXMUSIC/utils/errors.py`, `DAUSAXMUSIC/utils/security.py`
Patch: Known env and config secrets are redacted before being written to logs, paste output, or Telegram error messages.

9) SSRF and untrusted URL hardening
Files: `DAUSAXMUSIC/plugins/Kishu/webdl.py`, `DAUSAXMUSIC/plugins/misc/urlshortner.py`, `DAUSAXMUSIC/plugins/misc/downloadrepo.py`, `DAUSAXMUSIC/utils/security.py`
Patch: Public URL validation now blocks localhost, private IPs, credentialed URLs, redirects to untrusted hosts, and URLs containing secret values. `webdl` and `downloadrepo` were restricted to `SUDOERS`, and repo downloads are limited to HTTPS GitHub repos.

Date: 2026-02-05
Scope: command injection / shell execution and minimal safety hardening per request.

## Findings

1) Playlist command injection via yt-dlp shell invocation
File: `DAUSAXMUSIC/platforms/Youtube.py:239-266`
Issue: Playlist URL was interpolated into a shell command.
Patch: Replaced shell execution with list-args execution and added minimal URL character blocking (`; & | $ \n \r `).

2) Shell execution in ffmpeg speedup
File: `DAUSAXMUSIC/core/call.py:176-185`
Issue: ffmpeg command built as a shell string.
Patch: Use `create_subprocess_exec` with shlex-split args.

3) os.system use in update/restart commands
File: `DAUSAXMUSIC/plugins/sudo/restart.py:73-155`
Issue: git and heroku commands executed via shell (heroku push includes API key in command string).
Patch: Use `subprocess.run` with list args and suppress output.

4) os.system in video editing
File: `DAUSAXMUSIC/plugins/tools/videoedit.py:50-61`
Issue: ffmpeg command executed via shell.
Patch: Use `subprocess.run` with list args.

5) os.system in tiny sticker conversion
File: `DAUSAXMUSIC/plugins/tools/tiny.py:34-40`
Issue: lottie_convert commands executed via shell.
Patch: Use `subprocess.run` with list args.

## Secrets
`.env` is already gitignored and no `.env` file exists in the repo.

## Tests
`python -m py_compile DAUSAXMUSIC/platforms/Youtube.py`
`python -m py_compile DAUSAXMUSIC/core/call.py`
`python -m py_compile DAUSAXMUSIC/plugins/sudo/restart.py`
`python -m py_compile DAUSAXMUSIC/plugins/tools/videoedit.py DAUSAXMUSIC/plugins/tools/tiny.py`
