#!/data/data/com.termux/files/usr/bin/bash
BASE_DIR="$HOME/lab-hacker-putih"
REPORT_DIR="$BASE_DIR/06-report"
mkdir -p "$REPORT_DIR"
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'
echo -e "${GREEN}=== COUNCIL V10 FINAL GABUNGAN V9.1+V9.2 ===${NC}"
echo " [1] Scan doang (V9.1) - laporan cuma di HP"
echo " [2] Scan + Auto Push GitHub (V9.2)"
echo " [3] Multi Scan google.com+scanme+example + Push"
read -p "Mode [1-3]: " MODE
echo "Target: 1)scanme 2)google.com 3)example.com 4)custom"
read -p "Target [1-4]: " TPIL
case $TPIL in 1) TARGET="scanme.nmap.org";; 2) TARGET="google.com";; 3) TARGET="example.com";; 4) read -p "Target: " TARGET;; *) TARGET="scanme.nmap.org";; esac
if [[ "$MODE" == "3" ]]; then TARGETS=("scanme.nmap.org" "google.com" "example.com"); else TARGETS=("$TARGET"); fi
for T in "${TARGETS[@]}"; do DATE=$(date +%Y%m%d-%H%M%S); R="$REPORT_DIR/REPORT-V10-$T-$DATE.txt"; echo -e "${YELLOW}[*] Scanning $T...${NC}"; { echo "=== COUNCIL V10 $T $(date) Indralaya ==="; nmap --top-ports 20 "$T" 2>&1; } > "$R"; cat "$R"; done
if [[ "$MODE" == "1" ]]; then echo -e "${GREEN}SELESAI MODE 1 HP ONLY${NC}"; exit 0; fi
cd "$BASE_DIR"; git add 06-report/; git commit -m "Council V10 mode $MODE ${TARGETS[*]} $(date +%Y%m%d-%H%M) Indralaya" 2>/dev/null || true; git pull --rebase origin main 2>/dev/null || git pull origin main || true; git push origin main; echo -e "${GREEN}PUSH BERHASIL ke Homwied/Lab-white-hacker${NC}"
