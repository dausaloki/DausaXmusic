# GitHub upload instructions

Use a review branch first so the corrected tree can be compared before deployment.

## Android / Termux method (recommended for a complete folder upload)

GitHub's mobile app is not reliable for uploading a complete nested source tree. On Android, use Termux so folder structure and all 200+ project files are preserved. Do not upload the ZIP itself.

1. Install Termux from its official source, place `DausaXmusic-Railway-Playback-Fixed.zip` in your Downloads folder, and run:

```bash
pkg update
pkg install git gh unzip
termux-setup-storage
cd ~/storage/downloads
rm -rf dausa-playback-fix
mkdir dausa-playback-fix
unzip DausaXmusic-Railway-Playback-Fixed.zip -d dausa-playback-fix
```

2. Authenticate without putting a token in the repository or command line:

```bash
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
```

Open the shown GitHub page in Chrome and approve the one-time code. Use an account authorized to write to `dausaloki/DausaXmusic`.

3. Clone, copy the extracted contents, and review:

```bash
cd ~
git clone https://github.com/dausaloki/DausaXmusic.git
cd DausaXmusic
git checkout main
git pull origin main
git checkout -b railway-playback-fix
cp -a ~/storage/downloads/dausa-playback-fix/DausaXmusic/. ./
git status
git diff --check
```

The source path above is the extracted directory containing `Dockerfile`, `requirements.txt`, `config.py`, and the `DAUSAXMUSIC/` package. Do not create a second nested `DausaXmusic/DausaXmusic` root.

4. Confirm no secret file is staged, then commit and push:

```bash
git add -A
git diff --cached --name-only | grep -Ei '(^|/)(\.env(\..*)?|cookies\.txt|[^/]*\.session|[^/]*\.session-journal)$'
# The command above must print nothing.
git commit -m "Fix direct YouTube playback on Railway"
git push -u origin railway-playback-fix
```

If Git asks for name/email, set your own GitHub identity with `git config user.name` and `git config user.email`; never put credentials in those values. Open the branch link in Chrome, create a pull request, review it, and merge into `main`. Railway connected to `main` should then build a new deployment.

## Computer / command-line method

## 1. Extract and inspect the ZIP

Extract `DausaXmusic-Railway-Playback-Fixed.zip`. Inside it is one top-level `DausaXmusic/` directory. That directory must contain `Dockerfile`, `railway.json`, `requirements.txt`, `config.py`, `sample.env`, and the `DAUSAXMUSIC/` package directly.

Do **not** upload the ZIP itself as the application source, and do not create an extra nested project root.

## 2. Clone your repository and create a branch

```bash
git clone https://github.com/dausaloki/DausaXmusic.git
cd DausaXmusic
git checkout main
git pull origin main
git checkout -b railway-deployment-fix
```

If you are using a fork or a different default branch, substitute that repository/branch name.

## 3. Copy the corrected tree

On Linux/macOS, from the cloned repository root (replace the example path with your real extraction path):

```bash
rsync -av --delete \
  --exclude='.git' \
  --exclude='.env' \
  --exclude='.env.*' \
  --exclude='*.session' \
  --exclude='*.session-journal' \
  /absolute/path/to/extracted/DausaXmusic/ ./
```

The trailing `/` on the source path is important. `--delete` is used so removed redundant/artifact files are also reflected; the exclusions protect `.git` and local secret files. Verify the source path before running it.

Without `rsync`, copy the extracted contents into the clone manually, without copying any `.git` directory. Also apply these deliberate deletions if they still exist in the clone:

- `Readme.md` (redundant case-variant of `README.md`)
- `DAUSAXMUSIC/cookies.txt` (cookies must not be distributed)
- `tatus`
- `DAUSAXMUSIC/DAUSAXMUSI`
- `DAUSAXMUSIC/core/core`
- `tests/tests`
- `.github/.github`
- `.github/ci.yml` (inactive duplicate; keep `.github/workflows/ci.yml`)

Keep your local `.env` and session files private; they are not part of the corrected ZIP.

## 4. Review before staging

```bash
git status
find . -maxdepth 2 -type f -name 'Dockerfile' -o -name 'railway.json' -o -name 'requirements.txt'
git diff --stat
git diff --check
```

Confirm that the repository root is correct and no feature/asset directories were accidentally omitted.

Optional local verification with Python 3.12 and FFmpeg installed:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt pytest
pip check
python -m compileall -q DAUSAXMUSIC strings scripts tests config.py
python -m pytest -q
```

## 5. Stage and perform a secret-file check

```bash
git add -A
git diff --cached --check
git diff --cached --stat

# This should print nothing. If it prints a path, stop and remove that file from staging.
git diff --cached --name-only | grep -Ei '(^|/)(\.env(\..*)?|cookies\.txt|[^/]*\.session|[^/]*\.session-journal)$'
```

Also inspect staged configuration changes before committing. Do not rely only on filenames: make sure no token, session string, API secret, private cookie, or database credential appears in the diff.

## 6. Commit, push, and merge

```bash
git commit -m "Fix direct YouTube playback on Railway"
git push -u origin railway-deployment-fix
```

Open the pull request on GitHub, review the changed-file list and CI result, then merge into `main`. If Railway is connected to `main`, merging will normally trigger a new deployment.

To update an existing Railway deployment without opening a pull request, push the reviewed branch and select that branch in Railway, or merge the same reviewed commit into the branch Railway watches.

## 7. After upload

- Confirm GitHub Actions runs the workflow from `.github/workflows/ci.yml`.
- Confirm the workflow installs FFmpeg, checks dependencies, compiles the source, verifies YouTube imports, and runs tests.
- Follow `RAILWAY_DEPLOYMENT_HI.md` for variables and deployment.
- Never add real credentials to GitHub to make Railway work; enter them only in Railway Variables.
