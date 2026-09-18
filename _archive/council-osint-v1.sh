#!/data/data/com.termux/files/usr/bin/bash
BASE_DIR="$HOME/lab-hacker-putih"
REPORT_DIR="$BASE_DIR/06-report"
mkdir -p "$REPORT_DIR"
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'

echo -e "${CYAN}=== COUNCIL OSINT V1 - JEJAK DIGITAL USERNAME ===${NC}"
echo -e "${YELLOW}DISCLAIMER: HANYA UNTUK SELF AUDIT & EDUKASI PRIVASI!${NC}"
echo ""
read -p "Masukin username yang mau di audit (contoh: homwied): " USERNAME
if [ -z "$USERNAME" ]; then USERNAME="homwied"; fi

DATE=$(date +%Y%m%d-%H%M%S)
REPORT="$REPORT_DIR/REPORT-OSINT-V1-$USERNAME-$DATE.txt"

echo "Scanning username: $USERNAME" | tee "$REPORT"
echo "Tanggal: $DATE - Indralaya" | tee -a "$REPORT"
echo "=========================================" | tee -a "$REPORT"

# List 20 platform populer - versi ringan dari 3398 tadi
declare -A PLATFORMS
PLATFORMS["Instagram"]="https://instagram.com/$USERNAME"
PLATFORMS["Facebook"]="https://facebook.com/$USERNAME"
PLATFORMS["Twitter/X"]="https://x.com/$USERNAME"
PLATFORMS["TikTok"]="https://tiktok.com/@$USERNAME"
PLATFORMS["YouTube"]="https://youtube.com/@$USERNAME"
PLATFORMS["GitHub"]="https://github.com/$USERNAME"
PLATFORMS["GitLab"]="https://gitlab.com/$USERNAME"
PLATFORMS["Reddit"]="https://reddit.com/user/$USERNAME"
PLATFORMS["Medium"]="https://medium.com/@$USERNAME"
PLATFORMS["Pinterest"]="https://pinterest.com/$USERNAME"
PLATFORMS["Twitch"]="https://twitch.tv/$USERNAME"
PLATFORMS["Steam"]="https://steamcommunity.com/id/$USERNAME"
PLATFORMS["SoundCloud"]="https://soundcloud.com/$USERNAME"
PLATFORMS["Spotify"]="https://open.spotify.com/user/$USERNAME"
PLATFORMS["Telegram"]="https://t.me/$USERNAME"
PLATFORMS["LinkedIn"]="https://linkedin.com/in/$USERNAME"
PLATFORMS["Behance"]="https://behance.net/$USERNAME"
PLATFORMS["Dribbble"]="https://dribbble.com/$USERNAME"
PLATFORMS["Wattpad"]="https://wattpad.com/user/$USERNAME"
PLATFORMS["Blogger"]="https://$USERNAME.blogspot.com"

FOUND=0
NOTFOUND=0
FOUND_LIST=""

for NAME in "${!PLATFORMS[@]}"; do
  URL="${PLATFORMS[$NAME]}"
  echo -n "[*] Cek $NAME... "
  CODE=$(curl -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0" --max-time 8 -L "$URL" 2>/dev/null | tr -d '\n\r ')
  CODE=${CODE:-000}
  if [[ "$CODE" == "200" ]]; then
    echo -e "${GREEN}KETEMU 200 $URL${NC}"
    echo "[FOUND] $NAME : $URL (200)" | tee -a "$REPORT"
    FOUND=$((FOUND+1))
    FOUND_LIST="$FOUND_LIST $NAME,"
  elif [[ "$CODE" == "404" ]]; then
    echo -e "${RED}Gak ada 404${NC}"
    echo "[NOT FOUND] $NAME : $URL (404)" >> "$REPORT"
    NOTFOUND=$((NOTFOUND+1))
  else
    echo -e "${YELLOW}Ragu $CODE${NC}"
    echo "[UNKNOWN $CODE] $NAME : $URL" >> "$REPORT"
  fi
done

echo "=========================================" | tee -a "$REPORT"
echo ">>> HASIL OSINT V1: $FOUND KETEMU | $NOTFOUND GAK ADA" | tee -a "$REPORT"
echo ">>> Username: $USERNAME" | tee -a "$REPORT"
echo ">>> Daftar ketemu:$FOUND_LIST" | tee -a "$REPORT"
echo ""
if [ "$FOUND" -gt 0 ]; then
  echo -e "${GREEN}>>> SUKSES: $USERNAME punya jejak di $FOUND platform!${NC}"
  echo ">>> CEK MANUAL: Buka link [FOUND] di laporan buat audit postingan lama!"
  echo ">>> TIPS: Kalau ada postingan 2004 / PDF / PPT ke-index, hapus / private!"
else
  echo -e "${YELLOW}>>> BERSIH: $USERNAME gak ketemu di 20 platform populer!${NC}"
fi

cd "$BASE_DIR"
git add 06-report/ 2>/dev/null
git commit -m "Council OSINT V1 $USERNAME $FOUND found $(date +%Y%m%d-%H%M) Indralaya" 2>/dev/null || true
git pull --rebase origin main 2>/dev/null || true
git push origin main 2>/dev/null && echo -e "${GREEN}>>> PUSH BERHASIL KE GITHUB!${NC}" || echo -e "${YELLOW}>>> Laporan lokal aja (push gagal, cek internet)${NC}"
ls -lh "$REPORT"
echo -e "${CYAN}Laporan: $REPORT${NC}"
