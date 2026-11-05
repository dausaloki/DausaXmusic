# GitHub upload instructions

Use a review branch first so the corrected tree can be compared before deployment.

## 1. Extract and inspect the ZIP

Extract `DausaXmusic-Railway-Fixed.zip`. Inside it is one top-level `DausaXmusic/` directory. That directory must contain `Dockerfile`, `railway.json`, `requirements.txt`, `config.py`, `sample.env`, and the `DAUSAXMUSIC/` package directly.

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
git commit -m "Fix Railway deployment and complete project audit"
git push -u origin railway-deployment-fix
```

Open the pull request on GitHub, review the changed-file list and CI result, then merge into `main`. If Railway is connected to `main`, merging will normally trigger a new deployment.

To update an existing Railway deployment without opening a pull request, push the reviewed branch and select that branch in Railway, or merge the same reviewed commit into the branch Railway watches.

## 7. After upload

- Confirm GitHub Actions runs the workflow from `.github/workflows/ci.yml`.
- Confirm the workflow installs FFmpeg, checks dependencies, compiles the source, verifies YouTube imports, and runs tests.
- Follow `RAILWAY_DEPLOYMENT_HI.md` for variables and deployment.
- Never add real credentials to GitHub to make Railway work; enter them only in Railway Variables.
