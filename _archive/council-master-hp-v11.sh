#!/data/data/com.termux/files/usr/bin/bash
BASE_DIR="$HOME/lab-hacker-putih"
REPORT_DIR="$BASE_DIR/06-report"
mkdir -p "$REPORT_DIR"
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
echo -e "${GREEN}=== COUNCIL V11.1 FINAL FIX ===${NC}"
TARGET="google.com"
DATE=$(date +%Y%m%d-%H%M%S)
REPORT="$REPORT_DIR/REPORT-V11-google.com-$DATE.txt"
echo -e "${YELLOW}STEP 1: Scanning $TARGET...${NC}"
nmap --top-ports 20 "$TARGET" > "$REPORT" 2>&1 || true
cat "$REPORT"
OPEN_COUNT=$(grep -c " open " "$REPORT" 2>/dev/null | tr -d '\n\r ' || echo 0)
FILTERED=$(grep -E -c "0 hosts up|Failed to resolve" "$REPORT" 2>/dev/null | tr -d '\n\r ' || echo 0)
# sanitasi biar gak "0 0"
OPEN_COUNT=${OPEN_COUNT:-0}
FILTERED=${FILTERED:-0}
echo -e "${CYAN}>>> Hasil: $OPEN_COUNT open | Filtered: $FILTERED${NC}"
if [ "$OPEN_COUNT" -eq 0 ] || [ "$FILTERED" -gt 0 ]; then
  echo -e "${RED}>>> WARNING: $TARGET filtered! Fallback ke scanme.nmap.org...${NC}"
  TARGET="scanme.nmap.org"
  DATE2=$(date +%Y%m%d-%H%M%S)
  REPORT2="$REPORT_DIR/REPORT-V11-FALLBACK-$TARGET-$DATE2.txt"
  nmap --top-ports 20 "$TARGET" > "$REPORT2" 2>&1 || true
  cat "$REPORT2"
  REPORT="$REPORT2"
else
  echo -e "${GREEN}>>> SUKSES: $TARGET VALID!${NC}"
fi
cd "$BASE_DIR"; git add 06-report/; git commit -m "Council V11.1 $TARGET $DATE Indralaya" 2>/dev/null || true; git pull --rebase origin main 2>/dev/null || true; git push origin main; echo -e "${GREEN}>>> PUSH BERHASIL${NC}"; ls -lh "$REPORT"
