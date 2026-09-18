#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail
LAB="$HOME/lab-hacker-putih"
ALLOW="$LAB/00-config/targets_allow"
AUDIT="$LAB/09-audit-log/events.log"
REPORT_DIR="$LAB/06-report"

R="\033[1;31m"; G="\033[1;32m"; Y="\033[1;33m"; N="\033[0m"

TARGET="${1:-}"
if [ -z "$TARGET" ]; then
    echo "Usage: ./scan.sh <target>"
    echo "Target harus ada di whitelist:"
    grep -v '^#' "$ALLOW" | grep -v '^$'
    exit 1
fi

# WHITELIST ENFORCEMENT
if ! grep -qx "$TARGET" "$ALLOW"; then
    echo -e "${R}❌ TARGET TIDAK ADA DI WHITELIST: $TARGET${N}"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | SCAN_BLOCKED | NOT_WHITELISTED | target=$TARGET" >> "$AUDIT"
    exit 1
fi

mkdir -p "$REPORT_DIR"
TS=$(date +%Y%m%d-%H%M%S)
OUT="$REPORT_DIR/nmap-$TARGET-$TS.txt"

echo -e "${G}[+] Target allowed: $TARGET${N}"
echo -e "${Y}[*] Scanning (top 100 ports)...${N}"
nmap -sV -T4 --top-ports 100 "$TARGET" | tee "$OUT" || true

echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | SCAN | OK | target=$TARGET | out=$OUT" >> "$AUDIT"
echo -e "${G}[+] Selesai. Report: $OUT${N}"
