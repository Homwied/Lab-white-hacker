#!/data/data/com.termux/files/usr/bin/bash
BASE_DIR="$HOME/lab-hacker-putih"
REPORT_DIR="$BASE_DIR/06-report"
mkdir -p "$REPORT_DIR"
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; CYAN='\033[0;36m'; NC='\033[0m'

echo -e "${CYAN}=== COUNCIL OSINT V1.1 - 50 PLATFORM SULTAN ===${NC}"
read -p "Username audit: " USERNAME; [ -z "$USERNAME" ] && USERNAME="homwied"
DATE=$(date +%Y%m%d-%H%M%S)
TXT="$REPORT_DIR/REPORT-OSINT-V1.1-$USERNAME-$DATE.txt"
HTML="$REPORT_DIR/REPORT-OSINT-V1.1-$USERNAME-$DATE.html"

echo "<html><head><title>OSINT $USERNAME</title></head><body><h1>COUNCIL OSINT V1.1 - $USERNAME</h1><ul>" > "$HTML"
echo "Scanning $USERNAME 50 platform..." | tee "$TXT"

declare -A P
P["Instagram"]="https://instagram.com/$USERNAME"
P["Facebook"]="https://facebook.com/$USERNAME"
P["TikTok"]="https://tiktok.com/@$USERNAME"
P["X/Twitter"]="https://x.com/$USERNAME"
P["YouTube"]="https://youtube.com/@$USERNAME"
P["GitHub"]="https://github.com/$USERNAME"
P["GitLab"]="https://gitlab.com/$USERNAME"
P["Reddit"]="https://reddit.com/user/$USERNAME"
P["Twitch"]="https://twitch.tv/$USERNAME"
P["Steam"]="https://steamcommunity.com/id/$USERNAME"
P["Pinterest"]="https://pinterest.com/$USERNAME"
P["LinkedIn"]="https://linkedin.com/in/$USERNAME"
P["Medium"]="https://medium.com/@$USERNAME"
P["Blogger"]="https://$USERNAME.blogspot.com"
P["Behance"]="https://behance.net/$USERNAME"
P["Dribbble"]="https://dribbble.com/$USERNAME"
P["SoundCloud"]="https://soundcloud.com/$USERNAME"
P["Spotify"]="https://open.spotify.com/user/$USERNAME"
P["Telegram"]="https://t.me/$USERNAME"
P["Wattpad"]="https://wattpad.com/user/$USERNAME"
P["Patreon"]="https://patreon.com/$USERNAME"
P["Flickr"]="https://flickr.com/people/$USERNAME"
P["Vimeo"]="https://vimeo.com/$USERNAME"
P["Tumblr"]="https://$USERNAME.tumblr.com"
P["DeviantArt"]="https://deviantart.com/$USERNAME"
P["Keybase"]="https://keybase.io/$USERNAME"
P["Kaggle"]="https://kaggle.com/$USERNAME"
P["Codepen"]="https://codepen.io/$USERNAME"
P["Replit"]="https://replit.com/@$USERNAME"
P["HackerNews"]="https://news.ycombinator.com/user?id=$USERNAME"
P["ProductHunt"]="https://producthunt.com/@$USERNAME"
P["Disqus"]="https://disqus.com/$USERNAME"
P["Roblox"]="https://roblox.com/user.aspx?username=$USERNAME"
P["Gravatar"]="https://gravatar.com/$USERNAME"
P["About.me"]="https://about.me/$USERNAME"
P["500px"]="https://500px.com/$USERNAME"
P["Bandcamp"]="https://bandcamp.com/$USERNAME"
P["Bukalapak"]="https://bukalapak.com/u/$USERNAME"
P["Tokopedia"]="https://tokopedia.com/$USERNAME"
P["Shopee"]="https://shopee.co.id/$USERNAME"
P["Kaskus"]="https://kaskus.co.id/@$USERNAME"
P["Quora"]="https://quora.com/profile/$USERNAME"
P["SlideShare"]="https://slideshare.net/$USERNAME"
P["Scribd"]="https://scribd.com/$USERNAME"
P["BuyMeACoffee"]="https://buymeacoffee.com/$USERNAME"
P["Linktree"]="https://linktr.ee/$USERNAME"
P["Trakteer"]="https://trakteer.id/$USERNAME"
P["Saweria"]="https://saweria.co/$USERNAME"
P["Karyakarsa"]="https://karyakarsa.com/$USERNAME"
P["GitHub Gist"]="https://gist.github.com/$USERNAME"

FOUND=0; NF=0
for N in "${!P[@]}"; do
  U="${P[$N]}"; C=$(curl -s -o /dev/null -w "%{http_code}" -A "Mozilla/5.0" --max-time 6 -L "$U" 2>/dev/null)
  C=${C:-000}
  if [[ "$C" == "200" ]]; then echo -e "${GREEN}[FOUND] $N $C $U${NC}"; echo "[FOUND] $N : $U ($C)" | tee -a "$TXT"; echo "<li><b style=color:green>FOUND $N</b> <a href=$U>$U</a> ($C)</li>" >> "$HTML"; FOUND=$((FOUND+1))
  else echo -e "${RED}[NOT] $N $C${NC}"; echo "[NOT] $N : $U ($C)" >> "$TXT"; NF=$((NF+1)); fi
done
echo "</ul><h2>HASIL: $FOUND KETEMU / $NF GAK ADA</h2></body></html>" >> "$HTML"
echo ">>> HASIL V1.1: $FOUND KETEMU | $NF GAK ADA" | tee -a "$TXT"
cd "$BASE_DIR"; git add 06-report/; git commit -m "Council OSINT V1.1 $USERNAME $FOUND found 50 platform $(date +%H%M)" 2>/dev/null; git push 2>/dev/null && echo -e "${GREEN}>>> PUSH V1.1 BERHASIL!${NC}"
echo -e "${CYAN}TXT: $TXT\nHTML: $HTML${NC}"
