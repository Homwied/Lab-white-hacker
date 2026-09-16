#!/data/data/com.termux/files/usr/bin/bash
set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || exit 1

echo "=== COUNCIL V12 SAFE AUTO-PUSH ==="

BRANCH="$(git branch --show-current)"

if [ -z "$BRANCH" ]; then
  echo "DITOLAK: branch Git tidak diketahui."
  exit 1
fi

if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
  echo "DITOLAK: auto-push tidak boleh langsung ke $BRANCH."
  exit 1
fi

if ! git diff --cached --quiet; then
  echo "DITOLAK: sudah ada file lain di staging Git."
  echo "Periksa dengan: git diff --cached --name-only"
  exit 1
fi

echo "[1/5] Pemeriksaan sintaks..."

bash -n main || exit 1

python -c '
import ast
from pathlib import Path
for name in ["main_v12.py", "08-mobile-intake/tools_health.py"]:
    ast.parse(Path(name).read_text())
    print("OK:", name)
' || exit 1

echo "[2/5] Pemeriksaan tools..."

python 08-mobile-intake/tools_health.py || exit 1

echo "[3/5] Pemeriksaan data sensitif..."

SAFE_FILES="
.gitignore
main
main_v12.py
08-mobile-intake/tools_health.py
upgrade_menu6.py
00-config/policy.conf
tools/safe-auto-push.sh
"

EXISTING_FILES=""

for file in $SAFE_FILES; do
  if [ -f "$file" ]; then
    EXISTING_FILES="$EXISTING_FILES $file"
  fi
done

if grep -En \
'ghp_[A-Za-z0-9]+|github_pat_[A-Za-z0-9_]+|BEGIN [A-Z ]*PRIVATE KEY|AKIA[A-Z0-9]+|xox[baprs]-' \
$EXISTING_FILES; then
  echo "DITOLAK: pola kredensial ditemukan."
  exit 1
fi

echo "[4/5] Menambahkan file sistem..."

git add -- $EXISTING_FILES

if git diff --cached --quiet; then
  echo "Tidak ada upgrade baru untuk dipush."
  exit 0
fi

echo
echo "FILE YANG AKAN DIPUSH:"
git diff --cached --name-only
echo

printf "Ketik PUSH untuk melanjutkan: "
read -r CONFIRM

if [ "$CONFIRM" != "PUSH" ]; then
  echo "Dibatalkan. File tetap berada di staging."
  exit 1
fi

STAMP="$(date -u '+%Y-%m-%d %H:%M UTC')"

git commit -m "V12 mobile upgrade: $STAMP" || exit 1

echo "[5/5] Push ke origin/$BRANCH..."

git push -u origin "$BRANCH" || exit 1

echo "AUTO-PUSH BERHASIL"
echo "Branch: $BRANCH"
