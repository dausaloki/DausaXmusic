# GitHub upload and pull-request instructions

Use the `complete-rebuild` review branch. Do **not** upload directly over `main`, and do not upload the ZIP itself as application source. The final package is `DausaXmusic-Complete-Rebuild.zip`; its single top-level folder is `DausaXmusic/`.

## Android / Termux method

GitHub's mobile app is not reliable for a complete nested source tree. Termux preserves all project folders, assets and tests.

### 1. Extract and inspect

Install Termux from its official source, place the ZIP in Downloads, then run:

```bash
pkg update
pkg install git gh unzip
termux-setup-storage
cd ~/storage/downloads
rm -rf dausa-complete-rebuild
mkdir dausa-complete-rebuild
unzip DausaXmusic-Complete-Rebuild.zip -d dausa-complete-rebuild
```

The extracted `dausa-complete-rebuild/DausaXmusic/` directory must directly contain `Dockerfile`, `railway.json`, `requirements.txt`, `config.py`, `sample.env`, `PR_DESCRIPTION.md`, `FINAL_BUILD_INFO.md` and `DAUSAXMUSIC/`. There must not be a second nested project root. `FINAL_BUILD_INFO.md` records the exact audited commit from which the ZIP was generated.

### 2. Authenticate without exposing a token

```bash
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
```

Open the displayed GitHub page in Chrome and approve the one-time code. Use an account authorized to write to `dausaloki/DausaXmusic`. Never place a token in Git, the ZIP, or a shell command.

### 3. Clone and create the review branch

```bash
cd ~
git clone https://github.com/dausaloki/DausaXmusic.git
cd DausaXmusic
git checkout main
git pull origin main
git checkout -B complete-rebuild
cp -a ~/storage/downloads/dausa-complete-rebuild/DausaXmusic/. ./
git status
git diff --check
```

The `cp` source is the extracted directory containing the root Dockerfile. This rebuild intentionally removes no file relative to customized main `86bec22`; do not use a destructive `rsync --delete` or delete feature/assets manually.

### 4. Review and stage safely

```bash
git status
git diff --stat
git diff --check

git add -A
git diff --cached --check
git diff --cached --stat

# This command must print nothing. If it prints a path, stop and unstage it.
git diff --cached --name-only | grep -Ei '(^|/)(\.env(\..*)?|cookies\.txt|[^/]*\.session|[^/]*\.session-journal)$'
```

Also inspect staged text for real bot tokens, session strings, cookie values, API keys and MongoDB credentials. Filename checks alone are not enough.

Optional local verification with Python 3.12 and FFmpeg:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pytest
pip check
python -m compileall -q DAUSAXMUSIC strings scripts tests config.py
python -m pytest -q
```

### 5. Commit, push, and open the PR

If Git asks for identity, set **your own** GitHub name/email with `git config user.name` and `git config user.email`; never put credentials there.

```bash
git commit -m "Complete DausaXmusic audit and playback hardening"
git push -u origin complete-rebuild

gh pr create \
  --base main \
  --head complete-rebuild \
  --title "Complete DausaXmusic audit and playback hardening" \
  --body-file PR_DESCRIPTION.md
```

If the branch or PR already exists, do not create a duplicate: push the reviewed commit and open the existing PR in Chrome instead. Review the changed-file list and GitHub Actions before merging. Railway connected to `main` should deploy only after you deliberately merge, or you can select the review branch in Railway for a controlled test.

## Computer / command-line method

### 1. Clone and branch

```bash
git clone https://github.com/dausaloki/DausaXmusic.git
cd DausaXmusic
git checkout main
git pull origin main
git checkout -B complete-rebuild
```

### 2. Copy the extracted contents

Replace the example source with your actual extraction path:

```bash
rsync -av \
  --exclude='.git' \
  --exclude='.env' \
  --exclude='.env.*' \
  --exclude='*.session' \
  --exclude='*.session-journal' \
  /absolute/path/to/extracted/DausaXmusic/ ./
```

The trailing `/` is important. Do not add `--delete`; no file deletion is part of this rebuild. Keep local `.env`, cookie and session files outside the copied tree.

### 3. Review, test, commit, and open the PR

Use the same secret checks and test commands shown in the Android section, then:

```bash
git add -A
git diff --cached --check
git commit -m "Complete DausaXmusic audit and playback hardening"
git push -u origin complete-rebuild
gh pr create --base main --head complete-rebuild \
  --title "Complete DausaXmusic audit and playback hardening" \
  --body-file PR_DESCRIPTION.md
```

## After upload

- Confirm `.github/workflows/ci.yml` completes FFmpeg installation, dependency checks, compilation, import guard and tests.
- Compare the PR against `COMPLETE_REBUILD_REPORT.md` and `docs/upstream-comparison.csv`.
- Follow `RAILWAY_DEPLOYMENT_HI.md` for exact variables and the Railway IP/session limitation.
- Complete `DEPLOYMENT_CHECKLIST.md` with real Telegram, MongoDB and voice-chat checks; sandbox tests do not replace them.
- Never add real credentials to GitHub to make Railway work; enter them only in Railway Variables.
- Do not modify the separate Quiz Bot.
